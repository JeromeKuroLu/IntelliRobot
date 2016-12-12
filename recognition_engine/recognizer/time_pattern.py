import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory

time_patterns = [
    r"(\d+)(\s*):(\s*)(\d+)(\s*)((am|pm|hrs)?)",
    r"\d(\d?)(am|pm)",
    r"\d{4}(\s*)hrs",
    r"\d\d(\s*)\.(\s*)\d\d(\s*)(hrs)"
]


class TimePattern:
    time_pattern = matcher_factory.merge_regular_expressions(time_patterns)

    def extract(self, content):
        results = list()
        all_iterator = self.time_pattern.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            phrase = re.sub(r'\s\s+', ' ', phrase)
            phrase = re.sub(r'\s+:\s+', ':', phrase)
            results.append(phrase.strip())
        return results

    def replace(self, content):
        return self.time_pattern.sub(" _time_ ", content)
