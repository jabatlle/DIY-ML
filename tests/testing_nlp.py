import sys
from app.nlp import Content

def test(sample_text):
    try:
        content = Content(sample_text)
        content.summarize()
        content.get_keywords()
        content.get_sentiment()

        print("Summary:")
        print(content.summary)
        print("\nKeywords:")
        print(content.keywords)
        print("\nSentiment:")
        print(content.sentiment)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    sample_text = "Awesome! I am feeling extremely happy."

    test(sample_text)
