import re


def parse_all_bl_number(content):
    bl_number_pattern = [
        r"(this)?(\s*)(draft)?(\s*)(b)(\s*)(/)(\s*)(l)(\s*)(#)?(\s*)(no)?(\s*)(\.)?(\s*)(oolu)?(\s*)(\d{10})",
        r"(this)?(\s*)(draft)?(\s*)(bl)(\s*)(#)?(\s*)(-)?(\s*)(:)?(\s*)(no\|number)?(\s*)(\.)?(\s*)(is)?(\s*)(oolu)?(\s*)(\d{10})",
        r"(this)?(\s*)(MBL)(\s*)(no)?(\s*)(:\|\.)?(\s*)(oolu)?(\s*)(\d{10})",
        r"(mbl)(\s*)(no)?(\s*)(:)?(\s*)(oolu)?(\s*)(\d{10})",
        r"(oolu)(\s*)(\d{10})",
        r"(bill)(\s*)(for)?(\s*)(\d{10})"
    ]
    bl_regular_expression = merge_regular_expressions(bl_number_pattern)
    return bl_regular_expression.finditer(content)


def split_all_words(contents):
    result_list = list()
    cache_block = list()
    word_pattern = re.compile(r'\w')
    space_pattern = re.compile(r'\s')
    num_pattern = re.compile(r'\d')
    status = 0  # 0 for \s, 1 for word, 2 for number, 3 for other
    for single_char in contents:
        if num_pattern.match(single_char):
            if status != 2 and len(cache_block) != 0:
                result_list.append(''.join(cache_block))
                cache_block = list()
            status = 2
            cache_block.append(single_char)
        elif word_pattern.match(single_char):
            if status != 1 and len(cache_block) != 0:
                result_list.append(''.join(cache_block))
                cache_block = list()
            status = 1
            cache_block.append(single_char)
        elif space_pattern.match(single_char):
            status = 0
        else:
            if status != 3 and len(cache_block) != 0:
                result_list.append(''.join(cache_block))
                cache_block = list()
            status = 3
            result_list.append(single_char)
    if len(cache_block) != 0:
        result_list.append(''.join(cache_block))
    return result_list


def parse_all_bkg_number(content):
    bkg_number_pattern = [
        r"(booking)(\s*)(number)?(\s*)(no)?(\s*)(is)?(\s*)(#|:)?(\s*)(\.)?(\s*)(oolu)?(\s*)(\d{10})",
        r"(book)(\s*)(number)?(\s*)(no)?(\s*)(is)?(\s*)(#|:)?(\s*)(\.)?(\s*)(oolu)?(\s*)(\d{10})",
        r"(\d{10})(\s*)(booking)(\s*)(number|no)",
        r"(shipment)(\s*)(number|no)?(\s*)(\d{10})",
        r"(booking|book)(\s*)(#)?(\s*)(:)?(\s*)(\d{10})",
        r"(\d{10})(\s*)(-)?(\s*)(oocl)(\s*)(booking)",
    ]
    bkg_regular_expression = merge_regular_expressions(bkg_number_pattern)
    return bkg_regular_expression.finditer(content)


def merge_regular_expressions(expressions):
    expressions = ['(' + item + ')' for item in expressions]
    # print('|'.join(expressions))
    return re.compile('|'.join(expressions), re.IGNORECASE | re.DOTALL)


def merge_regular_expressions_in_raw_string(expressions):
    expressions = ["(" + item + ")" for item in expressions]
    return '(' + '|'.join(expressions) + ')'


def generate_regular_string(target_string):
    loc = locals()
    exec('result_arr = ' + target_string)
    result_arr = loc['result_arr']
    result_regex = list()
    for item in result_arr:
        result_regex.append(generate_regular_string_by_item(item))
    return '(\s*)'.join(result_regex)


def generate_regular_string_by_item(item):
    meta_char = set()
    # ignore | character because it may use inside the word
    char_set = ['.', '^', '$', '*', '+', '?', '{', '[', ']', '\\', '(', ')']
    replace_items = {
        '<number>': '\\d+',
        '<word>': '\\w+',
        'month': 'Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?',
        '<sep>': "[" + r"`=\[\];',/~!@#$%^&*()_+{}:<>?\\" + "]",
        '<eSep>': "[" + r"`\-=\[\];',./~!@#$%^&*()_+{}:<>?\\" + "]"
    }
    specified_handler = {
        '<number>': lambda x: '\\d{' + x[1:] + '}',
    }
    for char in char_set:
        meta_char.add(char)
    choices = [single_item.strip() for single_item in item[0].split('|')]
    result = ''
    if item[0] not in specified_handler and len(item) > 1:
        for char in item[1]:
            if char in char_set:
                result += '\\'
            result += char
    elif len(item) == 1:
        replaces = [replace_items[key] for key in choices if key in replace_items]
        result = '|'.join(replaces)
    else:
        result = specified_handler[item[0]](item[1])
    if 'nil' not in choices:
        return '(' + result + ')'
    else:
        return '(' + result + ')?'


