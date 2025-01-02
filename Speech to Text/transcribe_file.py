# file: transcribe_file.py

import os
from google.cloud import speech

def transcribe_file(speech_file):
    """
    Transcribe an audio file (e.g. WAV) using the Google Cloud Speech-to-Text API.
    This version is configured for stereo, 44.1 kHz audio.
    """
    # Optionally, set the path to your JSON credentials here.
    # If you prefer the environment variable approach, make sure you have:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/speech_to_text.json"
    #
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "speech_to_text.json"

    client = speech.SpeechClient()

    # Read the file
    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    # IMPORTANT: Match these values to the audio file’s format.
    # If your file is actually mono or uses a different sample rate,
    # update these accordingly. Or omit 'sample_rate_hertz' so it's auto-detected.
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,              # Match WAV header
        language_code="en-US",
        enable_automatic_punctuation=True,
        audio_channel_count=2,                # Match 2 channels (stereo)
        enable_separate_recognition_per_channel=False  
        # If you want separate transcripts for each channel, set True here
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        # Each result contains several alternatives - we print the most likely
        transcript = result.alternatives[0].transcript
        print("Transcript: ", transcript)


if __name__ == "__main__":
    # Replace with the path to your audio file
    audio_file_path = "sample.wav"
    transcribe_file(audio_file_path)
