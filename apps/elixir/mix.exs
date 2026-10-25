defmodule PesaGuardUmbrella.MixProject do
  use Mix.Project
  def project, do: [app: :pesaguard_umbrella, version: "0.1.0", apps_path: "apps", start_permanent: Mix.env() == :prod, deps: deps()]
  def application, do: [extra_applications: [:logger, :crypto]]
  defp deps, do: []
end
