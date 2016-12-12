import unittest
import os, sys
parentPath = os.path.abspath("../..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from recognizer import PhonePattern


class TestPhonePattern(unittest.TestCase):

    def test_single_date(self):
        input_strs = [
            "Tel 020 1473 659000               Company No. FC030216 Branch No. BR015210",
            "Laura Riley Direct Dial +44 01274 767425",
        ]
        output_strs = [
            ['020 1473 659000'],
            ['44 01274 767425']
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(PhonePattern().extract(input_str), output_strs[idx])

    def test_multiple_date(self):
        input_strs = [
            "Telephone: 01 274 727888 Direct Dial 123-456-789"
        ]
        output_strs = [
            ['01 274 727888', '123-456-789']
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(PhonePattern().extract(input_str), output_strs[idx])


if __name__ == '__main__':
    unittest.main()