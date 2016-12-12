import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory


load_address_pattern = [
    r"(Load Address(\s*):(\s*)|To Load(\s*?)\n|Load Address(\s+))(.+?)(([A-Za-z]\d|\d[A-Za-z])([^\n]*)\n)",
    r"(Loading Address(\s*):(\s*))(.+?)(([A-Za-z]\d|\d[A-Za-z])([^\n]*)\n)",
    r"at(\s+)the(\s+)below(\s+)address(.+?)(([A-Za-z]\d|\d[A-Za-z])([^\n]*)\n)",
    r"Loading(.+?)at(\s+)the(\s+)below(\s+)address(.+?)(([A-Za-z]\d|\d[A-Za-z])([^\n]*)\n)"
]


class LoadAddress:
    load_address_patterns = matcher_factory.merge_regular_expressions(load_address_pattern)
    clean_result_pattern = r"(Load Address)(\s*):(\s*)"

    def extract(self, content):
        results = list()
        all_iterator = self.load_address_patterns.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            phrase = re.sub(self.clean_result_pattern, "", phrase)
            results.append(phrase.strip())
        return results

    def replace(self, content):
        return self.load_address_patterns.sub(" _Load_Address_ ", content)
