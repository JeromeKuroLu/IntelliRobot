import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory
from util import place_handler

main_content = r"([ \t\d\w]+)"
destination_pattern = [
    r"Delivered(\s+)To(\s*)(:?)" + main_content,
    r"To(\s+)" + main_content,
    r"Destination(\s*):" + main_content,
    r"CFR(\s+)" + main_content,
    r"To(\s+)" + main_content,
    r"For(\s+)" + main_content + "(\s*),(\s*)" + main_content,
    r"For(\s+)Destination(\s+)" + main_content + r"(\s+)CFR",
    r"sailing(\s+)to(\s+)" + main_content,
    main_content + "(\s*)(\d{10}|_bkg_number_)",
]


class DestinationPattern:
    destination_patterns = matcher_factory.merge_regular_expressions(destination_pattern)

    def extract(self, content):
        result = list()
        iterators = self.destination_patterns.finditer(content)
        for single_iter in iterators:
            phrase = single_iter.group(0)
            phrase = place_handler.is_string_a_place(phrase)
            if phrase is not False:
                result.append(phrase)
        return result

    def replace(self, content):
        local_stack = list()
        iterators = self.destination_patterns.finditer(content)
        for single_iter in iterators:
            phrase = single_iter.group(0)
            phrase = place_handler.is_string_a_place(phrase)
            if phrase is not False:
                local_stack.append((single_iter.start(), single_iter.end()))
        while len(local_stack) != 0:
            replace_item = local_stack.pop()
            content = content[:replace_item[0]] + ' _Destination_ ' + content[replace_item[1]:]
        return content


if __name__ == '__main__':
    test = '''
 _Size_type_  HC CONTAINERS  - NEW YORK 4999921770
Hello

Please arrange to position  _Size_type_  GP/HC container at:

RAYBURN TRADING

PORRITT STREETOFF BRIDGE STREET

BURY BL9 6HJ

On Friday 12.08.16 @ 0800hrs

Collection ref: LIBERTY DISTRIBUTION

Non Haz Toiletries approx. 9000kgs

Going to arrival New York including US THC – quote ref: TAN2016V4.2
    '''
    print(DestinationPattern().replace(test))
