import Config
config :logger, :default_formatter, format: "$time $metadata[$level] $message\n", metadata: [:request_id, :correlation_id]

config :pesaguard_web, PesaGuardWeb.Endpoint,
  url: [host: "localhost"],
  http: [ip: {127, 0, 0, 1}, port: String.to_integer(System.get_env("PORT", "4000"))],
  server: config_env() == :dev,
  secret_key_base: String.duplicate("local-development-only-secret-", 3)
