import Config
# Load secrets from a runtime secret manager. Fail startup if mandatory production settings are absent.
if config_env() == :prod do
  # Add validated production configuration after Phoenix app generation.
end
