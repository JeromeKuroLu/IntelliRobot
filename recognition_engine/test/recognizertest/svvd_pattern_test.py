import unittest
import os, sys
parentPath = os.path.abspath("../..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from recognizer import SvvdPattern


class TestSvvdPattern(unittest.TestCase):
    # def test_single_svvd_verify(self):
    #     # input_str = "RE: LATE EU24 Notification BKG# 2573863450 Vsl/Voy GEX1-MCA-104E Load Port MTR03 EU24 Cut Off Tuesday, 14 Jun 2016 15:00EDT Ref#"
    #     input_str = "RE: GEX2/006 RE: EXPORT COD REQUEST: GEX2-LOG-006 E/ LP5-HGI-004 E/ MAX-SJG-001 E   / bkg# 4038390821  ( / cntr:  OOLU613939-  ), Singapore: 7/20"
    #     print("Input: " + input_str)
    #     print(SvvdPattern().extract(input_str))

    def test_single_svvd_number(self):
        input_strs = [
            "RE: LATE EU24 Notification BKG# 2573863450 Vsl/Voy GEX1-MCA-104E Load Port MTR03 EU24 Cut Off Tuesday, 14 Jun 2016 15:00EDT Ref#",
            "TOP URGENT ///     2571972230   NP1-ZAN-034 W "
        ]
        output_strs = [
            ['GEX1-MCA-104 E'],
            ['NP1-ZAN-034 W'],
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(SvvdPattern.extract(input_str), output_strs[idx])


    def test_multiple_svvd_number(self):
        input_strs = [
            "RE: GEX2/006 RE: EXPORT COD REQUEST: GEX2-LOG-006 E/ LP5-HGI-004 E/ MAX-SJG-001 E   / bkg# 4038390821  ( / cntr:  OOLU613939-  ), Singapore: 7/20"
        ]
        output_strs = [
            ['GEX2-LOG-006 E', 'LP5-HGI-004 E', 'MAX-SJG-001 E']
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(SvvdPattern.extract(input_str), output_strs[idx])


if __name__ == '__main__':
    unittest.main()