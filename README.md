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
            "Line 1",
            "",
            "Line 3"
        ],
        "device" : "cuda",
        "duration" : 12,
        "repository" : "https://github.com/hilderonny/taskworker-transcribe",
        "version" : "1.0.0",
        "library" : "fasterwhisper-0.8.15",
        "model" : "large-v2"
    }
}
```

The `type` must be `transcribe`.

`worker` contains the unique name of the worker which processed the task.

The worker expects a `file` property defining the filename which contains the audio to transcribe.

When the worker finishes the task, it sends back a `result` property. This property is an object. It contains an array `texts` with the transcribed audio broken into chunks. The result also contains the detected `language`'s 2 digit ISO code.

## Installation

Currently this worker only works with Nvidia GPUs (no CPU).
First install Python 3.12. The run the following commands in the folder of the downloaded repository.

```
python -m venv python-venv
python-venv/Scripts/activate
pip install faster-whisper==0.9.0
pip install --force-reinstall ctranslate2==3.24.0
```


cudnn_ops_infer64_8.dll
cudnn_cnn_infer64_8.dll
zlibwapi.dll
cublasLt64_11.dll
cublas64_11.dll

https://developer.nvidia.com/rdp/cudnn-archive#a-collapse811-111

https://developer.nvidia.com/cudnn-downloads

Download and install the CUDA Toolkit from https://developer.nvidia.com/cuda-downloads.

Next you need to copy `cudnn_ops_infer64_8.dll`, `cudnn_cnn_infer64_8.dll`, `cublas64_11.dll`, `cublasLt64_11.dll` and `zlibwapi.dll` (Can be found in subdirectory `dll`) into the directory `python-venv/Lib/site-packages/ctranslate2`.

## Running

Running the program the first time, ai models with about 4 GB (depending on the used model) get downloaded automatically.

```sh
python transcribe.py --taskbridgeurl http://192.168.178.39:42000/ --worker ROG --model large-v2
```

## Literature

1. https://github.com/SYSTRAN/faster-whisper

