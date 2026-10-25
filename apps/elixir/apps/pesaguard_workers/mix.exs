defmodule PesaGuardWorkers.MixProject do
  use Mix.Project
  def project, do: [app: :pesaguard_workers, version: "0.1.0", elixir: "~> 1.17", deps: deps()]
  def application, do: [extra_applications: [:logger]]
  defp deps, do: [{:oban, "~> 2.19"}, {:pesaguard_core, in_umbrella: true}]
end
