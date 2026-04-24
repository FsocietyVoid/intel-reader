FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure the data directory exists inside the container
RUN mkdir -p /data

EXPOSE 8501

# Default command will be overridden in docker-compose.yml
CMD streamlit run app.py --server.port 8501 --server.address 0.0.0.0