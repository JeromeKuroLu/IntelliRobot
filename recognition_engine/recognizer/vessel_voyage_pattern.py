import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory


vessel_voyage_pattern = [
    r"for(\s+)vessel(\s+)[ \t\w]+",
    r"for(\s+)the(\s+)vessel(\s+)[ \t\w]+"
]


class VesselVoyagePattern:

    vessel_voyage_patterns = matcher_factory.merge_regular_expressions(vessel_voyage_pattern)
    clean_result_pattern = r"for(\s+)the(\s+)vessel(\s+)|for(\s+)vessel(\s+)"

    def extract(self, content):
        results = list()
        all_iterator = self.vessel_voyage_patterns.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            phrase = re.sub(self.clean_result_pattern, "", phrase)
            results.append(phrase.strip())
        return results

    def replace(self, content):
        return self.vessel_voyage_patterns.sub(" _Vessel_voyage_ ", content)