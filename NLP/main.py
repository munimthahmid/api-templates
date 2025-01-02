# main.py
from nlp_utils import (
    analyze_sentiment,
    analyze_entities,
    analyze_entity_sentiment,
    analyze_syntax,
    classify_text
)

def main():
    sample_text = (
        "Google Cloud is a fantastic platform for developers worldwide. "
        "It offers various services like Compute Engine, Cloud Storage, "
        "and advanced Machine Learning APIs. I absolutely love it, "
        "though sometimes it can be expensive. "
        "In the last month, I spent over $200 on experimental projects. "
        "Nevertheless, it's an amazing ecosystem for innovation!"
    )

    # 1. Sentiment Analysis
    sentiment_result = analyze_sentiment(sample_text)
    print("=== 1) Sentiment Analysis ===")
    print(f"Sentiment Score: {sentiment_result['score']} (range: -1.0 to 1.0)")
    print(f"Sentiment Magnitude: {sentiment_result['magnitude']}\n")

    # 2. Entity Recognition
    entities_result = analyze_entities(sample_text)
    print("=== 2) Entity Recognition ===")
    for ent in entities_result:
        print(f"Entity: {ent['name']}, Type: {ent['type']}, Salience: {ent['salience']:.2f}")
    print()

    # 3. Entity Sentiment
    entity_sentiment_result = analyze_entity_sentiment(sample_text)
    print("=== 3) Entity Sentiment ===")
    for ent in entity_sentiment_result:
        print(
            f"Entity: {ent['name']}, Type: {ent['type']}, Salience: {ent['salience']:.2f}, "
            f"Sentiment Score: {ent['sentiment_score']:.2f}, Magnitude: {ent['sentiment_magnitude']:.2f}"
        )
    print()

    # 4. Syntax Analysis
    syntax_result = analyze_syntax(sample_text)
    print("=== 4) Syntax Analysis ===")
    for token_info in syntax_result[:10]:  # just show first 10 tokens for brevity
        print(
            f"Token: '{token_info['token_text']}', "
            f"POS Tag: {token_info['tag']}, "
            f"Tense: {token_info['tense']}, "
            f"Person: {token_info['person']}, "
            f"Number: {token_info['number']}"
        )
    print("... (truncated)\n")

    # 5. Content Classification
    # NOTE: This requires English text with at least 20 characters.
    classification_result = classify_text(sample_text)
    print("=== 5) Content Classification ===")
    for cat in classification_result:
        print(f"Category Name: {cat['name']} (Confidence: {cat['confidence']:.2f})")
    print()

if __name__ == "__main__":
    main()
