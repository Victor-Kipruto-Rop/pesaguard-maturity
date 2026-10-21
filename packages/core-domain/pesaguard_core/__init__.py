"""PesaGuard framework-independent core domain primitives."""

from .matching import LedgerEntry, MatchResult, SourceTransaction, reconcile

__all__ = ["LedgerEntry", "MatchResult", "SourceTransaction", "reconcile"]
