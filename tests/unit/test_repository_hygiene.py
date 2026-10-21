from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_local_environment_files_are_ignored() -> None:
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for rule in (".env", "*.env", ".venv/", "*.db"):
        assert rule in ignore


def test_replacement_acceptance_gates_are_documented() -> None:
    acceptance = ROOT / "docs" / "operations" / "PRODUCTION_ACCEPTANCE.md"
    assert acceptance.is_file()
    text = acceptance.read_text(encoding="utf-8")
    assert "one backend is authorized to write live financial events" in text
    assert "rollback" in text.lower()
