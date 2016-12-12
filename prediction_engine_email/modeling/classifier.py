from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier


class Classifier:
    cls = None


class Classification:
    def __init__(self):
        self.sgd = None
        self.rft = None
        self.build_sgd()
        self.build_rft()

    def build_sgd(self, loss='log', penalty='l2', alpha=1e-3, n_iter=5, random_state=10, class_weight="balanced"):
        self.sgd = SGDClassifier(
            loss=loss, penalty=penalty, alpha=alpha, n_iter=n_iter
            , random_state=random_state, class_weight=class_weight)

        return self

    def sgd_fit(self, contents, labels):
        return self.sgd.fit(contents, labels)

    def build_rft(self):
        self.rft = RandomForestClassifier(n_estimators=100, max_features='sqrt', min_samples_split=1, min_samples_leaf=3, criterion='gini', bootstrap=False, max_depth=100)
        return self

    def rft_fit(self, contents, labels):
        return self.rft.fit(contents, labels)


class ClassificationFactory:

    single_instance = None

    @staticmethod
    def get_instance():
        if ClassificationFactory.single_instance is None:
            ClassificationFactory.single_instance = ClassificationFactory()
        return ClassificationFactory.single_instance

    def __init__(self):
        self.classifier = Classification()
        self.naive_bayes = MultinomialNB(alpha=0.01)
        self.algorithm = dict()
        self.algorithm['sgd'] = (lambda x, y: self.classifier.sgd_fit(x, y), self.classifier.sgd)
        self.algorithm['bayes'] = (lambda x, y: self.naive_bayes.fit(x, y), self.naive_bayes)
        self.algorithm['rft'] = (lambda x, y: self.classifier.rft_fit(x, y), self.classifier.rft)

    def get_prediction_model(self, training_data_numpy, training_label, mark):
        return self.algorithm[mark][0](training_data_numpy, training_label)

    def get_prediction_instance(self, mark):
        return self.algorithm[mark][1]
