from google.cloud import translate_v2 as translate
import os

# Set the path to your Google Cloud credentials JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cloud-translation-api.json"

def translate_text(text, target_language="bn"):
    """
    Translates a given text into the target language using the Google Cloud Translation API (v2).
    :param text: The source text to translate.
    :param target_language: The language code to translate into (e.g., 'bn' for Bengali).
    :return: Translated text as a string.
    """
    # Initialize the translation client
    client = translate.Client()
    
    # Perform the translation
    result = client.translate(text, target_language=target_language)
    
    # Ensure proper UTF-8 encoding and decoding for Bengali text
    translated_text = result["translatedText"].encode("utf-8").decode("utf-8")
    return translated_text

if __name__ == "__main__":
    sample_text = "Hello, how are you?Are you fine thanks!"
    
    # Translate the sample text to Bengali
    translated_output = translate_text(sample_text, "es")
    
    print("Original:", sample_text)
    print("Translated to Bengali:", translated_output)
