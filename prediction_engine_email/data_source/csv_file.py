import pandas as pd


class CsvFile:
    @staticmethod
    def read(file_path, headers, separator=",", has_header=None):
        raw_data = pd.read_csv(
            file_path,  sep=separator, engine='python', header=has_header, names=headers)
        return raw_data

