FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY all.py ./
COPY src ./src
COPY all_charts.html ./

CMD ["sleep", "infinity"]
