import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory


contract_patterns = [
    r"[^\w][A|B|C|D|E|F|\d]{8}[^\w]",
    r"Rate(\s+)agreement(\s*):(\s*)[A|B|C|D|E|F|\d]{8}[^\w]",
    r"Agreement(\s+)no(\s*)(:|#)(\s*)[A|B|C|D|E|F|\d]{8}[^\w]",
    r"Quotation(\s+)[A|B|C|D|E|F|\d]{8}[^\w]",
    r"Agreement(\s+)[A|B|C|D|E|F|\d]{8}[^\w]",
    r"Rate(\s+)folder(\s+)no(\s*):(\s*)[A|B|C|D|E|F|\d]{8}[^\w]"
]


class ContractPattern:

    contract_patterns = matcher_factory.merge_regular_expressions(contract_patterns)
    clean_result_pattern = re.compile(r"[A|B|C|D|E|F|\d]{8}", re.DOTALL | re.IGNORECASE)

    def extract(self, content):
        results = list()
        all_iterator = self.contract_patterns.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            result = self.clean_result_pattern.search(phrase)
            results.append(result.group(0).strip())
        return results

    def replace(self, content):
        return self.contract_patterns.sub(" _Contract_ ", content)
