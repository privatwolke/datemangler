FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends ntfs-3g
COPY . /app
RUN pip install -e .
ENTRYPOINT ["python", "-m", "unittest"]