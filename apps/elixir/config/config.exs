import Config
config :logger, :default_formatter, format: "$time $metadata[$level] $message\n", metadata: [:request_id, :correlation_id]
