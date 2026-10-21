from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_local_environment_files_are_ignored() -> None:
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for rule in (".env", "*.env", "!.env.example", ".venv/", "*.db"):
        assert rule in ignore


def test_production_compose_file_is_not_empty_placeholder() -> None:
    path = ROOT / "docker-compose.prod.yml"
    if path.exists():
        assert path.stat().st_size > 0, "production compose file is an empty placeholder"
