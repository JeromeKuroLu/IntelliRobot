import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory
from util.time_handler import date_time, specify_time, week, unit


eta_pattern = [
    r"eta(\s+)(\w+)(approx|approximate|approximately|about|on|for)([^\w]*)" + date_time,
    r"eta(\s+)(\w+)((of|for)?)(\s+)" + date_time,
    r"eta(\s*):(\s*)" + date_time + "(\s*)" + specify_time,
    r"eta(\s+)sin(\s*):(\s*)" + date_time
]


class EtaPattern:

    eta_patterns = matcher_factory.merge_regular_expressions(eta_pattern)

    def extract(self, content):
        results = list()
        all_iterator = self.eta_patterns.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            results.append(phrase)
        return results

    def replace(self, content):
        return self.eta_patterns.sub(" _ETA_ ", content)
