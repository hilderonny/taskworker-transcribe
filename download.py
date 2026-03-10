import argparse

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, action='store')
args = parser.parse_args()

MODEL = args.model

print(f'Downloading whisper model {MODEL}')

from faster_whisper import WhisperModel    
whisper_model = WhisperModel( model_size_or_path = MODEL, device = "cpu", local_files_only = False, download_root = "./models/faster-whisper" )
