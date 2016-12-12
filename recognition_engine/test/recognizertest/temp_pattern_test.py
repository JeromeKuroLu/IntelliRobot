import unittest
import os, sys
parentPath = os.path.abspath("../..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from recognizer import TempPattern


class TestTempPattern(unittest.TestCase):

    def test_single_date(self):
        input_strs = [
            "232 c deg",
            "232c",
            "minu+123c degre",
            "pre-set temp  232 c deg hello",
            "minu+123c degre temp set"
        ]
        output_strs = [
            ['232 c deg'],
            ['232 c'],
            ['minu + 123 c degre'],
            ['pre - set temp 232 c deg'],
            ['minu + 123 c degre temp set']
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(TempPattern().extract(input_str), output_strs[idx])

    def test_multiple_date(self):
        input_strs = [
            "232c 232 c minu+232c deg",
            "1234%humid sensor moistur percentag% minu+123c degre temp set",
            "232c deg pre-set temp 232 c deg minu+123c degre "
        ]
        output_strs = [
            ['232 c', '232 c', 'minu + 232 c deg'],
            ['1234 % humid sensor moistur percentag %', 'minu + 123 c degre temp set'],
            ['232 c deg', 'pre - set temp 232 c deg', 'minu + 123 c degre']
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(TempPattern().extract(input_str), output_strs[idx])


if __name__ == '__main__':
    unittest.main()