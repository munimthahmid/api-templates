# file: transcribe_streaming.py
import os

import sys
import queue
import pyaudio
from google.cloud import speech

# Audio recording parameters
RATE = 16000       # Sample rate
CHUNK = int(RATE / 10)  # 100ms frames

class MicrophoneStream(object):
    """
    Opens a recording stream as a generator yielding the audio chunks.
    """
    def __init__(self, rate=RATE, chunk=CHUNK):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,   # 16-bit resolution
            channels=1,              # Single channel (mono)
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """
        This is called by PyAudio for each audio chunk.
        """
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """
        Generator that yields audio chunks from the buffer.
        """
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Read until there's no more data
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

def listen_print_loop(responses):
    """
    Iterates through server responses and prints them.
    The responses passed is a generator that will block until a response is provided by the server.
    """
    for response in responses:
        if not response.results:
            continue

        # Since we are streaming, here we only care about the
        # first result being recognized.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative
        transcript = result.alternatives[0].transcript
        # The is_final result indicates the end of a spoken phrase.
        if result.is_final:
            sys.stdout.write("Final transcript: {}\n".format(transcript))
        else:
            # Intermediate transcript
            sys.stdout.write("Intermediate transcript: {}\r".format(transcript))
        sys.stdout.flush()


def main():
    # If you prefer to set the credentials here instead of environment variable:
    # import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "speech_to_text.json"

    client = speech.SpeechClient()

    # Configure the recognition
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
        enable_automatic_punctuation=True
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True  # Set to True to get partial (interim) results
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, block and process the server responses
        listen_print_loop(responses)


if __name__ == "__main__":
    print("Start speaking. Press CTRL+C to stop.")
    main()
