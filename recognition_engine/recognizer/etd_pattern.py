import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory
from util.time_handler import date_time, specify_time, week, unit


etd_pattern = [
    r"etd(\s+)([\w \t]+)(\s*)" + date_time,
    r"sailing(\s+)([\w \t]+)(on|the)?" + date_time,
    r"sailing(\s+)before(the?)(\s*)" + date_time,
    r"sailing(\s+)on(\s+)the(\s*)" + date_time,
    r"departure(\s+)" + date_time,
    r"etd(\s*):(\s*)" + date_time,
]


class EtdPattern:

    etd_patterns = matcher_factory.merge_regular_expressions(etd_pattern)

    def extract(self, content):
        results = list()
        all_iterator = self.etd_patterns.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            results.append(phrase)
        return results

    def replace(self, content):
        return self.etd_patterns.sub(" _ETD_ ", content)