# taskworker-transcribe

Worker for taskbridge which can handle tasks of type `transcribe`.

## Task format

```json
{
    ...
    "type" : "transcribe",
    "worker" : "ROG",
    "file" : "123456789",
    ...
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

The `type` must be `transcribe`.

`worker` contains the unique name of the worker which processed the task.

The worker expects a `file` property defining the filename which contains the audio to transcribe.

When the worker finishes the task, it sends back a `result` property. This property is an object. It contains an array `texts` with the transcribed audio broken into chunks. Each of the elements has the properties `start` and `end` defining at which second in the audio the text chunk started and ended. The result also contains the detected `language`'s 2 digit ISO code.

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
sudo apt install -y git python3.11-env ocl-icd-libopencl1 nvidia-cuda-toolkit nvidia-utils-510-server nvidia-utils-535-server
python3.11 -m venv python-venv
source python-venv/bin/activate
pip install faster-whisper==0.9.0 nvidia_cublas_cu11==11.11.3.6 nvidia_cudnn_cu11==9.4.0.58
```

Adopt the shell script `translate.sh`to your needs and create SystemD config files (if you want tu run the worker as Linux service).

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