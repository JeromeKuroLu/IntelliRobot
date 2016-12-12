from sklearn.externals import joblib


class DumpFile:
    @staticmethod
    def read(file_path):
        return joblib.load(file_path)

    @staticmethod
    def write(file_path, data):
        joblib.dump(data, file_path)
