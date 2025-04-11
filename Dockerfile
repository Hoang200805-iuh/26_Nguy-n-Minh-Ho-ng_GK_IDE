# Dockerfile - dùng cho app Python chạy crawl/transform/save

FROM python:3.10-slim

# Cài các thư viện cần thiết
WORKDIR /app

# Copy mã nguồn và requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/

CMD ["python", "src/dag/cat_pipeline_dag.py"]
