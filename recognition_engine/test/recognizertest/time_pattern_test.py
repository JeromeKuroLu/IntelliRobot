import unittest
import os, sys
parentPath = os.path.abspath("../..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from recognizer import TimePattern


class TestTimePattern(unittest.TestCase):

    def test_single_date(self):
        input_strs = [
            "Sent: Tuesday, August 09, 2016 9:09 PM",
            "Load at 10:30 am",
        ]
        output_strs = [
            ['9:09 PM'],
            ['10:30 am']
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(TimePattern().extract(input_str), output_strs[idx])

    def test_multiple_date(self):
        input_strs = [
            "Sent: Tuesday, August 09, 2016 9:09 PM, arrive at 10:48 AM",
            "10    :  30  am   19  :    51   pm"
        ]
        output_strs = [
            ['9:09 PM', '10:48 AM'],
            ['10:30 am', '19:51 pm']
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(TimePattern().extract(input_str), output_strs[idx])


if __name__ == '__main__':
    unittest.main()