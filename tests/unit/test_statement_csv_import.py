from decimal import Decimal

from pesaguard_core.csv_import import parse_statement_csv


HEADER = b"reference,amount,currency,occurred_at\n"
VALID_ROW = b"MPESA-123,100.25,kes,2026-01-01T12:00:00Z\n"


def test_parses_valid_csv_with_decimal_and_timezone() -> None:
    result = parse_statement_csv(HEADER + VALID_ROW, tenant_id="tenant-a")
    assert result.accepted
    assert len(result.rows) == 1
    assert result.rows[0].amount == Decimal("100.25")
    assert result.rows[0].currency == "KES"
    assert result.rows[0].occurred_at.utcoffset().total_seconds() == 0


def test_rejects_entire_file_when_one_row_is_invalid() -> None:
    content = HEADER + VALID_ROW + b"MPESA-456,not-a-number,KES,2026-01-01T12:00:00Z\n"
    result = parse_statement_csv(content, tenant_id="tenant-a")
    assert not result.accepted
    assert result.rows == ()
    assert result.issues[0].code == "invalid_amount"


def test_rejects_duplicate_rows() -> None:
    result = parse_statement_csv(HEADER + VALID_ROW + VALID_ROW, tenant_id="tenant-a")
    assert not result.accepted
    assert result.rows == ()
    assert any(issue.code == "duplicate_row" for issue in result.issues)


def test_rejects_naive_timestamp() -> None:
    result = parse_statement_csv(
        HEADER + b"MPESA-123,100.25,KES,2026-01-01T12:00:00\n",
        tenant_id="tenant-a",
    )
    assert not result.accepted
    assert result.issues[0].code == "invalid_timestamp"


def test_rejects_missing_required_column() -> None:
    result = parse_statement_csv(
        b"reference,amount,currency\nMPESA-123,100.25,KES\n",
        tenant_id="tenant-a",
    )
    assert not result.accepted
    assert any(issue.code == "missing_column" for issue in result.issues)


def test_rejects_oversized_file() -> None:
    result = parse_statement_csv(HEADER + VALID_ROW, tenant_id="tenant-a", max_bytes=5)
    assert not result.accepted
    assert result.issues[0].code == "invalid_csv"


def test_requires_trusted_tenant_context() -> None:
    result = parse_statement_csv(HEADER + VALID_ROW, tenant_id=" ")
    assert not result.accepted
    assert result.rows == ()


def test_content_digest_is_stable() -> None:
    content = HEADER + VALID_ROW
    assert parse_statement_csv(content, tenant_id="tenant-a").content_sha256 == (
        parse_statement_csv(content, tenant_id="tenant-a").content_sha256
    )
