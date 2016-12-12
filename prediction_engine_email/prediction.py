import matplotlib.pyplot as plt

from data_source import DumpFile, CsvFile
from data_preparation import Cleansing, Splitting
from modeling import Transformation
from modeling import Classifier, ClassificationFactory
from evaluation import Evaluator

model_base_path = "./model"
data_base_path = "./data"

tfidf_transformer_file_path = model_base_path + "/tfidf_transformer.model"
prediction_model_file_path = model_base_path + "/prediction.model"

# stop_words = text.ENGLISH_STOP_WORDS.union(['re:', 'fw:', 'oocl', 'for', 'to', 'request:', 'inc.'])


def predict_subject(subject):
    transformer = DumpFile.read(tfidf_transformer_file_path)
    model = DumpFile.read(prediction_model_file_path)

    prediction_data_numpy = transformer.transform([subject])
    prediction_result = model.predict(prediction_data_numpy)
    predicted_label = prediction_result.tolist()[0]

    return predicted_label


def combine_predict_result(raw_data, test_data, test_predictions):
    real_dict = dict(zip(raw_data['intention'], raw_data['subject']))
    predict_dict = dict(zip(test_data, test_predictions))
    error_count = 0
    for data_item in predict_dict:
        if predict_dict[data_item] != real_dict[data_item]:
            error_count += 1
            print(data_item + " predict: " + predict_dict[data_item] + " real: " + real_dict[data_item])
    print("All testing data is " + str(len(test_data)) + " missing data is " + str(error_count) + " rate is " + str(1 - error_count / len(test_data)))


def training(source_file_name, algorithm="bayes"):
    # Data preparation
    raw_data = CsvFile.read(
        file_path=source_file_name, separator="!@#", headers=["subject", "intention"])
    cleansing = Cleansing()
    raw_data = cleansing.filter(raw_data=raw_data)
    raw_data = cleansing.clean(raw_data=raw_data)
    training_data, training_label, test_data, test_label\
        = Splitting().stratifiedSplit(labels=raw_data.ix[:, 0], contents=raw_data.ix[:, 1])

    # Transformation
    transformation = Transformation()
    transformer = transformation.build_tfidf_transformer(training_data, stop_words=Cleansing.stopwords())
    training_data_numpy = transformer.transform(training_data)
    test_data_numpy = transformer.transform(test_data)
    DumpFile.write(file_path=tfidf_transformer_file_path, data=transformer)

    # Modeling
    # prediction_model = Classification().build_sgd().fit(training_data_numpy, training_label)
    prediction_model = ClassificationFactory.get_instance().get_prediction_model(training_data_numpy, training_label, algorithm)
    test_predictions = prediction_model.predict(test_data_numpy)
    DumpFile.write(file_path=prediction_model_file_path, data=prediction_model)

    # Evaluation
    combine_predict_result(raw_data, test_data, test_predictions)
    fig, sub_plot1 = plt.subplots()
    evaluator = Evaluator(model=prediction_model, contents=test_predictions, labels=test_label)
    evaluator.evaluate()
    evaluator.plot_cm(sub_plot1)
    plt.show()


if __name__ == '__main__':
    training(data_base_path + "/email_subject.csv", algorithm="bayes")
    # predict_subject("RE: exp161212  4999920140")
