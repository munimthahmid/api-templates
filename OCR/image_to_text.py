import os
from google.cloud import vision

def detect_text_from_local(image_path):
    """
    Detects and returns text content from a local image using the Google Cloud Vision API.
    """
    # Initialize a Vision API client
    client = vision.ImageAnnotatorClient()

    # Read image file into memory
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Construct the Image instance
    image = vision.Image(content=content)

    # Call the text_detection method
    response = client.text_detection(image=image)
    annotations = response.text_annotations

    if response.error.message:
        raise Exception(f"Vision API Error: {response.error.message}")

    # The first annotation is the entire extracted text
    if annotations:
        full_text = annotations[0].description
        return full_text
    else:
        return ""

def detect_text_from_gcs(gcs_uri):
    """
    Detects and returns text content from an image stored in Google Cloud Storage.
    Example of gcs_uri: 'gs://your-bucket-name/path/to/image.jpg'
    """
    # Initialize a Vision API client
    client = vision.ImageAnnotatorClient()

    # Construct the Image instance
    image = vision.Image()
    image.source.image_uri = gcs_uri

    # Call the text_detection method
    response = client.text_detection(image=image)
    annotations = response.text_annotations

    if response.error.message:
        raise Exception(f"Vision API Error: {response.error.message}")

    if annotations:
        full_text = annotations[0].description
        return full_text
    else:
        return ""

if __name__ == "__main__":
    # (Optional) Set the credentials path programmatically
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cloud-vision-api.json"

    # Example: Detect text from a local image
    local_image_path = "test.jpg"
    text_from_local = detect_text_from_local(local_image_path)
    print("Extracted Text (Local Image):")
    print(text_from_local)

    # # Example: Detect text from an image in Google Cloud Storage
    # gcs_image_uri = "gs://your-bucket-name/path/to/gcs_image.jpg"
    # text_from_gcs = detect_text_from_gcs(gcs_image_uri)
    # print("\nExtracted Text (GCS Image):")
    # print(text_from_gcs)
