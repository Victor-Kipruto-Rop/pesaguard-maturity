defmodule PesaGuardWeb.RouterTest do
  use ExUnit.Case, async: true

  test "health endpoint returns a stable liveness payload" do
    conn = Plug.Test.conn(:get, "/health/live")
    conn = PesaGuardWeb.Router.call(conn, PesaGuardWeb.Router.init([]))
    assert conn.status == 200
  end
end
