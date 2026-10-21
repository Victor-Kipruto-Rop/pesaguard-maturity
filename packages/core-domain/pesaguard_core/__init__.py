"""PesaGuard framework-independent core domain primitives."""

from .csv_import import (
    ImportIssue,
    ImportedStatementRow,
    StatementColumnMap,
    StatementImportResult,
    parse_statement_csv,
)
from .matching import LedgerEntry, MatchResult, SourceTransaction, reconcile
from .transaction_state import InvalidTransition, StateTransition, TransactionState, transition

__all__ = [
    "InvalidTransition",
    "ImportIssue",
    "ImportedStatementRow",
    "LedgerEntry",
    "MatchResult",
    "SourceTransaction",
    "StateTransition",
    "StatementColumnMap",
    "StatementImportResult",
    "TransactionState",
    "parse_statement_csv",
    "reconcile",
    "transition",
]
