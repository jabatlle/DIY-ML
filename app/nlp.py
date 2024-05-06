import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
import yake

# Function to download NLTK resources
def download_nltk_resources():
    nltk.download("stopwords", quiet=True)

# Class for NLP processing
class NLPProcessor:
    def __init__(self, text):
        self.text = text
        self.summary = None
        self.keywords = set()
        self.polarity = 0

    # Summarize the text
    def summarize(self):
        try:
            stop_words = set(stopwords.words('english'))
            word_freq = {}
            for word in nltk.word_tokenize(self.text.lower()):
                if word not in stop_words:
                    word_freq[word] = word_freq.get(word, 0) + 1
            sorted_words = sorted(word_freq, key=word_freq.get, reverse=True)
            self.summary = ' '.join(sorted_words[:10])  # Summarize by top 10 frequent words
            return self.summary
        except Exception as e:
            print(e)
            return None

    # Extract keywords
    def extract_keywords(self):
        try:
            extractor = yake.KeywordExtractor(top=10, stopwords=stopwords.words('english'))
            keywords = extractor.extract_keywords(self.text)
            self.keywords = {keyword for keyword, _ in keywords}
            return self.keywords
        except Exception as e:
            print(e)
            return None

    # Analyze polarity
    def analyze_polarity(self):
        try:
            analysis = TextBlob(self.text)
            self.polarity = analysis.sentiment.polarity
            return self.polarity
        except Exception as e:
            print(e)
            return None
