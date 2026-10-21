import pytest
from pydantic import ValidationError

from app.config.settings import Settings


def production_settings(**overrides) -> Settings:
    values = {
        "environment": "production",
        "debug": False,
        "database_url": "postgresql+psycopg://user:password@db.example.invalid/pesaguard",
        "secret_key": "production-secret-material-at-least-32-bytes",
        "jwt_algorithm": "HS256",
        "jwt_issuer": "pesaguard-auth",
        "jwt_audience": "pesaguard-api",
        "trusted_hosts": ["api.pesaguard.co.ke"],
        "cors_origins": ["https://app.pesaguard.co.ke"],
    }
    values.update(overrides)
    return Settings(**values)


def test_accepts_explicit_production_configuration() -> None:
    settings = production_settings()
    assert settings.environment == "production"
    assert settings.debug is False
    assert settings.trusted_hosts == ["api.pesaguard.co.ke"]


@pytest.mark.parametrize(
    "overrides",
    [
        {"database_url": "sqlite:///./production.db"},
        {"secret_key": "short"},
        {"secret_key": "development-only-do-not-use-this-secret"},
        {"trusted_hosts": ["*"]},
        {"cors_origins": ["*"]},
        {"debug": True},
        {"jwt_issuer": ""},
        {"jwt_audience": ""},
    ],
)
def test_rejects_insecure_production_configuration(overrides: dict) -> None:
    with pytest.raises(ValidationError):
        production_settings(**overrides)


def test_rejects_unsupported_jwt_algorithm() -> None:
    with pytest.raises(ValidationError, match="HS256 only"):
        production_settings(jwt_algorithm="none")


def test_token_lifetimes_have_safe_bounds() -> None:
    with pytest.raises(ValidationError):
        Settings(access_token_ttl_minutes=0)
    with pytest.raises(ValidationError):
        Settings(refresh_token_ttl_days=31)
