defmodule PesaGuardWeb.Router do
  use Phoenix.Router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", PesaGuardWeb do
    pipe_through :api
    get "/", HealthController, :index
    get "/health/live", HealthController, :live
  end
end
