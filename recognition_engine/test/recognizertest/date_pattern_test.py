import unittest
import os, sys
parentPath = os.path.abspath("../..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from recognizer import DatePattern


class TestDatePattern(unittest.TestCase):

    def test_single_date(self):
        input_strs = [
            "4TH August @ 0700hrs then please!  :)",
            "29 July 2016 5:08 PM",
            "The desired vessel Kyoto Express has an estimated arrival in Southampton of 11 Aug 2016",
            "Sent: Tuesday, August 09, 2016 4:52 PMTo: OOCLLEVNVO/OUKL-CS",
            "Hi Please book to load 30.6.16  @ 10am for Shanghai load ref TT2419 40’hq – YARN – 8000 kgs YarnLoad address Sirdar Spinning ",
            "Hi Please book as per quote  00001719 – 16049 To load   16.8.16  9am",
            " BOOKING ACKNOWLEDGEMENT  DATE : 22 Jun 2016 16:40  FROM                        : Orient Overseas Container Line Limited - UK Branch",
            "Good Morning Thank you for booking with OOCL.As of 1st July 2016 all containers will require a verified gross mass (VGM) by law under the Safety of Lives at Sea (SOLAS) convention. "
        ]
        output_strs = [
            ['4TH August'],
            ['29 July 2016'],
            ['11 Aug 2016'],
            ['August 09, 2016'],
            ['30.6.16'],
            ['16.8.16'],
            ['22 Jun 2016'],
            ['1st July 2016']
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(DatePattern().extract(input_str), output_strs[idx])

    def test_multiple_date(self):
        input_strs = [
            "Thank you for booking with OOCL.The desired vessel Kyoto Express has an estimated arrival in Southampton of"
            " 11 Aug 2016 and therefore the first free date for receiving laden containers to quay is 4 Aug 2016.You have"
            "requested a shipment loading in Bury on 3 Aug 2016 which will incur 1 day demurrage;",

            "Hi Please book below as per our agreed rates attached On separate refs please Via Los Angeles to Pomona CA "
            "40gp To load Rosehill Polymers ringbank Mills Watson Mill Lane Halifax HX6 3BW To load 27.6.16 @ 10am load "
            "ref  23913 To load 27.6.16  @ 8am load ref  23912– 19000 kgs each  Rubber Granules AMS  FFCY Thanks Rachael"
        ]
        output_strs = [
            ['11 Aug 2016', '4 Aug 2016', '3 Aug 2016'],
            ['27.6.16', '27.6.16']
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(DatePattern().extract(input_str), output_strs[idx])


if __name__ == '__main__':
    unittest.main()
