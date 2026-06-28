# 1. Update to match your working local runtime (Python 3.14)
FROM python:3.14-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV EXIFTOOL_PATH=/usr/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg

# 2. Keep the media engines needed for audio/metadata processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    exiftool \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Copy dependencies list and install them natively
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your local repository structures into the container
COPY packages/ ./packages/
COPY app.py .

# 5. Install your modified local markitdown safely without breaking on 3.14 constraints
RUN pip install -e packages/markitdown --no-deps

# 6. Expose the standard communication port for Render web services
EXPOSE 8000

# 7. Change the Entrypoint/CMD to start your FastAPI server instead of the CLI tool
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]