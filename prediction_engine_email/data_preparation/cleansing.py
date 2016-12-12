import nltk, string
from nltk.corpus import stopwords
from sklearn.feature_extraction import text


nltk_stop_words = stopwords.words('english')
sklearn_stop_words = text.ENGLISH_STOP_WORDS
email_stop_words = ['fw:', 'oocl', 'for', 'to', 'request:', 'inc.']
global_english_email_stop_words = text.ENGLISH_STOP_WORDS.union(email_stop_words + nltk_stop_words)


class Cleansing:
    @staticmethod
    def stopwords():
        return global_english_email_stop_words

    @staticmethod
    def filter(raw_data):
        # raw_data = raw_data.dropna()

        raw_data = raw_data[raw_data.intention != 'Notification']
        raw_data = raw_data[raw_data.intention != 'Rate Quotation']
        # raw_data = raw_data.applymap(replace_city_country_name)

        # raw_data = raw_data.groupby("subject").first()
        # raw_data = raw_data.groupby("intention").filter(lambda x: len(x) > 7)

        raw_data.subject = raw_data.subject.str.strip()
        return raw_data

    @staticmethod
    def clean(raw_data):
        # remove stop words
        raw_data['intention'] = raw_data['intention'] \
            .str.lower().str.split() \
            .apply(lambda x: [item for item in x if item not in global_english_email_stop_words]) \
            .apply(lambda x: ' '.join(x))
        return raw_data

