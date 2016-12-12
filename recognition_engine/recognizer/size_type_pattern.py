import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory


size_type_pattern = [
    r"(\d+)(\s*)x(\s*)(\d+)(\s*)([']?\w\w)"
]


class SizeTypePattern:

    size_type_patterns = matcher_factory.merge_regular_expressions(size_type_pattern)

    def extract(self, content):
        results = list()
        all_iterator = self.size_type_patterns.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            results.append(phrase.strip())
        return results

    def replace(self, content):
        return self.size_type_patterns.sub(" _Size_type_ ", content)


if __name__ == '__main__':
    test = '''
    asdfa asdfasdf 1 x 20'gp
    asdfaweadf asdfawe 23x40hp
        '''
    print(SizeTypePattern().extract(test))