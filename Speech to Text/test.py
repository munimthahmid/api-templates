import os
import io
from pydub import AudioSegment
from google.cloud import speech

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "speech_to_text.json"

def convert_to_mono(file_path):
    """Converts stereo WAV files to mono."""
    sound = AudioSegment.from_file(file_path)
    sound = sound.set_channels(1)  # Set to mono
    mono_file_path = "mono_" + file_path
    sound.export(mono_file_path, format="wav")
    return mono_file_path

def generate_text(input_file):
    """Processes the audio file and generates text."""
    client = speech.SpeechClient()

    with io.open(input_file, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )

    response = client.recognize(request={"config": config, "audio": audio})

    for result in response.results:
        print("Text to Speech Output: {}".format(result.alternatives[0].transcript))

# Process all WAV files in the directory
for file in os.listdir():
    if file.endswith(".wav"):
        mono_file = convert_to_mono(file)  # Convert to mono
        generate_text(mono_file)          # Process the mono file
