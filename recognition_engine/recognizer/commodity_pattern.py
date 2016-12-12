import os
import sys
import re

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory


main_content = r"([ \t\d\w]+)"
commodity_pattern = [
    r"Goods(\s*)[:-](\s*)" + main_content,
    r"Commodity(\s*)[:-](\s*)" + main_content,
    r"(product|commodity|comm)(\s+)(is|are|will(\s+)be)(\s+)" + main_content,
]


class CommodityPattern:

    commodity_patterns = matcher_factory.merge_regular_expressions(commodity_pattern)
    clean_result_pattern = matcher_factory.merge_regular_expressions([
        r"Goods(\s*)[:-]",
        r"Commodity(\s*)[:-](\s*)",
        r"(cargo|product|commodity|comm)(\s+)(is|are|will(\s+)be)(\s+)"
    ])

    def extract(self, content):
        results = list()
        all_iterator = self.commodity_patterns.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            result = re.sub(self.clean_result_pattern, "", phrase)
            results.append(result.strip())
        return results

    def replace(self, content):
        return self.commodity_patterns.sub(" _Commodity_ ", content)
