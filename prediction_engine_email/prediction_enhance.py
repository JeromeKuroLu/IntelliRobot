import matplotlib.pyplot as plt
from data_source import DumpFile, CsvFile
from data_preparation import Cleansing, Splitting
from modeling import Transformation
from modeling import Classifier, ClassificationFactory
from evaluation import Evaluator
from sklearn.grid_search import GridSearchCV
from time import time
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import cross_val_score
from distance_calculate import calculation_distance

model_base_path = "./model"
data_base_path = "./data"

tfidf_transformer_file_path = model_base_path + "/tfidf_transformer.model"
prediction_model_file_path = model_base_path + "/prediction.model"

# stop_words = text.ENGLISH_STOP_WORDS.union(['re:', 'fw:', 'oocl', 'for', 'to', 'request:', 'inc.'])
file_path_dict = {
    'all': (model_base_path + "/[algorithm]_all_transformer", model_base_path + "/[algorithm]_all_predict_model"),
    'body': (model_base_path + "/[algorithm]_body_transformer", model_base_path + "/[algorithm]_body_predict_model"),
    'subject': (
        model_base_path + "/[algorithm]_subject_transformer", model_base_path + "/[algorithm]_subject_predict_model")
}


def predict_subject(subject):
    transformer = DumpFile.read(tfidf_transformer_file_path)
    model = DumpFile.read(prediction_model_file_path)
    prediction_data_numpy = transformer.transform([subject])
    prediction_result = model.predict(prediction_data_numpy)
    predicted_label = prediction_result.tolist()[0]

    return predicted_label


# 'all' means consider both subject & body, 'body' means consider only body, 'subject' means consider only subject
def predict_email(content, target="all", algorithm="rft"):
    transformer_file_path = file_path_dict[target][0].replace('[algorithm]', algorithm)
    model_path = file_path_dict[target][1].replace('[algorithm]', algorithm)

    transformer = DumpFile.read(transformer_file_path)
    model = DumpFile.read(model_path)

    prediction_data_numpy = transformer.transform([content])
    prediction_result = model.predict_proba(prediction_data_numpy)
    all_classes = model.classes_
    property_result = dict(zip(all_classes.tolist(), prediction_result.tolist()[0]))
    predicted_label = all_classes.tolist()[0]
    max_number = property_result[predicted_label]
    for label in property_result:
        if property_result[label] >= max_number:
            max_number = property_result[label]
            predicted_label = label
    # predicted_label = prediction_result.tolist()[0]

    return predicted_label, property_result


def combine_predict_result(raw_data, test_data, test_predictions, labels):
    real_dict = dict(zip(raw_data[labels[1]], raw_data[labels[0]]))
    predict_dict = dict(zip(test_data, test_predictions))
    error_count = 0
    for data_item in predict_dict:
        if predict_dict[data_item] != real_dict[data_item]:
            error_count += 1
            print(data_item + " predict: " + predict_dict[data_item] + " real: " + real_dict[data_item])
    print("All testing data is " + str(len(test_data)) + " missing data is " + str(error_count) + " rate is " + str(
        1 - error_count / len(test_data)))


def training(raw_data, training_data, test_data, training_label, test_label, labels, transformer_file_path,
             prediction_file_path, show_pic=True, algorithm="bayes"):
    # Transformation
    transformation = Transformation()
    transformer = transformation.build_tfidf_transformer(training_data, stop_words=Cleansing.stopwords())
    training_data_numpy = transformer.transform(training_data)
    # test_data = "RE: Book"
    test_data_numpy = transformer.transform(test_data)
    calculate_distance(training_data, test_data)
    DumpFile.write(file_path=transformer_file_path, data=transformer)

    # Modeling
    # prediction_model = Classification().build_sgd().fit(training_data_numpy, training_label)
    prediction_model = ClassificationFactory.get_instance().get_prediction_model(training_data_numpy, training_label,
                                                                                 algorithm)
    test_predictions = prediction_model.predict(test_data_numpy)
    DumpFile.write(file_path=prediction_file_path, data=prediction_model)

    # Evaluation
    combine_predict_result(raw_data, test_data, test_predictions, labels)
    if show_pic:
        fig, sub_plot1 = plt.subplots()
        evaluator = Evaluator(model=prediction_model, contents=test_predictions, labels=test_label)
        evaluator.evaluate()
        evaluator.plot_cm(sub_plot1)
        plt.show()

