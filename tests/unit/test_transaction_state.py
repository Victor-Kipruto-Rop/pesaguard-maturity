import pytest

from pesaguard_core.transaction_state import (
    InvalidTransition,
    TransactionState as State,
    transition,
)


def test_valid_ingestion_to_reconciliation_path() -> None:
    assert transition(State.RECEIVED, State.VALIDATED, actor_id="ingestion-worker").current == State.VALIDATED
    assert transition(State.VALIDATED, State.RECONCILIATION_PENDING, actor_id="worker").current == State.RECONCILIATION_PENDING
    assert transition(State.RECONCILIATION_PENDING, State.MATCHED, actor_id="reconciler").current == State.MATCHED


@pytest.mark.parametrize("terminal", [State.MATCHED, State.REJECTED])
def test_terminal_state_cannot_be_reopened(terminal: State) -> None:
    with pytest.raises(InvalidTransition):
        transition(terminal, State.RECONCILIATION_PENDING, actor_id="operator", reason="retry")


def test_unmatched_transaction_requires_reason_to_rerun() -> None:
    with pytest.raises(InvalidTransition, match="reason is required"):
        transition(State.UNMATCHED, State.RECONCILIATION_PENDING, actor_id="operator")


def test_rerun_requires_actor_and_reason() -> None:
    result = transition(
        State.UNMATCHED,
        State.RECONCILIATION_PENDING,
        actor_id="operator-1",
        reason="new ledger data imported",
    )
    assert result.previous == State.UNMATCHED
    assert result.current == State.RECONCILIATION_PENDING
    assert result.reason == "new ledger data imported"


def test_rejection_requires_reason() -> None:
    with pytest.raises(InvalidTransition, match="reason is required"):
        transition(State.RECEIVED, State.REJECTED, actor_id="validator")


def test_actor_is_required() -> None:
    with pytest.raises(InvalidTransition, match="actor_id is required"):
        transition(State.RECEIVED, State.VALIDATED, actor_id=" ")
