from fastapi import FastAPI

app = FastAPI(title="PesaGuard Data Quality Service", version="0.1.0")

@app.get("/health/live", tags=["health"])
def liveness() -> dict[str, str]:
    return {"status": "ok"}
