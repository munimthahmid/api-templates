# nlp_utils.py
import os
from google.cloud import language_v1

def get_language_service_client():
    """
    Returns a LanguageServiceClient, using the default credentials
    set by the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    # Optionally, you can set credentials in code if needed:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cloud-nlp-api.json"
    return language_v1.LanguageServiceClient()


def analyze_sentiment(text):
    """
    Analyzes the overall sentiment of the provided text (ranging from -1.0 to +1.0).
    Returns a dictionary containing sentiment score and magnitude.
    """
    client = get_language_service_client()
    
    # Construct a Document object
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment

    return {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude
    }


def analyze_entities(text):
    """
    Performs Entity Recognition on the text, extracting real-world entities like
    people, places, organizations, etc., along with their salience.
    Returns a list of entity dictionaries.
    """
    client = get_language_service_client()

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_entities(request={"document": document})

    entity_list = []
    for entity in response.entities:
        entity_list.append({
            "name": entity.name,
            "type": entity.type_.name,   # e.g. PERSON, LOCATION, ORGANIZATION
            "salience": entity.salience, # importance of the entity in the text
            # Optional: you can also get metadata like Wikipedia URL if available
            "metadata": dict(entity.metadata),
        })

    return entity_list


def analyze_entity_sentiment(text):
    """
    Performs Entity Sentiment Analysis, which combines entity recognition
    with sentiment for each entity. 
    Returns a list of entity data with sentiment scores.
    """
    client = get_language_service_client()

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_entity_sentiment(request={"document": document})

    entity_sentiment_list = []
    for entity in response.entities:
        entity_sentiment_list.append({
            "name": entity.name,
            "type": entity.type_.name,
            "salience": entity.salience,
            "sentiment_score": entity.sentiment.score,      # entity-level sentiment
            "sentiment_magnitude": entity.sentiment.magnitude
        })

    return entity_sentiment_list


def analyze_syntax(text):
    """
    Performs Syntax Analysis, returning tokens, part-of-speech tags, etc.
    Returns a list of token information dictionaries.
    """
    client = get_language_service_client()

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_syntax(request={"document": document})

    syntax_info = []
    for token in response.tokens:
        part_of_speech = token.part_of_speech
        syntax_info.append({
            "token_text": token.text.content,
            "tag": part_of_speech.tag.name,          # e.g. NOUN, VERB, ADJ
            "tense": part_of_speech.tense.name,      # e.g. PAST, PRESENT
            "person": part_of_speech.person.name,    # e.g. FIRST, SECOND, THIRD
            "number": part_of_speech.number.name     # e.g. SINGULAR, PLURAL
        })

    return syntax_info


def classify_text(text):
    """
    Classifies text into categories (e.g., /Arts & Entertainment/Music) using
    the Natural Language API's classify_text method.
    NOTE: This API only works for English text of >= 20 characters.
    Returns a list of categories with confidence scores.
    """
    client = get_language_service_client()

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.classify_text(request={"document": document})

    categories_info = []
    for category in response.categories:
        categories_info.append({
            "name": category.name,            # e.g. "/Arts & Entertainment/Movies"
            "confidence": category.confidence # float from 0.0 to 1.0
        })

    return categories_info
