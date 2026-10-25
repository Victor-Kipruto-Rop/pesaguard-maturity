defmodule PesaGuardWeb.Application do
  use Application

  @impl true
  def start(_type, _args) do
    children = [PesaGuardWeb.Endpoint]
    Supervisor.start_link(children, strategy: :one_for_one, name: PesaGuardWeb.Supervisor)
  end

  @impl true
  def config_change(changed, _new, removed) do
    PesaGuardWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