def calculate_distance(training_data, test_data):
    transformation = Transformation()
    transformer = transformation.build_word2vec(training_data)
    training_data_numpy = transformation.tranform_word2vec(transformer, training_data)
    test_data = ["Booking Office"]
    test_data_numpy = transformation.tranform_word2vec(transformer, test_data)
    calculation_distance.calculateDistance(training_data_numpy, training_data, test_data_numpy, test_data, return_num = 10)

def training_email_subject(source_file_name, algorithm="bayes", show_pic=True):
    # Data preparation
    raw_data = CsvFile.read(
        file_path=source_file_name, separator="!@#", headers=["subject", "intention"])
    cleansing = Cleansing()
    raw_data = cleansing.filter(raw_data=raw_data)
    raw_data = cleansing.clean(raw_data=raw_data)
    training_data, training_label, test_data, test_label \
        = Splitting().stratifiedSplit(labels=raw_data.ix[:, 0], contents=raw_data.ix[:, 1])

    training(raw_data, training_data, test_data, training_label, test_label, ["subject", "intention"],
             model_base_path + r"/subject_transformer", model_base_path + r"/subject_predict_model",
             algorithm=algorithm, show_pic=show_pic)


def get_raw_data(source_file_name):
    raw_data = CsvFile.read(
        file_path=source_file_name, separator="!@#", headers=["intention", "subject", "body"])
    cleansing = Cleansing()
    raw_data = cleansing.filter(raw_data=raw_data)
    raw_data = cleansing.clean(raw_data=raw_data)
    raw_data['all'] = raw_data['subject'] + ' ' + raw_data['body']
    return raw_data


def training_email(source_file_name, algorithm="bayes", show_pic=True):
    raw_data = get_raw_data(source_file_name)
    only_subject = raw_data[['intention', 'subject']]
    only_body = raw_data[['intention', 'body']]
    all_content = raw_data[['intention', 'all']]

    training_data, training_label, test_data, test_label \
        = Splitting().stratifiedSplit(labels=only_subject.ix[:, 0], contents=only_subject.ix[:, 1])
    training(raw_data, training_data, test_data, training_label, test_label, ["intention", "subject"],
             model_base_path + r"/[algorithm]_subject_transformer".replace('[algorithm]', algorithm),
             model_base_path + r"/[algorithm]_subject_predict_model".replace('[algorithm]', algorithm),
             algorithm=algorithm, show_pic=False)
    print('===============================')
    training_data, training_label, test_data, test_label \
        = Splitting().stratifiedSplit(labels=only_body.ix[:, 0], contents=only_body.ix[:, 1])
    training(raw_data, training_data, test_data, training_label, test_label, ["intention", "body"],
             model_base_path + r"/[algorithm]_body_transformer".replace('[algorithm]', algorithm),
             model_base_path + r"/[algorithm]_body_predict_model".replace('[algorithm]', algorithm),
             algorithm=algorithm,
             show_pic=False)
    print('===============================')
    # training_data, test_data = Splitting.get_taining_testing_dataset(raw_data)
    # training_pipeline(training_data, training_data['intention'], test_data, test_data['intention'],
    #                   model_base_path + r"/[algorithm]_all_predict_model".replace('[algorithm]', algorithm),
    #                   algorithm=algorithm, show_pic=False)
    training_data, training_label, test_data, test_label \
        = Splitting().stratifiedSplit(labels=all_content.ix[:, 0], contents=all_content.ix[:, 1])
    training(raw_data, training_data, test_data, training_label, test_label, ["intention", "all"],
             model_base_path + r"/[algorithm]_all_transformer".replace('[algorithm]', algorithm),
             model_base_path + r"/[algorithm]_all_predict_model".replace('[algorithm]', algorithm), algorithm=algorithm,
             show_pic=False)


