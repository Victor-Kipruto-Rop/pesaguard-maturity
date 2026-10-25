defmodule PesaGuardWeb.MixProject do
  use Mix.Project
  def project, do: [app: :pesaguard_web, version: "0.1.0", elixir: "~> 1.17", deps: deps()]
  def application, do: [extra_applications: [:logger], mod: {PesaGuardWeb.Application, []}]
  defp deps, do: [{:phoenix, "~> 1.7"}, {:phoenix_live_view, "~> 1.0"}, {:plug_cowboy, "~> 2.7"}, {:jason, "~> 1.4"}, {:pesaguard_core, in_umbrella: true}]
end
