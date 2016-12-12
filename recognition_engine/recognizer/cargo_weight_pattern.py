import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory


end_mark = "(kg|kgs|tonne|ton)"
cargo_weight_pattern = [
    r"(\d+)(,?)(\d+)(\s*)" + end_mark,
]


class CargoWeightPattern:

    cargo_weight_patterns = matcher_factory.merge_regular_expressions(cargo_weight_pattern)

    def extract(self, content):
        results = list()
        all_iterator = self.cargo_weight_patterns.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            results.append(phrase.strip())
        return results

    def replace(self, content):
        return self.cargo_weight_patterns.sub(" _Cargo_weight_ ", content)
