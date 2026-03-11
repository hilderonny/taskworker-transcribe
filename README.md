# taskworker-transcribe

[TaskBridge](https://github.com/hilderonny/taskbridge)-Worker zur Transkription von Mediendateien (Aufgabentyp `transcribe`). Das Programm basiert auf [faster-whisper](https://github.com/SYSTRAN/faster-whisper).

## Ergebnisformat

Das `result`, welches an die TaskBridge gesendet wird, hat folgendes Format:

```json
{
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
  "version" : "1.1.1",
  "library" : "faster-whisper-1.2.1",
  "model" : "large-v2"
}
```

|Attribut|Beschreibung|
|---|---|
|`language`|Anhand der ersten 10 Sekunden erkannte Sprache als zweistelliger ISO code|
|`texts`|Liste erkannter Textabschnitte. Die Trennung erfolgt anhand von tonlosen Stellen, oftmals Sätze.|
|`texts.start`|Startzeitpunkt innerhalb der Datei in Millisekunden|
|`texts.end`|Endzeitpunkt in Millisekunden|
|`texts.text`|Text in Originalsprache|
|`device`|Gerät, auf dem die Transkription durchgeführt wurde. `cuda` for NVIDIA-grafikkarte, `cpu` für normale CPU|
|`duration`|Gesamtdauer der Verarbeitung in Sekunden|
|`repository`|Herkunft des Workers|
|`version`|Version des Workers|
|`library`|Bibliothek, mit welcher die Transkription erfolgte|
|`model`|KI-Modell, welches für die Transkription verwendet wurde|

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
pip install faster-whisper==0.9.0
```

## Running

Running the program the first time, ai models with about 4 GB (depending on the used model) get downloaded automatically.

```sh
python transcribe.py --taskbridgeurl http://192.168.178.39:42000/ --device cuda --worker ROG --model large-v2
```

Das Programm ist als Docker-Container konzipiert. Es werden je nach KI-Modell verschiedene Container-Tags bereitgestellt. Die brauchbarsten multilingualen Ergebnisse liefert das Modell (Tag) `large-v2`, welches auf einer GPU mit 6GB VRAM gut läuft. Aufgrund der Kapselung der GPU-Treiber und KI-Modelle sind die Docker-Images zwischen **17 GB und 23 GB** groß.

- Docker installieren
- Image herunterladen, mögliche Tags sind `tiny` und `large-v2`

```sh
docker pull hilderonny2024/taskworker-transcribe:large-v2
```

- Container starten

```sh
docker run --name DOCKER-TRANSCRIBE-LARGE-V2 --gpus all -e taskbridgeurl=http://192.168.0.153:42000/ -e worker=DOCKER-TRANSCRIBE-LARGE-V2 hilderonny2024/taskworker-transcribe:large-v2
```

|Parameter|Beschreibung|
|---|---|
| `--name DOCKER-TRANSCRIBE-LARGE-V2`|Name des Containers zur Anzeige in Docker Desktop|
|`--gpus all`|Stellt dem Container alle Grafikkarten zur Verfügung|
|`-e taskbridgeurl=http://192.168.0.153:42000/`|URL der TaskBridge. `localhost` oder `127.0.0.1` geht nicht, auch wenn der Container auf demselben Host wie die TaskBridge läuft|
|`-e worker=DOCKER-TRANSCRIBE-LARGE-V2`|Name des Workers, wie er in der Worker-Liste in der TaskBridge angezeigt wird|

## Literature

1. https://github.com/SYSTRAN/faster-whisper