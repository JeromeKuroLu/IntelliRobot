import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory

temp_patterns = [
    r"((((\s)((minu|plus))(\s))?((\s)(-|\+)(\s))?(\s)(\d+)(\s)((\s)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\])(\s))?((\s)((degre|deg|grad))(\s))?(\s)((c|f|celsiu|celciu|fah|cel))(\s)((\s)((degre|deg|grad))(\s))?)|(((\s)(\d+)(\s))?((\s)(%)(\s))?(\s)((humid))(\s)((\s)((sensor))(\s))?((\s)((moistur))(\s))?((\s)((percentag))(\s))?((\s)(%)(\s))?((\s)(\d+)(\s))?)|(((\s)((minu|plus))(\s))?((\s)(-|\+)(\s))?(\s)(\d+)(\s)((\s)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\])(\s))?((\s)((degre|deg|grad))(\s))?(\s)((c|f|celsiu|celciu|fah|cel))(\s)((\s)((degre|deg|grad))(\s))?)|(((\s)(\d+)(\s))?((\s)(%)(\s))?(\s)((humid))(\s)((\s)((sensor))(\s))?((\s)((moistur))(\s))?((\s)((percentag))(\s))?((\s)(%)(\s))?((\s)(\d+)(\s))?))(\s)((temperatur|temp))(\s)((\s)((set))(\s))?",
    r"((\s)((pre))(\s))?(\s)(-)(\s)(\s)((set))(\s)(\s)((temperatur|temp))(\s)((\s)((at|to))(\s))?((\s)((be))(\s))?((((\s)((minu|plus))(\s))?((\s)(-|\+)(\s))?(\s)(\d+)(\s)((\s)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\])(\s))?((\s)((degre|deg|grad))(\s))?(\s)((c|f|celsiu|celciu|fah|cel))(\s)((\s)((degre|deg|grad))(\s))?)|(((\s)(\d+)(\s))?((\s)(%)(\s))?(\s)((humid))(\s)((\s)((sensor))(\s))?((\s)((moistur))(\s))?((\s)((percentag))(\s))?((\s)(%)(\s))?((\s)(\d+)(\s))?)|(((\s)((minu|plus))(\s))?((\s)(-|\+)(\s))?(\s)(\d+)(\s)((\s)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\])(\s))?((\s)((degre|deg|grad))(\s))?(\s)((c|f|celsiu|celciu|fah|cel))(\s)((\s)((degre|deg|grad))(\s))?)|(((\s)(\d+)(\s))?((\s)(%)(\s))?(\s)((humid))(\s)((\s)((sensor))(\s))?((\s)((moistur))(\s))?((\s)((percentag))(\s))?((\s)(%)(\s))?((\s)(\d+)(\s))?))",
    r"((\s)((set))(\s))?(\s)((temperatur|temp))(\s)((\s)((set))(\s))?((\s)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\]|[`\-=\[\];',./~!@#$%^&*()_+{}:<>?\\])(\s))?((\s)((need))(\s))?((\s)((at|to))(\s))?((\s)((be))(\s))?((((\s)((minu|plus))(\s))?((\s)(-|\+)(\s))?(\s)(\d+)(\s)((\s)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\])(\s))?((\s)((degre|deg|grad))(\s))?(\s)((c|f|celsiu|celciu|fah|cel))(\s)((\s)((degre|deg|grad))(\s))?)|(((\s)(\d+)(\s))?((\s)(%)(\s))?(\s)((humid))(\s)((\s)((sensor))(\s))?((\s)((moistur))(\s))?((\s)((percentag))(\s))?((\s)(%)(\s))?((\s)(\d+)(\s))?)|(((\s)((minu|plus))(\s))?((\s)(-|\+)(\s))?(\s)(\d+)(\s)((\s)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\])(\s))?((\s)((degre|deg|grad))(\s))?(\s)((c|f|celsiu|celciu|fah|cel))(\s)((\s)((degre|deg|grad))(\s))?)|(((\s)(\d+)(\s))?((\s)(%)(\s))?(\s)((humid))(\s)((\s)((sensor))(\s))?((\s)((moistur))(\s))?((\s)((percentag))(\s))?((\s)(%)(\s))?((\s)(\d+)(\s))?))",
    r"((\s)(\d+)(\s))?((\s)(%)(\s))?(\s)((humid))(\s)((\s)((sensor))(\s))?((\s)((moistur))(\s))?((\s)((percentag))(\s))?((\s)(%)(\s))?((\s)(\d+)(\s))?",
    r"((\s)((minu|plus))(\s))?((\s)(-|\+)(\s))?(\s)(\d+)(\s)((\s)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\])(\s))?((\s)((degre|deg|grad))(\s))?(\s)((c|f|celsiu|celciu|fah|cel))(\s)((\s)((degre|deg|grad))(\s))?",
]


class TempPattern:
    temp_pattern = matcher_factory.merge_regular_expressions(temp_patterns)

    def extract(self, content):
        content = '   ' + '  '.join(matcher_factory.split_all_words(content)) + '    '
        results = list()
        all_iterator = self.temp_pattern.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            phrase = ' '.join([item.strip() for item in phrase.split(' ') if item != ''])
            results.append(phrase.strip())
        return results

    def replace(self, content):
        content = '   ' + '  '.join(matcher_factory.split_all_words(content)) + '    '
        return self.temp_pattern.sub(" _temp_ ", content)


if __name__ == '__main__':
    test = r"((([^\w]+?|^)(minu|plus)([^\w]+?|$))?(\s+?)(-|\+)?(\s+?)(\d+)(\s+?)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\])?(\s+?)(([^\w]+?|^)(degre|deg|grad)([^\w]+?|$))?(\s+?)(([^\w]+?|^)(c|f|celsiu|celciu|fah|cel)([^\w]+?|$))(\s+?)(([^\w]+?|^)(degre|deg|grad)([^\w]+?|$))?)"
    matches = re.finditer(
        r"((([^\w]+?|^)(minu|plus)([^\w]+?|$))?(\s*?)(-|\+)?(\s*?)(\d+)(\s*?)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\])?(\s*?)(([^\w]+?|^)(degre|deg|grad)([^\w]+?|$))?(\s*?)(([^\w]+?|^)(c|f|celsiu|celciu|fah|cel)([^\w]+?|$))(\s*?)(([^\w]+?|^)(degre|deg|grad)([^\w]+?|$))?)",
        "232     c     deg")
    matches = re.compile(
        r"((minu|plus)(\s))?((\s)-|\+(\s))?((\s)\d+(\s))((\s)[`=\[\];',/~!@#$%^&*()_+{}:<>?\\](\s))?((\s)(degre|deg|grad)(\s))?((\s)(c|f|celsiu|celciu|fah|cel)(\s))((\s)(degre|deg|grad)(\s))?")
    test = "minu+123c degre"
    print('  '.join(matcher_factory.split_all_words(test)))
    matches = matches.finditer(' ' + '  '.join(matcher_factory.split_all_words(test)))
    for match in matches:
        print(match.group(0))
