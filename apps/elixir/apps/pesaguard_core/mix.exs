defmodule PesaGuardCore.MixProject do
  use Mix.Project
  def project, do: [app: :pesaguard_core, version: "0.1.0", elixir: "~> 1.17", deps: deps()]
  def application, do: [extra_applications: [:logger, :crypto]]
  defp deps, do: [{:ecto_sql, "~> 3.12"}, {:postgrex, ">= 0.0.0"}, {:jason, "~> 1.4"}]
end