def shallow_copy(target_list):
    return [item for item in target_list]


def split_array_by_nil(target_array):
    result_array = list()
    current_array = list()
    for index in range(len(target_array)):
        array_item = target_array[index]
        has_nil = (array_item[0].split('|')[-1] == 'nil')
        if has_nil is True:
            new_arrays = split_array_by_nil(target_array[index + 1:])
            not_current = [shallow_copy(current_array) + item for item in new_arrays]
            result_array += not_current
            array_item[0] = '|'.join(array_item[0].split('|')[:-1])
            current_array.append(array_item)
            has_current = [shallow_copy(current_array) + item for item in new_arrays]
            result_array += has_current
        else:
            current_array.append(array_item)
    result_array.append(current_array)
    true_result = list()
    [true_result.append(i) for i in result_array if i not in true_result]
    return true_result


class TokenParser:
    def __init__(self):
        self.token_list = {
            '<number>': '\\d+',
            '<word>': '\\w+',
            'month': 'Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?',
            '<sep>': "[" + r"`=\[\];',/~!@#$%^&*()_+{}:<>?\\" + "]",
            '<eSep>': "[" + r"`\-=\[\];',./~!@#$%^&*()_+{}:<>?\\" + "]"
        }
        self.word_list = list()
        self.meta_pattern = re.compile(r"\w+")

    def generate_regular_string_by_item(self, item):
        meta_char = set()
        # ignore | character because it may use inside the word
        char_set = ['.', '^', '$', '*', '+', '?', '{', '[', ']', '\\', '(', ')']
        specified_handler = {
            '<number>': lambda x: '\\d{' + x[1:] + '}',
            '<word>': lambda x: r'(' + x + ')',
            '<word>|nil': lambda x: r'(' + x + ')',
        }
        for char in char_set:
            meta_char.add(char)
        choices = [single_item.strip() for single_item in item[0].split('|')]
        result = ''
        if item[0] not in specified_handler and len(item) > 1:
            if choices[0] in specified_handler:
                result = specified_handler[choices[0]](item[1])
            else:
                for char in item[1]:
                    if char in char_set:
                        result += '\\'
                    result += char

        elif len(item) == 1:
            replaces = [self.token_list[key] for key in choices if key in self.token_list]
            if self.judge_is_meta(item[0]) is False:
                replaces.append("TOKEN_FOR_META")
            result = '|'.join(replaces)

        else:
            result = specified_handler[item[0]](item[1])
        if 'nil' not in choices:
            return r'(\s)(' + result + r')(\s)'
        else:
            return r'((\s)(' + result + r')(\s))?'

    @staticmethod
    def generate_pattern_by_list(target_list):
        return "".join(target_list)

    def generate_all_pattern(self, patterns):
        all_result_list = list()
        for target_string in patterns:
            result_regex = list()
            loc = locals()
            exec('result_arr = ' + target_string)
            result_arr = loc['result_arr']
            is_meta = True
            for item in result_arr:
                meta_res = self.judge_is_meta(item[0])
                if meta_res is False:
                    is_meta = False
                result_regex.append(self.generate_regular_string_by_item(item))
            if is_meta:
                self.word_list.append(self.generate_pattern_by_list(result_regex))
            all_result_list.append(self.generate_pattern_by_list(result_regex))
        token_regex = merge_regular_expressions_in_raw_string(self.word_list)  # generate token value
        all_result_list = self.sort_by_dependency(all_result_list)  # move all pattern contains a token to tail
        all_result_list = [result_item.replace("(\s)(TOKEN_FOR_META)(\s)", token_regex) for result_item in
                           all_result_list]  # replace token with token value
        return all_result_list

    def generate_all_pattern_by_array(self, patterns):
        all_result_list = list()
        for result_arrs in patterns:
            result_arrs = split_array_by_nil(result_arrs)
            for result_arr in result_arrs:
                result_regex = self.generate_pattern_by_pure_array(result_arr)
                all_result_list.append(self.generate_pattern_by_list(result_regex))
        self.word_list.sort(key=len, reverse=True)
        token_regex = merge_regular_expressions_in_raw_string(self.word_list)  # generate token value
        all_result_list = self.sort_by_dependency(all_result_list)  # move all pattern contains a token to tail
        all_result_list = [result_item.replace("TOKEN_FOR_META", token_regex) for result_item in
                           all_result_list]  # replace token with token value
        all_result_list.sort(key=len, reverse=True)
        return all_result_list

    def generate_pattern_by_pure_array(self, result_arr):
        is_meta = True
        result_regex = list()
        tmp_word_list = list()
        has_other = False
        for index in range(len(result_arr)):
            item = result_arr[index]
            meta_res = self.judge_is_meta(item[0])
            if meta_res is False:
                is_meta = False
            if item[0] != '<word>':
                has_other = True
                if len(tmp_word_list) > 0:
                    if len(result_regex) == 0:
                        result_regex.append(self.merge_word_list(tmp_word_list, '([^\w]|^)', ''))
                    else:
                        result_regex.append(self.merge_word_list(tmp_word_list, '', ''))
                    tmp_word_list = list()
                result_regex.append(self.generate_regular_string_by_item(item))
            else:
                tmp_word_list.append(item)
        if len(tmp_word_list) > 0 and has_other:  # if has o
            result_regex.append(self.merge_word_list(tmp_word_list, '', '([^\w]|$)'))
        elif len(tmp_word_list) > 0:
            result_regex.append(self.merge_word_list(tmp_word_list, '([^\w]|^)', '([^\w]|$)'))
        if is_meta:
            self.word_list.append(self.generate_pattern_by_list(result_regex))
        return result_regex

    @staticmethod
    def merge_word_list(tmp_list, start, end):
        if len(tmp_list) <= 0:
            return None
        new_list = list()
        for item in tmp_list:
            if len(item) > 0:
                new_list.append("(" + item[1] + ")")
            else:
                new_list.append("(\w+)")
        result_regex = '([^\w]+)'.join(new_list)
        return start + result_regex + end

    @staticmethod
    def sort_by_dependency(result_list):
        start_index = 0
        end_index = len(result_list) - 1
        while start_index != end_index:
            if result_list[start_index].find("TOKEN_FOR_META") == -1:
                tmp_str = result_list[end_index]
                result_list[end_index] = result_list[start_index]
                result_list[start_index] = tmp_str
                end_index -= 1
            else:
                start_index += 1
        return result_list

    def judge_is_meta(self, item):
        tmp_arr = item.split('|')
        for token in tmp_arr:
            if self.meta_pattern.match(token) and token != 'nil':
                return False
        return True


