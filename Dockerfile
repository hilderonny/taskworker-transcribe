FROM nvidia/cuda:12.8.0-cudnn-runtime-ubuntu24.04

# Install latest python and pip
RUN apt update && apt install -y --no-install-recommends \
    python3 \
    python3-pip && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*
    
# Install dependencies
RUN pip install --break-system-packages --no-cache-dir faster-whisper

# Set the working directory
WORKDIR /app

# Copy the application code
COPY ./transcribe.py /app/transcribe.py

# Set the entrypoint
ENTRYPOINT ["python3", "transcribe.py"]