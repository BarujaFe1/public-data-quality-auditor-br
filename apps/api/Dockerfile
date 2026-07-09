FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PYTHONPATH=/app
ENV PROJECT_ROOT=/workspace
ENV DEMO_DIR=/workspace/data/demo
ENV AUDIT_OUTPUT_DIR=/workspace/data/audit_outputs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
