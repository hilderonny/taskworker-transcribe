FROM ubuntu:22.04

ENV PYTHONDONTWRITEBYTECODE=1

RUN apt update
RUN apt install -y python3.11 python3-pip
RUN apt install -y nvidia-cuda-toolkit nvidia-utils-510-server nvidia-utils-535-server
RUN apt install -y ocl-icd-libopencl1

RUN rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir faster-whisper==0.9.0 nvidia_cublas_cu11==11.11.3.6 nvidia_cudnn_cu11==9.4.0.58

WORKDIR /app

ENV taskbridgeurl=http://127.0.0.1:42000/
ENV worker=DOCKER
ENV model=large-v2
ENV device=cuda

COPY transcribe.py /app

CMD [ "sh" , "-c", "python3 -u transcribe.py --taskbridgeurl ${taskbridgeurl} --worker ${worker} --device ${device} --model ${model}" ]

# Building
# docker build -t hilderonny2024/taskworker-transcribe .

# First time run to enable GPUs
# docker run --gpus all -e taskbridgeurl=http://127.0.0.1:42000/ -e worker=DOCKER -e model=large-v2 hilderonny2024/taskworker-transcribe

# Publishing
# docker login
# docker push hilderonny2024/taskworker-transcribe