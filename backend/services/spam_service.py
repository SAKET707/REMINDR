import joblib
import nltk

from pathlib import Path
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

MODEL_DIR = Path(__file__).parent.parent / "artifacts"

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("punkt_tab", quiet=True)

_model = joblib.load(
    MODEL_DIR / "spam_model.joblib"
)

_vectorizer = joblib.load(
    MODEL_DIR / "vectorizer.joblib"
)

_lemmatizer = WordNetLemmatizer()

_stop_words = set(stopwords.words("english"))


class SpamService:

    @staticmethod
    def preprocess(text: str):

        text = text.lower()

        tokens = word_tokenize(text)

        tokens = [
            token
            for token in tokens
            if token.isalnum()
        ]

        tokens = [
            token
            for token in tokens
            if token not in _stop_words
        ]

        tokens = [
            _lemmatizer.lemmatize(token)
            for token in tokens
        ]

        return " ".join(tokens)

    @staticmethod
    def predict(body: str) -> bool:

        cleaned = SpamService.preprocess(body)

        vector = _vectorizer.transform(
            [cleaned]
        )

        prediction = _model.predict(vector)[0]

        return prediction == 1
