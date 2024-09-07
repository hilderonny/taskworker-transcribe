from importlib.metadata import version
import time
import json
import requests
import datetime
import argparse
import os

REPOSITORY = "https://github.com/hilderonny/taskworker-transcribe"
VERSION = "1.0.0"
LIBRARY = "faster-whisper-" + version("faster-whisper")
DEVICE = "cuda"
APIVERSION = "v2"
LOCAL_MODEL_PATH = "./models/faster-whisper"
LOCAL_FILE_PATH = "./temp"

print(f'Transcriber Version {VERSION}')

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--taskbridgeurl', type=str, action='store', required=True, help='Root URL of the API of the task bridge to use, e.g. https://taskbridge.ai/')
parser.add_argument('--model', type=str, action='store', help='Whisper model size to use. Can be "tiny", "base", "small", "medium", "large-v2" or "large-v3".')
parser.add_argument('--version', '-v', action='version', version=VERSION)
parser.add_argument('--worker', type=str, action='store', required=True, help='Unique name of this worker')
args = parser.parse_args()

WORKER = args.worker
print(f'Worker name: {WORKER}')
TASKBRIDGEURL = args.taskbridgeurl
if not TASKBRIDGEURL.endswith("/"):
    TASKBRIDGEURL = f"{TASKBRIDGEURL}/"
APIURL = f"{TASKBRIDGEURL}api/{APIVERSION}/"
print(f'Using API URL {APIURL}')

MODEL = args.model
print(f'Using whisper model {MODEL}')

# Prepare temp path
os.makedirs(LOCAL_FILE_PATH, exist_ok=True)

# Load AI
from faster_whisper import WhisperModel    
compute_type = 'float16' # if USEGPU else 'int8'
#device = 'cuda' # if USEGPU else 'cpu'
whisper_model = WhisperModel( model_size_or_path = MODEL, device = DEVICE, local_files_only = False, compute_type = compute_type, download_root = LOCAL_MODEL_PATH )

def process_file(file_path):
    start_time = datetime.datetime.now()
    result = {}
    try:
        print("Processing file " + file_path)
        print("Transcribing")
        transcribe_segments_generator, transcribe_info = whisper_model.transcribe(file_path, task = "transcribe")
        transcribe_segments = list(map(lambda segment: { "start": segment.start, "end": segment.end, "text": segment.text.strip() }, transcribe_segments_generator))
        original_language = transcribe_info.language
        result["language"] = original_language
        result["texts"] = transcribe_segments
    except Exception as ex:
        print(ex)
    end_time = datetime.datetime.now()
    result["duration"] = (end_time - start_time).total_seconds()
    return result

def check_and_process():
    start_time = datetime.datetime.now()
    take_request = {}
    take_request["type"] = "transcribe"
    take_request["worker"] = WORKER
    response = requests.post(f"{APIURL}tasks/take/", json=take_request)
    print(response)
    if response.status_code != 200:
        return False
    task = response.json()
    taskid = task["id"]
    print(json.dumps(task, indent=2))

    file_response = requests.get(f"{APIURL}tasks/file/{taskid}")
    print(file_response)
    local_file_path = os.path.join(LOCAL_FILE_PATH, taskid)
    with open(local_file_path, 'wb') as file:
        file.write(file_response.content)

    result_to_report = {}
    result_to_report["result"] = process_file(local_file_path)
    end_time = datetime.datetime.now()
    result_to_report["result"]["device"] = DEVICE
    result_to_report["result"]["duration"] = (end_time - start_time).total_seconds()
    result_to_report["result"]["repository"] = REPOSITORY
    result_to_report["result"]["version"] = VERSION
    result_to_report["result"]["library"] = LIBRARY
    result_to_report["result"]["model"] = MODEL
    print(json.dumps(result_to_report, indent=2))
    print("Reporting result")
    requests.post(f"{APIURL}tasks/complete/{taskid}/", json=result_to_report)
    print("Done")
    return True

try:
    print('Ready and waiting for action')
    while True:
        task_was_processed = False
        try:
            task_was_processed = check_and_process()
        except Exception as ex:
            print(ex)
        if task_was_processed == False:
            time.sleep(3)
except Exception:
    pass
