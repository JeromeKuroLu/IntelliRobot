import numpy as np

from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt
from matplotlib import ticker


class Evaluation:
    name = ''
    precision = 0.0
    recall = 0.0
    f_score = 0.0
    support = 0.0


class Evaluator:
    def __init__(self, model, contents, labels):
        self.model = model
        self.contents = contents
        self.labels = labels
        self.results = []
        self.cm = None
        self.accuracy = -1

    def get_label_names(self):
        return list(set(self.labels))

    def get_labels(self):
        return self.labels

    def plot_cm(
            self, axis, title='Confusion matrix', y_label='True label', x_label='Predicted label'
            , cmap=plt.cm.Blues):

        axis.imshow(self.cm, interpolation='nearest', cmap=cmap)
        axis.set_title(title)
        # axis.colorbar()
        tick_marks = np.arange(len(self.model.classes_))
        axis.set_xticks(tick_marks)
        axis.set_xticklabels(self.model.classes_, rotation=0)
        axis.set_yticks(tick_marks)
        axis.set_yticklabels(self.model.classes_, rotation=0)

        width, height = self.cm.shape

        for x in range(width):
            for y in range(height):
                if self.cm[x][y] != 0:
                    axis.annotate(
                        str(self.cm[x][y]), xy=(y, x), horizontalalignment='center',
                        verticalalignment='center')

        # ax1.tight_layout()
        axis.set_ylabel(y_label)
        axis.set_xlabel(x_label)

        return axis

    # FIXME: Need allowing to evaluate specific type
    def evaluate(self):
        # Precision, Recall
        feature_names = self.model.classes_
        evaluation_results = precision_recall_fscore_support(self.labels, self.contents, average=None,
                                                             labels=feature_names)
        precisions = evaluation_results[0]
        recalls = evaluation_results[1]
        f_scores = evaluation_results[2]
        supports = evaluation_results[3]

        for name in feature_names:
            evaluation = Evaluation()
            evaluation.name = name
            self.results.append(evaluation)

        for idx, name in enumerate(feature_names):
            self.results[idx].precision = precisions[idx]
            self.results[idx].recall = recalls[idx]
            self.results[idx].f_score = f_scores[idx]
            self.results[idx].support = supports[idx]

        # Confusion Matrix
        self.cm = confusion_matrix(self.labels, self.contents)

        # Accuracy
        self.accuracy = accuracy_score(self.labels, self.contents)

        return self

    def plot_precision_recall_table(self, axis):
        columns = ['precision', 'recall']
        labels = []
        cell_texts = []

        for result in self.results:
            labels.append(result.name)
            cell_texts.append([result.precision, result.recall])

        axis.matshow(cell_texts, cmap=plt.cm.Blues, alpha=0.3, aspect='auto')
        for row_idx, row in enumerate(cell_texts):
            for col_idx in range(0, 2):
                val = round(row[col_idx], 2)
                axis.text(x=col_idx, y=row_idx, s=val, va='center', ha='center')

        axis.set_xticklabels([''] + columns)
        axis.set_yticklabels([''] + labels)
        axis.yaxis.set_major_locator(ticker.MultipleLocator(1))

    def show_incorrect_prediction(self, test_data, compare_actual, compare_predict):
        idx_dict = self.labels.index.tolist()
        for actual_idx, actual in enumerate(self.labels):
            predict = self.contents[actual_idx]
            if actual == compare_actual and predict == compare_predict:
                print(test_data[idx_dict[actual_idx]])

