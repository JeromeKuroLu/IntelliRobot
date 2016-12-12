import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory

phone_patterns = [
    r"(\d+)(\s*)([`\-=\[\];',./~!@#$%^&*()_+{}:<>?\\]|(\s+))(\d+)(\s*)([`\-=\[\];',./~!@#$%^&*()_+{}:<>?\\]|\s+)(\d+)",
    r"tel(\s*):(\s*)[(+)\d\s]+",
    r"mobile(\s*):(\s*)[(+)\d\s]+"
]


class PhonePattern:
    time_pattern = matcher_factory.merge_regular_expressions(phone_patterns)

    def extract(self, content):
        results = list()
        all_iterator = self.time_pattern.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            phrase = phrase.strip()
            results.append(phrase.strip())
        return results

    def replace(self, content):
        return self.time_pattern.sub(" __phone__ ", content)
