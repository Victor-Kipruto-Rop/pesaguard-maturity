"""Explicit transaction lifecycle rules for the reconciliation domain.

This is a pure state machine. The persistence layer must apply transitions with
optimistic concurrency or a row lock and append an audit event in the same
database transaction.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class TransactionState(StrEnum):
    RECEIVED = "received"
    VALIDATED = "validated"
    RECONCILIATION_PENDING = "reconciliation_pending"
    MATCHED = "matched"
    UNMATCHED = "unmatched"
    AMBIGUOUS = "ambiguous"
    FAILED = "failed"
    REJECTED = "rejected"


_ALLOWED: dict[TransactionState, frozenset[TransactionState]] = {
    TransactionState.RECEIVED: frozenset({
        TransactionState.VALIDATED,
        TransactionState.REJECTED,
    }),
    TransactionState.VALIDATED: frozenset({
        TransactionState.RECONCILIATION_PENDING,
        TransactionState.REJECTED,
    }),
    TransactionState.RECONCILIATION_PENDING: frozenset({
        TransactionState.MATCHED,
        TransactionState.UNMATCHED,
        TransactionState.AMBIGUOUS,
        TransactionState.FAILED,
    }),
    TransactionState.UNMATCHED: frozenset({TransactionState.RECONCILIATION_PENDING}),
    TransactionState.AMBIGUOUS: frozenset({TransactionState.RECONCILIATION_PENDING}),
    TransactionState.FAILED: frozenset({TransactionState.RECONCILIATION_PENDING}),
    # A matched record is not silently reopened. Corrections require a separate
    # auditable correction/reconciliation-run event.
    TransactionState.MATCHED: frozenset(),
    TransactionState.REJECTED: frozenset(),
}


@dataclass(frozen=True, slots=True)
class StateTransition:
    previous: TransactionState
    current: TransactionState
    actor_id: str
    reason: str | None


class InvalidTransition(ValueError):
    """Raised when a transaction lifecycle transition is not permitted."""


def transition(
    current: TransactionState,
    target: TransactionState,
    *,
    actor_id: str,
    reason: str | None = None,
) -> StateTransition:
    """Validate and describe a state change without mutating persisted data."""
    if not actor_id.strip():
        raise InvalidTransition("actor_id is required for an auditable transition")
    if target not in _ALLOWED[current]:
        raise InvalidTransition(f"transition not allowed: {current.value} -> {target.value}")
    if target in {
        TransactionState.REJECTED,
        TransactionState.RECONCILIATION_PENDING,
    } and current in {
        TransactionState.UNMATCHED,
        TransactionState.AMBIGUOUS,
        TransactionState.FAILED,
    } and not (reason and reason.strip()):
        raise InvalidTransition("a reason is required when retrying or rerunning a transaction")
    if target == TransactionState.REJECTED and not (reason and reason.strip()):
        raise InvalidTransition("a reason is required when rejecting a transaction")
    return StateTransition(current, target, actor_id.strip(), reason.strip() if reason else None)
