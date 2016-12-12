import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory
from util import place_handler


main_content = r"([ \t\d\w]+)"
origin_pattern = [
    r"ex(\s+)" + main_content + "(\s+)to(\s+)",
    r"ex(\s+)" + main_content,
]


class OriginPattern:
    origin_patterns = matcher_factory.merge_regular_expressions(origin_pattern)

    def extract(self, content):
        result = list()
        iterators = self.origin_patterns.finditer(content)
        for single_iter in iterators:
            phrase = single_iter.group(0)
            phrase = place_handler.is_string_a_place(phrase)
            if phrase is not False:
                result.append(phrase)
        return result

    def replace(self, content):
        local_stack = list()
        iterators = self.origin_patterns.finditer(content)
        for single_iter in iterators:
            phrase = single_iter.group(0)
            phrase = place_handler.is_string_a_place(phrase)
            if phrase is not False:
                local_stack.append((single_iter.start(), single_iter.end()))
        while len(local_stack) != 0:
            replace_item = local_stack.pop()
            content = content[:replace_item[0]] + ' _Origin_ ' + content[replace_item[1]:]
        return content