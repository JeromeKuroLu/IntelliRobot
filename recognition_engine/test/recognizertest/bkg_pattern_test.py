import unittest
import os, sys
parentPath = os.path.abspath("../..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from recognizer import BkgPattern


class TestBkgPattern(unittest.TestCase):
    # def test_single_bkg_number_verify(self):
    #     input_str = "FW: CONFIRMATION OF ACTUAL BKG SEAL OOLU9581541111 2570021606"
    #     print("Input: " + input_str)
    #     print(BkgPattern().extract(input_str))

    def test_single_bkg_number(self):
        input_strs = [
            "RE: Booking ref: 4024116670 asd",
            "RE: [-[2573038911 ]-]FW: bkg# 2573038911 // 365-3429156",
            "RE: AX2/001 RE: EXPORT COD REQUEST: AX2 SPH 010 E- BKG #4038232240- (Cntr # CAXU724157-5/40GP)- ETA BRV  5/23; HSL: 6/2- (NAGC CB)",
            "Bill instructions + B13 for booking# 4038676030",
            "RE: URGENT URGENT URGENT 2nd REVISED BOL INSTRUCTIONS FOR BOOKING#4038559170   SO#5500169566 LII 302-058609   INVISTA TEXTILES",
            "BL for booking 2022717000/ S00041219/ PO# P95828",
            "FW: Need corrected invoice CAYUL 470516  OOLU 2022686530 - Rotterdam - 2nd Reminder",
            "RE: 3rd request =  US24 FROB/JP24/CN24 Status - Incomplete Shipping Instructions --4038710390     NP3-HVX-063 W VAN - ETA 6/9 - cutoff",
            "BKG NO. 2573203530",
            "RE: Booking 2022547511  POS  6500591950,6500591951,6500591952",
            "RE : Booking 4999921740"
        ]
        output_strs = [
            ['4024116670'],
            ['2573038911'],
            ['4038232240'],
            ['4038676030'],
            ['4038559170'],
            ['2022717000'],
            ['2022686530'],
            ['4038710390'],
            ['2573203530'],
            ['2022547511'],
            ['4999921740']
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(BkgPattern.extract(input_str), output_strs[idx])

    def test_multiple_bkg_number(self):
        input_strs = [
            "FW: CONFIRMATION OF ACTUAL BKG OOLU9581541111 2570021606",
            "RE: Late EU24 SI Notification BKG# 4038467050;4038467051 Vsl/Voy AZX-RBW-009W Load Port HAL02"
            " EU24 SI Cut Off Wednesday, 08 Jun 2016 17:00EDT Ref# ",
            "RE: [-[]-]FW: [Urgent] (SC) RE: SUPER URGENT!!! PUT CONTAINERS ON HOLD. BOOKING:  4038575541, "
            "4038575521, 4038575540, 4038575520"

        ]
        output_strs = [
            ['9581541111', '2570021606'],
            ['4038467050', '4038467051'],
            ['4038575541', '4038575521', '4038575540', '4038575520']
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(BkgPattern.extract(input_str), output_strs[idx])


if __name__ == '__main__':
    unittest.main()