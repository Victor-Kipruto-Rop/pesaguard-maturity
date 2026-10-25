# Integration Configuration (Elixir)
P1 owns tenant-facing Daraja configuration metadata, callback URL setup and connection status. Store credential values in a secrets manager and only keep references/metadata in the application database. Keep sandbox and production configurations separate; never show a connection as verified without an actual successful check.