def detect_best_params(algorithm_model, param_grid, contents, labels):
    grid_search = GridSearchCV(algorithm_model, param_grid=param_grid)
    start = time()
    grid_search.fit(contents, labels)
    result_params = list()
    for key in grid_search.best_params_:
        result_params.append(key + '=' + str(grid_search.best_params_[key]))
    print(', '.join(result_params))
    print(str(time() - start))
    # print("GridSearchCV took %.2f seconds for %d candidate parameter settings." % (
    # time() - start, len(grid_search)))
    # report(grid_search.cv_results_)


def detect_best_params_for_random_forest(source_file_name):
    param_grid = {"max_depth": [3, 100, 200, 300, None],
                  "n_estimators": [100, 150],
                  "max_features": [10, 'auto', None, 'sqrt', 'log2'],
                  "min_samples_split": [2, 4, 10, 1, 3],
                  "min_samples_leaf": [1, 2, 5, 3, 10],
                  "bootstrap": [True, False],
                  "criterion": ["gini", "entropy"]}
    algorithm_model = ClassificationFactory.get_instance().get_prediction_instance('rft')
    raw_data = get_raw_data(source_file_name)
    all_content = raw_data[['intention', 'all']]
    training_data, training_label, test_data, test_label \
        = Splitting().stratifiedSplit(labels=all_content.ix[:, 0], contents=all_content.ix[:, 1])
    transformation = Transformation()
    transformer = transformation.build_tfidf_transformer(training_data, stop_words=Cleansing.stopwords())
    training_data_numpy = transformer.transform(training_data)
    detect_best_params(algorithm_model, param_grid, training_data_numpy, training_label)


class ItemSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]


def build_model(training_data, training_label, algorithm='bayes'):
    tfidf1 = Transformation.get_new_tfidf_instance()
    tfidf2 = Transformation.get_new_tfidf_instance()
    clf = ClassificationFactory.get_instance().get_prediction_instance(algorithm)
    pipelines = [
        ('union', FeatureUnion(
            n_jobs=-1,
            transformer_list=[
                ('body', Pipeline([
                    ('selector', ItemSelector(key='body')),
                    ('tfidf', tfidf1)
                ])),
                ('subject', Pipeline([
                    ('selector', ItemSelector(key='subject')),
                    ('tfidf', tfidf2)
                ]))
            ],
            transformer_weights={
                'body': 0.5,

                'subject': 0.5
            }
        )),
        ('clf', clf)
    ]
    model = Pipeline(pipelines)
    model.fit(training_data, training_label)

    return model


def training_pipeline(training_data, training_label, test_data, test_label,
                      prediction_file_path, show_pic=True, algorithm="bayes"):
    # Transformation
    prediction_model = build_model(training_data, training_label, algorithm)
    print(cross_val_score(prediction_model, test_data, test_data['intention'], cv=10))
    print('here')
    # DumpFile.write(file_path=prediction_file_path, data=prediction_model)
    #
    # # Evaluation
    # combine_predict_result(raw_data, test_data, test_predictions, labels)
    if show_pic:
        fig, sub_plot1 = plt.subplots()
        evaluator = Evaluator(model=prediction_model, contents=test_predictions, labels=test_label)
        evaluator.evaluate()
        evaluator.plot_cm(sub_plot1)
        plt.show()


if __name__ == '__main__':
    # detect_best_params_for_random_forest(data_base_path + "/data3.csv")
    training_email(data_base_path + "/data5.csv", algorithm="rft")
    # training_email_subject(data_base_path + "/email_subject.csv", algorithm="bayes")
    # predict_subject("RE: exp161212  4999920140")
