# taskworker-transcribe

Worker for taskbridge which can handle tasks of type `transcribe`.

## Result format

When calling the TaskBridge `/api/tasks/complete/:id` API, the following JSON structure is sent to the endpoint.

```json
{
  "result" : {
    "language" : "en",
    "texts" : [
      {
        "start" : 0.0,
        "end" : 1.0,
        "text" : "Line 1"
      },
      {
        "start" : 1.0,
        "end" : 2.0,
        "text" : "Line 2"
      }
    ],
    "device" : "cuda",
    "duration" : 12,
    "repository" : "https://github.com/hilderonny/taskworker-transcribe",
    "version" : "1.1.0",
    "library" : "fasterwhisper-0.8.15",
    "model" : "large-v2"
  }
}
```

|Property|Description|
|---|---|
|`language`|Detected langugage in the file depending on the first seconds as 2 digit ISO code|
|`texts`|Array of detected text chunks. Normally the text is splitted by sentences|
|`texts.start`|Start second of the chunk|
|`texts.end`|End second of the chunk|
|`texts.text`|Text content of the chunk|
|`device`|`cuda` for GPU processing and `cpu` for CPU processing |
|`duration`|Time in seconds for the processing|
|`repository`|Source code repository of the worker|
|`version`|Version of the worker|
|`library`|Library used to perform transcription|
|`model`|AI model used for transcription|

## Running with docker (recommended)

First install Docker Desktop with WSL2 support.
After that install the latest GPU driver for your video card if you want GPU support.

Next run this command and adopt the parameters to your needs.

https://docs.docker.com/desktop/features/gpu/

```sh
docker run --gpus=all --name taskworker-translate_ROG_LARGE_V2 hilderonny2014/taskworker-transcribe:latest --taskbridgeurl http://192.168.0.2:42000/ --worker ROG_LARGE_V2 --device cuda --model large-v2
```

On the first run the container needs an internet connection to download the
model (up to 5 GB depending on the model). While downloading the container
has no output. This can take up some minutes depending on the model but is
normal.

The order of the parameters is important!

|Parameter|Description|
|---|---|
|`--name`|Name the docker container should get while running|
|`--taskbridgeurl`|The URL of the TaskBridge to use. When the worker is running on the same machine as the TaskBridge, make sure to use the official IP of the host and not 127.0.0.1!|
|`--worker`|Name of the worker to be shown to the TaskBridge|
|`--device`|`cuda` for using the GPU, `cpu` otherwise|
|`--model`|Whisper model to use. Can be one of `tiny`, `base`, `small`, `medium`, `large`, `large-v2` (recommended), `large-v3`, `distil-large-v3`|

|Model|Size|GPU RAM requirement|Remarks|
|---|---|---|---|
|tiny|72 MB|400 MB|Not useful for languages other than english|
|base|139 MB|400 MB||
|small|462 MB|900 MB||
|medium|1.4 GB|2.8 GB||
|large-v2|2.9 GB|4.2 GB|Best quality for multiple languages|
|large-v3|2.9 GB|4.9 GB|Inaccurate|
|distil-large-v3|1.4 GB|1.8 GB|Currently only supports english|

## Installation on Windows

First install Python 3.11.
Currently I cannot get the actual faster-whisper 1.0.3 implementation to work with CUDA 12.
So I need to use version 0.9.0 which is installable only with Python 3.11.
Then run the following commands in the folder of the downloaded repository.

```
python3.11 -m venv python-venv
python-venv\Scripts\activate
pip install faster-whisper==0.9.0
```

Next you need to copy `cudnn_ops_infer64_8.dll`, `cudnn_cnn_infer64_8.dll`, `cublas64_11.dll`, `cublasLt64_11.dll` and `zlibwapi.dll` (Can be found on NVIDIA websites) into the directory `python-venv/Lib/site-packages/ctranslate2`.

## Installation as service under Linux

```
sudo ubuntu-drivers --gpgpu install nvidia:535-server
sudo apt install -y git python3.11-venv ocl-icd-libopencl1 nvidia-cuda-toolkit nvidia-utils-535-server
python3.11 -m venv python-venv
source python-venv/bin/activate
pip install nvidia-cublas-cu12==12.8.3.14 nvidia-cudnn-cu12==9.7.1.26 faster-whisper
```

Adopt the shell script `translate.sh` to your needs and create SystemD config files (if you want tu run the worker as Linux service).

**/etc/systemd/system/taskworker-transcribe.service**:

```
[Unit]
Description=Task Worker - Audio Transcriber

[Service]
ExecStart=/taskworker-transcribe/transcribe.sh
Restart=always
User=user
WorkingDirectory=/taskworker-transcribe/

[Install]
WantedBy=multi-user.target
```

Finally register and start the services.

```
chmod +x ./transcribe.sh
sudo systemctl daemon-reload
sudo systemctl enable taskworker-transcribe.service
sudo systemctl start taskworker-transcribe.service
```

## Running

Running the program the first time, ai models with about 4 GB (depending on the used model) get downloaded automatically.

```sh
python transcribe.py --taskbridgeurl http://192.168.178.39:42000/ --device cuda --worker ROG --model large-v2
```

## Literature

1. https://github.com/SYSTRAN/faster-whisper
