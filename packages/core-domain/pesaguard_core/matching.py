"""Conservative, deterministic reconciliation matching primitives.

This module is intentionally framework- and database-independent. It does not
initiate payments or mutate financial records. Persist results and audit events
in the application layer after applying domain and authorization checks.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from collections.abc import Sequence
from typing import Literal


MatchStatus = Literal["matched", "unmatched", "ambiguous"]


def _normalize_reference(value: str | None) -> str:
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKC", value).strip().casefold()
    return re.sub(r"[^a-z0-9]", "", normalized)


def _validate_common(tenant_id: str, currency: str, occurred_at: datetime) -> None:
    if not tenant_id.strip():
        raise ValueError("tenant_id is required")
    if not re.fullmatch(r"[A-Z]{3}", currency):
        raise ValueError("currency must be a three-letter uppercase code")
    if occurred_at.tzinfo is None or occurred_at.utcoffset() is None:
        raise ValueError("occurred_at must be timezone-aware")


@dataclass(frozen=True, slots=True)
class SourceTransaction:
    """An immutable normalized transaction received from an external source."""

    transaction_id: str
    tenant_id: str
    reference: str | None
    amount: Decimal
    currency: str
    occurred_at: datetime

    def __post_init__(self) -> None:
        if not self.transaction_id.strip():
            raise ValueError("transaction_id is required")
        if not isinstance(self.amount, Decimal) or not self.amount.is_finite():
            raise ValueError("amount must be a finite Decimal")
        _validate_common(self.tenant_id, self.currency, self.occurred_at)


@dataclass(frozen=True, slots=True)
class LedgerEntry:
    """A normalized internal record to reconcile against a source transaction."""

    ledger_id: str
    tenant_id: str
    reference: str | None
    amount: Decimal
    currency: str
    occurred_at: datetime

    def __post_init__(self) -> None:
        if not self.ledger_id.strip():
            raise ValueError("ledger_id is required")
        if not isinstance(self.amount, Decimal) or not self.amount.is_finite():
            raise ValueError("amount must be a finite Decimal")
        _validate_common(self.tenant_id, self.currency, self.occurred_at)


@dataclass(frozen=True, slots=True)
class MatchResult:
    source_transaction_id: str
    status: MatchStatus
    ledger_entry_id: str | None
    candidate_ledger_ids: tuple[str, ...]
    reason: str


def reconcile(
    source_transactions: Sequence[SourceTransaction],
    ledger_entries: Sequence[LedgerEntry],
    *,
    tolerance_seconds: int = 300,
) -> list[MatchResult]:
    """Match source transactions to ledger entries conservatively.

    A match requires the same tenant, currency, exact Decimal amount, a
    non-empty normalized reference, and a timestamp within the configured
    tolerance. A ledger entry can be consumed only once per run. Ambiguous
    candidates are never selected arbitrarily.

    Missing references are deliberately left unmatched; fuzzy matching should
    be a separate, explainable review workflow rather than an implicit rule.
    """
    if tolerance_seconds < 0:
        raise ValueError("tolerance_seconds must be non-negative")

    ledger_by_key: dict[tuple[str, str, Decimal, str], list[LedgerEntry]] = {}
    for entry in ledger_entries:
        reference = _normalize_reference(entry.reference)
        if not reference:
            continue
        key = (entry.tenant_id, entry.currency, entry.amount, reference)
        ledger_by_key.setdefault(key, []).append(entry)

    consumed: set[str] = set()
    results: list[MatchResult] = []

    for source in source_transactions:
        reference = _normalize_reference(source.reference)
        if not reference:
            results.append(MatchResult(
                source_transaction_id=source.transaction_id,
                status="unmatched",
                ledger_entry_id=None,
                candidate_ledger_ids=(),
                reason="missing_source_reference",
            ))
            continue

        key = (source.tenant_id, source.currency, source.amount, reference)
        candidates = [
            entry for entry in ledger_by_key.get(key, [])
            if entry.ledger_id not in consumed
            and abs((source.occurred_at - entry.occurred_at).total_seconds())
            <= tolerance_seconds
        ]

        if len(candidates) == 1:
            entry = candidates[0]
            consumed.add(entry.ledger_id)
            results.append(MatchResult(
                source_transaction_id=source.transaction_id,
                status="matched",
                ledger_entry_id=entry.ledger_id,
                candidate_ledger_ids=(entry.ledger_id,),
                reason="exact_reference_amount_currency_and_time",
            ))
        elif len(candidates) > 1:
            results.append(MatchResult(
                source_transaction_id=source.transaction_id,
                status="ambiguous",
                ledger_entry_id=None,
                candidate_ledger_ids=tuple(sorted(e.ledger_id for e in candidates)),
                reason="multiple_valid_candidates",
            ))
        else:
            results.append(MatchResult(
                source_transaction_id=source.transaction_id,
                status="unmatched",
                ledger_entry_id=None,
                candidate_ledger_ids=(),
                reason="no_candidate_met_matching_rules",
            ))

    return results
