defmodule PesaGuardShared.MixProject do
  use Mix.Project
  def project, do: [app: :pesaguard_shared, version: "0.1.0", elixir: "~> 1.17", deps: []]
  def application, do: [extra_applications: [:logger, :crypto]]
end
