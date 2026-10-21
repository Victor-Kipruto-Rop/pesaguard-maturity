"""Strict CSV statement parsing with all-or-nothing validation.

Persistence, upload authorization, malware scanning, and durable idempotency belong
to the application layer. This parser only normalizes untrusted CSV bytes.
"""

from __future__ import annotations

import csv
import hashlib
import io
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Literal


@dataclass(frozen=True, slots=True)
class StatementColumnMap:
    reference: str = "reference"
    amount: str = "amount"
    currency: str = "currency"
    occurred_at: str = "occurred_at"


@dataclass(frozen=True, slots=True)
class ImportedStatementRow:
    row_number: int
    reference: str
    amount: Decimal
    currency: str
    occurred_at: datetime
    fingerprint: str


@dataclass(frozen=True, slots=True)
class ImportIssue:
    row_number: int
    code: Literal[
        "invalid_csv",
        "missing_header",
        "missing_column",
        "missing_value",
        "invalid_amount",
        "invalid_currency",
        "invalid_timestamp",
        "duplicate_row",
        "row_limit_exceeded",
    ]
    message: str


@dataclass(frozen=True, slots=True)
class StatementImportResult:
    rows: tuple[ImportedStatementRow, ...]
    issues: tuple[ImportIssue, ...]
    content_sha256: str

    @property
    def accepted(self) -> bool:
        return not self.issues


def _normalize_reference(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).strip().casefold()
    return re.sub(r"[^a-z0-9]", "", value)


def parse_statement_csv(
    content: bytes,
    *,
    tenant_id: str,
    columns: StatementColumnMap = StatementColumnMap(),
    max_bytes: int = 5_000_000,
    max_rows: int = 100_000,
) -> StatementImportResult:
    """Parse a UTF-8 CSV statement and reject the whole file on any row error.

    The tenant is passed by trusted application context; it is never read from
    the uploaded file. Timestamps must be ISO-8601 and timezone-aware. Amounts
    are parsed with Decimal, never binary floating point.
    """
    digest = hashlib.sha256(content).hexdigest()
    issues: list[ImportIssue] = []
    if not tenant_id.strip():
        return StatementImportResult((), (ImportIssue(0, "missing_value", "tenant_id is required"),), digest)
    if max_bytes <= 0 or max_rows <= 0:
        raise ValueError("max_bytes and max_rows must be positive")
    if len(content) > max_bytes:
        return StatementImportResult((), (ImportIssue(0, "invalid_csv", "file exceeds size limit"),), digest)
    if not content:
        return StatementImportResult((), (ImportIssue(0, "missing_header", "file is empty"),), digest)

    try:
        text = content.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)
        headers = reader.fieldnames
        if not headers:
            return StatementImportResult((), (ImportIssue(1, "missing_header", "CSV header is required"),), digest)
        required = {columns.reference, columns.amount, columns.currency, columns.occurred_at}
        missing = sorted(required.difference(headers))
        if missing:
            return StatementImportResult(
                (),
                tuple(ImportIssue(1, "missing_column", f"required column missing: {name}") for name in missing),
                digest,
            )

        normalized_rows: list[ImportedStatementRow] = []
        seen_fingerprints: set[str] = set()
        for row_number, row in enumerate(reader, start=2):
            if row_number - 1 > max_rows:
                issues.append(ImportIssue(row_number, "row_limit_exceeded", "row limit exceeded"))
                break
            if None in row:
                issues.append(ImportIssue(row_number, "invalid_csv", "row contains extra columns"))
                continue
            reference = (row.get(columns.reference) or "").strip()
            amount_text = (row.get(columns.amount) or "").strip()
            currency = (row.get(columns.currency) or "").strip().upper()
            timestamp_text = (row.get(columns.occurred_at) or "").strip()
            if not reference or not amount_text or not currency or not timestamp_text:
                issues.append(ImportIssue(row_number, "missing_value", "required value is blank"))
                continue
            try:
                amount = Decimal(amount_text)
                if not amount.is_finite():
                    raise InvalidOperation
            except (InvalidOperation, ValueError):
                issues.append(ImportIssue(row_number, "invalid_amount", "amount must be a finite decimal"))
                continue
            if not re.fullmatch(r"[A-Z]{3}", currency):
                issues.append(ImportIssue(row_number, "invalid_currency", "currency must be a three-letter code"))
                continue
            try:
                occurred_at = datetime.fromisoformat(timestamp_text.replace("Z", "+00:00"))
                if occurred_at.tzinfo is None or occurred_at.utcoffset() is None:
                    raise ValueError("timezone required")
            except ValueError:
                issues.append(ImportIssue(row_number, "invalid_timestamp", "timestamp must be ISO-8601 with timezone"))
                continue

            canonical = "|".join((
                _normalize_reference(reference),
                format(amount, "f"),
                currency,
                occurred_at.isoformat(),
            ))
            fingerprint = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
            if fingerprint in seen_fingerprints:
                issues.append(ImportIssue(row_number, "duplicate_row", "duplicate statement row"))
                continue
            seen_fingerprints.add(fingerprint)
            normalized_rows.append(ImportedStatementRow(
                row_number=row_number,
                reference=reference,
                amount=amount,
                currency=currency,
                occurred_at=occurred_at,
                fingerprint=fingerprint,
            ))
    except (UnicodeDecodeError, csv.Error):
        return StatementImportResult((), (ImportIssue(0, "invalid_csv", "file is not valid UTF-8 CSV"),), digest)

    # Never partially accept a file. Callers must present validation issues to
    # the user and create an import job only after the complete file is valid.
    if issues:
        return StatementImportResult((), tuple(issues), digest)
    return StatementImportResult(tuple(normalized_rows), (), digest)
