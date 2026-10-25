FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml ./pyproject.toml
COPY src ./src
RUN pip install --no-cache-dir .
USER 10001:10001
EXPOSE 8080
CMD ["uvicorn", "pesaguard_reconciliation.app:app", "--host", "0.0.0.0", "--port", "8080"]
