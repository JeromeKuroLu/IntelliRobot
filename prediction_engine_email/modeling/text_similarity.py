from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


class TextSimilarity:
    @staticmethod
    def cosine_similarity(data_numpy):
        return (data_numpy * data_numpy.T).A
