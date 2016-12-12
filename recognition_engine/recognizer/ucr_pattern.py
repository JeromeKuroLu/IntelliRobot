import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory


ucr_patterns = [
    r"(UCR)(\s*):(\s*)(\w+)-(\w+)"
]


class UcrPattern:
    ucr_patterns = matcher_factory.merge_regular_expressions(ucr_patterns)
    clean_result_pattern = r"(UCR)(\s*):(\s*)"

    def extract(self, content):
        results = list()
        all_iterator = self.ucr_patterns.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            phrase = re.sub(self.clean_result_pattern, "", phrase)
            results.append(phrase.strip())
        return results

    def replace(self, content):
        return self.ucr_patterns.sub(" _UCR_ ", content)
