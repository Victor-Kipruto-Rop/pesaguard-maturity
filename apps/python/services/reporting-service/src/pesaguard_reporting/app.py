from fastapi import FastAPI

app = FastAPI(title="PesaGuard Reporting Service", version="0.1.0")

@app.get("/health/live", tags=["health"])
def liveness() -> dict[str, str]:
    return {"status": "ok"}