if __name__ == '__main__':
    # print('_______________________________________________________________')

    # date_patterns = [
    #     r"[ ['<number>'], ['<sep>|<eSep>','.|/|*|:'], ['<number>'],['<sep>|<eSep>','.|/|*|:'],['<number>']  ]",
    #     r" [ ['<number>'], ['month'], ['<sep>|<eSep>|nil',',|.|/|*|:'], ['<number>'] ]",
    #     r" [ ['<number>'], ['<word>','of'], ['month'], ['<sep>|<eSep>|nil',',|.|/|*|:'], ['<number>'] ]",
    #     r"[ ['<number>'], ['<word>','of'], ['month'] ]",
    #     r" [ ['month'], ['<sep>|<eSep>|nil','.|/|*|:'], ['<number>'], ['<word>|nil','th|st|nd'], ['<sep>|<eSep>|nil'], ['<number>'] ]",
    #     r" [ ['month'], ['<sep>|<eSep>|nil','.|/|*|:'], ['<number>'], ['<word>|nil','th|st|nd'] ]",
    #     r"[ ['<number>'], ['<sep>', '/'], ['<number>'] ]",
    #     r"[ ['<word>', 'date' ],  ['<sep>|<eSep>|nil','.|/|*|:'], ['<number>'] ]",
    #     r"[ ['<word>', 'pol|pod' ],  ['<sep>|<eSep>','.|/|*|:'], ['<number>'] ]",
    #     r"[ ['<number>'], ['<word>|nil','th|st|nd'],['<sep>|<eSep>|nil'], ['month'],['<sep>|<eSep>|nil','.|/|*|:'],['<number>|nil'] ]",
    #     r"[['<word>', 'date'], ['<sep>|nil', ':'], ['date'] ]"
    # ]
    #
    # for date_pattern in date_patterns:
    #     print("r\"" + generate_regular_string(date_pattern) + "\",")

    temp_patterns = [
        [ ['<word>|nil', 'minu|plus'], ['<sep>|<eSep>|nil','-|+'], ['<number>'], ['<sep>|nil',], ['<word>|nil', 'degre|deg|grad'], ['<word>', 'c|f|celsiu|celciu|fah|cel'], ['<word>|nil', 'degre|deg|grad'] ],
        [ ['<number>|nil'], ['<sep>|nil', '%'], ['<word>', 'humid'], ['<word>|nil', 'sensor'], ['<word>|nil','moistur'], ['<word>|nil','percentag'],['<sep>|nil','%'], ['<number>|nil']  ],
        [ ['<word>|nil', 'set'], ['<word>', 'temperatur|temp'], ['<word>|nil', 'set'], ['<sep>|<eSep>|nil'], ['<word>|nil','need'], ['<word>|nil', 'at|to'],['<word>|nil', 'be'], ['Temperature']  ],
        [ ['<word>|nil', 'pre'], ['<eSep>','-'], ['<word>', 'set'], ['<word>', 'temperatur|temp'], ['<word>|nil', 'at|to'], ['<word>|nil', 'be'], ['Temperature'] ],
        [ ['Temperature'], ['<word>', 'temperatur|temp'], ['<word>|nil', 'set'] ],
    ]
    temp_patterns_str = [
        r"[ ['<word>|nil', 'minu|plus'], ['<sep>|<eSep>|nil','-|+'], ['<number>'], ['<sep>|nil',], ['<word>|nil', 'degre|deg|grad'], ['<word>', 'c|f|celsiu|celciu|fah|cel'], ['<word>|nil', 'degre|deg|grad'] ]",
        r"[ ['<number>|nil'], ['<sep>|nil', '%'], ['<word>', 'humid'], ['<word>|nil', 'sensor'], ['<word>|nil','moistur'], ['<word>|nil','percentag'],['<sep>|nil','%'], ['<number>|nil']  ]",
        r"[ ['<word>|nil', 'set'], ['<word>', 'temperatur|temp'], ['<word>|nil', 'set'], ['<sep>|<eSep>|nil'], ['<word>|nil','need'], ['<word>|nil', 'at|to'],['<word>|nil', 'be'], ['Temperature']  ]",
        r"[ ['<word>|nil', 'pre'], ['<eSep>','-'], ['<word>', 'set'], ['<word>', 'temperatur|temp'], ['<word>|nil', 'at|to'], ['<word>|nil', 'be'], ['Temperature'] ]",
        r"[ ['Temperature'], ['<word>', 'temperatur|temp'], ['<word>|nil', 'set'] ]",
    ]

    parser1 = TokenParser()
    parser1.generate_all_pattern(temp_patterns_str)

    test_arr = [['<word>|nil', 'minu|plus'], ['<sep>|<eSep>|nil', '-|+'], ['<number>'], ['<sep>|nil', ],
                ['<word>|nil', 'degre|deg|grad'], ['<word>', 'c|f|celsiu|celciu|fah|cel'],
                ['<word>|nil', 'degre|deg|grad']]
    # test_arr = [ ['<word>|nil', 'pre'], ['<eSep>','-'], ['<word>', 'set'], ['<word>', 'temperatur|temp'], ['<word>|nil', 'at|to'], ['<word>|nil', 'be'], ['Temperature'] ]
    test_arr1 = split_array_by_nil(test_arr)
    print("start")
    for item in test_arr1:
        print(item)
    print(len(test_arr1))
    phone_patterns = [
        r"[ ['<number>'], ['<eSep>|nil'], ['<number>'],['<eSep>|nil'],['<number>']   ]"
    ]
    parser = TokenParser()
    # all_results = parser.generate_all_pattern_by_array(test_arr)
    all_results = parser1.generate_all_pattern(temp_patterns_str)
    for result in all_results:
        print("r\"" + result + "\",")
    # test_arr2 = parser.generate_all_pattern_by_array(temp_patterns)
    # for result in test_arr2:
    #     print("r\"" + result + "\",")
    # print(merge_regular_expressions_in_raw_string(parser.word_list))
    # print(parser.word_list)
