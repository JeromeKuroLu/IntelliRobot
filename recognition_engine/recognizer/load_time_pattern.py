import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory
from util.time_handler import date_time, specify_time, week, unit


load_time_patterns = [
    r"Date(\s*)/(\s*)Time(\s*):(\s*)" + date_time + '(\s*)@(\s*)' + specify_time + '([^@]*)@(\s*)' + specify_time,
    r"((Date|Date(\s*)/(\s*)Time)(\s*):(\s*)|to load(\s*)|loading(\s*))" + date_time + '(\s*)@(\s*)' + specify_time,
    r"((Date|Date(\s*)/(\s*)Time)(\s*):(\s*)|to load(\s*)|loading(\s*))" + date_time + '(\s+)' + specify_time,
    r"Collect(\s*)" + week + '(\s*)' + specify_time + '(\s*)' + date_time,
    r"Collect(\s+)on(\s+)" + week + '(\s*)' + date_time + '(\s*)' + unit,
    specify_time + '(\s*)-(\s*)' + date_time,
]


class LoadTimePattern:
    load_time_pattern = matcher_factory.merge_regular_expressions(load_time_patterns)
    clean_result_pattern = r"(Date|Date(\s*)/(\s*)Time)(\s*):(\s*)|to load(\s*)|loading(\s*)|Collect(\s*)|Collect(\s+)on(\s+)"

    def extract(self, content):
        results = list()
        all_iterator = self.load_time_pattern.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            result = re.sub(self.clean_result_pattern, "", phrase)
            results.append(result.strip())
        return results

    def replace(self, content):
        return self.load_time_pattern.sub(" _Load_Time_ ", content)


if __name__ == '__main__':
    test = LoadTimePattern()
    test_str = [
        '''
        Date / Time:Thursday 23rd June @ 1200 noon – Driver to quote: UCB 19246 @ 1400 hrs – Driver to quote: UCB 19247
        ''',
        '''
        Date: 25th August @ 1200hrs
        ''',

    ]
    test_pattern = re.compile(
        r"((Date|Date(\s*)/(\s*)Time)(\s*):(\s*)|to load(\s*)|loading(\s*))" + date_time + '(\s*)@(\s*)' + specify_time,
        re.IGNORECASE | re.DOTALL)
    test_pattern2 = re.compile(
        r"Date(\s*)/(\s*)Time(\s*):(\s*)" + date_time + '(\s*)@(\s*)' + specify_time + '([^@]*)@(\s*)' + specify_time,
        re.IGNORECASE | re.DOTALL)
    for content in test_str:
        print(test.extract(content))


