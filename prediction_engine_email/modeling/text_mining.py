from sklearn.feature_extraction.text import CountVectorizer


class TextMining:
    @staticmethod
    def count_ngrams(raw_data_df, ngram_range=(1, 3), stop_words=None):
        document = raw_data_df.as_matrix()
        vectorizer = CountVectorizer(ngram_range=ngram_range, stop_words=stop_words)

        X = vectorizer.fit_transform(document)
        terms = vectorizer.get_feature_names()

        freqs = X.sum(axis=0).A1
        result = dict(zip(terms, freqs))
        return sorted(result.items(), key=lambda x: x[1], reverse=True)
