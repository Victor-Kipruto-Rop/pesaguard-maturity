defmodule PesaGuardWeb.HealthController do
  use Phoenix.Controller, formats: [:json]

  def index(conn, _params) do
    json(conn, %{service: "pesaguard-web", status: "scaffold"})
  end

  def live(conn, _params) do
    json(conn, %{status: "ok"})
  end
end
