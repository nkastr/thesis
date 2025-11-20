FROM python:3.9.7-slim
RUN mkdir -p /comm-aware-sc/src
WORKDIR /comm-aware-sc/src
COPY requirements.txt /comm-aware-sc/src
RUN pip install -r requirements.txt
COPY . /comm-aware-sc/src/
CMD ["taskset", "-a", "-c", "0,1", "python3", "scheduler.py"]
