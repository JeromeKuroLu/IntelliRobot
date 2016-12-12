from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.cross_validation import train_test_split


class Splitting:

    def stratifiedSplit(self, labels, contents, n_iter=1, test_size=0.2, random_state=0):
        split_index = StratifiedShuffleSplit(labels, n_iter=n_iter, test_size=test_size, random_state=random_state)
        for train_index, test_index in split_index:
            training_contents = contents.iloc[train_index]
            training_labels = labels.iloc[train_index]

            test_contents = contents.iloc[test_index]
            test_labels = labels.iloc[test_index]

        return training_contents, training_labels, test_contents, test_labels

    @staticmethod
    def get_training_testing_dataset(raw_data):
        return train_test_split(raw_data, train_size=0.8)

