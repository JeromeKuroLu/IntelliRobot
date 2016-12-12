from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models.word2vec import Word2Vec
from sklearn.preprocessing import scale
import numpy as np
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer, SnowballStemmer

global_stop_words = text.ENGLISH_STOP_WORDS


# class StemTokenizer(object):
#     def __init__(self):
#         self.sbs = SnowballStemmer("english")
#
#     def __call__(self, doc):
#         analyzer = super(TfidfVectorizer, self).build_analyzer()
#         return lambda x: self.sbs.stemWords(analyzer(doc))


class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


class Transformation:
    # def transform(self, transformer, contents):
    #     return transformer.transform(contents)
    @staticmethod
    def build_tfidf_transformer(
            contents, use_idf=False, lowercase=True, analyzer="word", stop_words=global_stop_words
            , tokenizer=LemmaTokenizer(), ngrams=(1, 2)):

        transformer = TfidfVectorizer(
            use_idf=use_idf, lowercase=lowercase, analyzer=analyzer, stop_words=stop_words
            , tokenizer=tokenizer, ngram_range=ngrams) \
            .fit(contents)

        return transformer

    @staticmethod
    def get_new_tfidf_instance(use_idf=False, lowercase=True, analyzer="word", stop_words=global_stop_words,
                               tokenizer=LemmaTokenizer(), ngrams=(1, 2)):
        return TfidfVectorizer(
            use_idf=use_idf, lowercase=lowercase, analyzer=analyzer, stop_words=stop_words
            , tokenizer=tokenizer, ngram_range=ngrams)

    @staticmethod
    def build_count_transformer(
            ngrams={1, 3}, stop_words=global_stop_words, lowercase=True, tokenizer=LemmaTokenizer()):
        transformer = CountVectorizer(
            ngram_range=ngrams, stop_words=stop_words, lowercase=lowercase, analyzer="word", tokenizer=tokenizer)

        return transformer

    @staticmethod
    def build_word_vector(model, text, size):
        vec = np.zeros(size).reshape((1, size))
        count = 0.
        for word in text:
            try:
                vec += model[word].reshape((1, size))
                count += 1.
            except KeyError:
                continue
        if count != 0:
            vec /= count
        return vec

    @staticmethod
    def build_word2vec(
            contents, num_features=400, min_word_count=40, num_workers=5, context=10, downsampling=1e-3):
        transformer = Word2Vec(
            workers=num_workers, size=num_features, min_count=min_word_count
            , window=context, sample=downsampling)

        transformer.build_vocab(contents)
        transformer.train(contents)

        return transformer

    @staticmethod
    def tranform_word2vec(transformer, contents, num_features=400):
        transformer.train(contents)
        train_vecs = np.concatenate([Transformation.build_word_vector(transformer, z, num_features) for z in contents])
        return scale(train_vecs)
