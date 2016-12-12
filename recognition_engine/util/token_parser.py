import os, sys
parentPath = os.path.abspath("../..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from matcher_factory import split_array_by_nil
import nltk
import re


class TreeNode:
    def __init__(self):
        self.child = dict()

    def add_child_by_item(self, key_ref, child_node):
        self.child[key_ref] = child_node

    def __eq__(self, other):
        self_key_set = set()
        other_key_set = set()
        for child_key in self.child:
            self_key_set.add(child_key)
        for child_key in other.child:
            other_key_set.add(child_key)
        if len(self_key_set) != len(other_key_set):
            return False
        for child_key in other.child:
            if child_key not in self_key_set:
                return False
            flag = self.child[child_key].__eq__(other.child[child_key])
            if flag is False:
                return False
        return True


def modify_for_word(key, root_node, child_node):
    tmp_arr = key.split('ლ(╹◡╹ლ)')
    key_refs = tmp_arr[1].split('|')
    for key_item in key_refs:
        root_node.add_child_by_item(key_item, child_node)


def modify_for_number(key, root_node, child_node):
    tmp_arr = key.split('ლ(╹◡╹ლ)')
    limited = tmp_arr[1][1:]
    root_node.add_child_by_item(limited, child_node)


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

dealer_by_token = {
    '<word>': modify_for_word,
    '<sep>|<eSep>': modify_for_word,
    '<sep>': modify_for_word,
    '<eSep>': modify_for_word,
    '<number>': modify_for_number
}


def basic_tree_generator(patterns, end_mark):
    used_dict = dict()
    if len(patterns) == 0:
        return end_mark
    for pattern in patterns:
        if pattern == end_mark:
            used_dict[end_mark] = end_mark
            continue
        head_item = pattern[0]
        key_ref = 'ლ(╹◡╹ლ)'.join(head_item)
        if key_ref not in used_dict:
            used_dict[key_ref] = list()
        if len(pattern[1:]) > 0:
            used_dict[key_ref].append(pattern[1:])
        else:
            used_dict[key_ref].append(end_mark)
    root_node = TreeNode()
    for key in used_dict:
        cur_item = used_dict[key]
        if cur_item != end_mark and len(cur_item) >= 1:
            child_node = basic_tree_generator(cur_item, end_mark)
            if key.find('ლ(╹◡╹ლ)') != -1:
                dealer = dealer_by_token[key.split('ლ(╹◡╹ლ)')[0]]
                dealer(key, root_node, child_node)
            else:
                root_node.add_child_by_item(key, child_node)
        elif cur_item == end_mark:
            root_node.add_child_by_item(end_mark, end_mark)
    return root_node


def merge_trees(tree_one, tree_two):
    result_tree = TreeNode()
    for child_key in tree_two.child:
        result_tree.add_child_by_item(child_key, tree_two.child[child_key])
    for child_key in tree_one.child:
        if child_key not in tree_two.child:
            result_tree.child[child_key] = tree_one.child[child_key]
        elif child_key in tree_two.child and isinstance(tree_two.child[child_key], type('string')):
            continue
        elif child_key in tree_two.child:
            result_tree.child[child_key] = merge_trees(tree_one.child[child_key], tree_two.child[child_key])
    return result_tree


def concat_2d_list(target_list, source_list):
    for item_arr in target_list:
        source_list.append(item_arr)


class TokenMatcher:
    def __init__(self):
        self.result_list = list()
        self.current_match_word = list()
        self.root_tree = None
        self.current_node = None
        self.patterns = None
        self.grammar_item = set()
        self.stack_cache = list()
        self.token_list = {
            '<number>': re.compile('\\d+'),
            '<word>': re.compile('\\w+'),
            'month': re.compile('Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?', re.IGNORECASE),
            '<sep>': re.compile("[" + r"`=\[\];',/~!@#$%^&*()_+{}:<>?\\" + "]"),
            '<eSep>': re.compile("[" + r"`\-=\[\];',./~!@#$%^&*()_+{}:<>?\\" + "]")
        }

    def build_up_pattern(self, patterns):
        self.patterns = dict()
        for key in patterns:
            self.patterns[key] = basic_tree_generator(patterns[key], key)
            self.root_tree = self.patterns[key]
            self.grammar_item.add(key)
        for key in self.patterns:
            self.root_tree = merge_trees(self.root_tree, self.patterns[key])

    def get_pattern(self, target_word):
        if self.token_list['<number>'].match(target_word):
            return '<number>', '#' + str(len(target_word))
        for token in self.token_list:
            if self.token_list[token].match(target_word):
                return token
        return None

    def has_basic_token(self, node):
        for key in node.child:
            if key in self.patterns and not isinstance(node.child[key], type('string')):
                return True
        return False

    def findAll(self, contents):
        word_list = nltk.word_tokenize(contents)
        self.current_node = self.root_tree
        cur_index = 0
        while cur_index < len(word_list):
            can_step = True
            target_word = word_list[cur_index]
            for end_mark in self.grammar_item:
                if end_mark in self.current_node.child and isinstance(self.current_node.child[end_mark], type('string')):
                    self.result_list.append(''.join(self.current_match_word))
                    self.current_match_word = list()
                    self.current_node = self.root_tree
                    word_list.insert(cur_index, end_mark)
                    if len(self.stack_cache) != 0:
                        recover = self.stack_cache.pop()
                        self.current_match_word, self.current_node = recover
                    can_step = False
            if can_step is False:
                continue
            cur_pattern = self.get_pattern(target_word)
            if target_word in self.current_node.child:
                self.current_node = self.current_node.child[target_word]
                self.current_match_word.append(target_word)
            elif isinstance(cur_pattern, type((1, 2))) and cur_pattern[1] in self.current_node.child:  # handle <number>, #12
                self.current_node = self.current_node.child[cur_pattern[1]]
                self.current_match_word.append(target_word)
            elif isinstance(cur_pattern, type((1, 2))) and cur_pattern[0] in self.current_node.child:  # if not #12, then <number>
                self.current_node = self.current_node.child[cur_pattern[0]]
                self.current_match_word.append(target_word)
            elif cur_pattern in self.current_node.child:
                self.current_node = self.current_node.child[cur_pattern]
                self.current_match_word.append(target_word)
            elif self.has_basic_token(self.current_node):
                self.stack_cache.append((self.current_match_word, self.current_node))
                self.current_node = self.root_tree
            else:
                self.current_node = None
            if self.current_node is None:
                self.current_match_word = list()
            cur_index += 1


if __name__ == "__main__":
    test_arr = list()
    test_arr.append([['<word>|nil', 'minu|plus'], ['<sep>|<eSep>|nil', '-|+'], ['<number>'], ['<sep>|nil', ],
                     ['<word>|nil', 'degre|deg|grad'], ['<word>', 'c|f|celsiu|celciu|fah|cel'],
                     ['<word>|nil', 'degre|deg|grad']])
    # test_arr.append([['<word>|nil', 'set'], ['<word>', 'temperatur|temp'], ['<word>|nil', 'set'], ['<sep>|<eSep>|nil'],
    #                  ['<word>|nil', 'need'], ['<word>|nil', 'at|to'], ['<word>|nil', 'be'], ['Temperature']])
    # test_arr.append([['<word>|nil', 'pre'], ['<eSep>', '-'], ['<word>', 'set'], ['<word>', 'temperatur|temp'],
    #                  ['<word>|nil', 'at|to'], ['<word>|nil', 'be'], ['Temperature']])
    # test_arr.append([['Temperature'], ['<word>', 'temperatur|temp'], ['<word>|nil', 'set']])
    test_arr.append(
        [['<number>|nil'], ['<sep>|nil', '%'], ['<word>', 'humid'], ['<word>|nil', 'sensor'], ['<word>|nil', 'moistur'],
         ['<word>|nil', 'percentag'], ['<sep>|nil', '%'], ['<number>|nil']])
    settings_arr = list()
    settings_arr.append(
        [['<word>|nil', 'set'], ['<word>', 'temperatur|temp'], ['<word>|nil', 'set'], ['<sep>|<eSep>|nil'],
         ['<word>|nil', 'need'], ['<word>|nil', 'at|to'], ['<word>|nil', 'be'], ['Temperature']])
    settings_arr.append([['<word>|nil', 'pre'], ['<eSep>', '-'], ['<word>', 'set'], ['<word>', 'temperatur|temp'],
                         ['<word>|nil', 'at|to'], ['<word>|nil', 'be'], ['Temperature']])
    settings_arr.append([['Temperature'], ['<word>', 'temperatur|temp'], ['<word>|nil', 'set']])
    result_arr = list()
    tmp = None
    for arr in test_arr:
        # print(arr)
        tmp = split_array_by_nil(arr)
        concat_2d_list(tmp, result_arr)
    result_arr2 = list()
    for arr in settings_arr:
        tmp = split_array_by_nil(arr)
        concat_2d_list(tmp, result_arr2)
    match_grammar = {
        'Temperature': result_arr,
        'Settings': result_arr2
    }
    matcher = TokenMatcher()
    matcher.build_up_pattern(match_grammar)
    match_tree = dict()
    for key in match_grammar:
        match_tree[key] = basic_tree_generator(match_grammar[key], key)
    tree = merge_trees(match_tree['Temperature'], match_tree['Settings'])
    tree1 = TreeNode()
    print(tree == matcher.root_tree)

    print(split_all_words("1234%humid sensor moistur percentag% minu+123c degre temp set"))
    # result_arr = list()
    # tmp = None
    # for arr in test_arr:
    #     # print(arr)
    #     tmp = split_array_by_nil(arr)
    #     concat_2d_list(tmp, result_arr)
    # for item in result_arr:
    #     print(item)
    # tree = basic_tree_generator(result_arr, 'End')
    # print(tree)
