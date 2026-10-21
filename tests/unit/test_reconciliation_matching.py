from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from pesaguard_core.matching import LedgerEntry, SourceTransaction, reconcile


NOW = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)


def source(
    transaction_id: str = "src-1",
    *,
    tenant: str = "tenant-a",
    reference: str | None = "MPESA-123",
    amount: str = "100.00",
    currency: str = "KES",
    at: datetime = NOW,
) -> SourceTransaction:
    return SourceTransaction(transaction_id, tenant, reference, Decimal(amount), currency, at)


def ledger(
    ledger_id: str = "led-1",
    *,
    tenant: str = "tenant-a",
    reference: str | None = "mpesa 123",
    amount: str = "100.00",
    currency: str = "KES",
    at: datetime = NOW,
) -> LedgerEntry:
    return LedgerEntry(ledger_id, tenant, reference, Decimal(amount), currency, at)


def test_matches_normalized_reference_and_exact_decimal_amount() -> None:
    result = reconcile([source()], [ledger()])
    assert result[0].status == "matched"
    assert result[0].ledger_entry_id == "led-1"


@pytest.mark.parametrize(
    ("source_record", "ledger_record"),
    [
        (source(tenant="tenant-a"), ledger(tenant="tenant-b")),
        (source(amount="100.00"), ledger(amount="100.01")),
        (source(currency="KES"), ledger(currency="USD")),
        (source(at=NOW), ledger(at=NOW + timedelta(minutes=10))),
    ],
)
def test_does_not_match_records_outside_rules(source_record, ledger_record) -> None:
    assert reconcile([source_record], [ledger_record])[0].status == "unmatched"


def test_ambiguous_candidates_are_not_selected_arbitrarily() -> None:
    result = reconcile([source()], [ledger("led-b"), ledger("led-a")])[0]
    assert result.status == "ambiguous"
    assert result.ledger_entry_id is None
    assert result.candidate_ledger_ids == ("led-a", "led-b")


def test_one_ledger_entry_cannot_match_two_source_records() -> None:
    results = reconcile([source("src-1"), source("src-2")], [ledger()])
    assert [r.status for r in results] == ["matched", "unmatched"]


def test_missing_reference_is_not_fuzzy_matched() -> None:
    result = reconcile([source(reference=None)], [ledger(reference=None)])[0]
    assert result.status == "unmatched"
    assert result.reason == "missing_source_reference"


def test_naive_datetimes_are_rejected() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        source(at=datetime(2026, 1, 1, 12, 0))


def test_float_amount_is_rejected() -> None:
    with pytest.raises(ValueError, match="Decimal"):
        SourceTransaction("src", "tenant-a", "ref", 100.0, "KES", NOW)  # type: ignore[arg-type]


def test_negative_tolerance_is_rejected() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        reconcile([], [], tolerance_seconds=-1)
