import unittest
import os, sys
parentPath = os.path.abspath("../..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import reshape_util


class TestReshapeContent(unittest.TestCase):

    def test_reshape(self):
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
            '_Date_ @ 0700 hrs then please ! : )',
            '_Date_ _time_',
            'The desired vessel _City_ Express has an estimated arrival in _City_ of _Date_',
            'Sent : Tuesday , _Date_ _time_ To : OOCLLEVNVO / OUKL - CS',
            'Hi Please book to load _Date_ @ _time_ for _City_ load ref TT 2419 40 ’ hq – YARN – 8000 kgs YarnLoad address Sirdar Spinning',
            'Hi Please book as per quote 00001719 – 16049 To load _Date_ _time_',
            'BOOKING ACKNOWLEDGEMENT _Date_ 16 : 40 FROM : _City_ Overseas Container Line Limited - UK _City_',
            'Good Morning Thank you for booking with OOCL . As of _Date_ all containers will require a verified gross mass ( VGM ) by law under the Safety of Lives at Sea ( _City_ ) convention .'
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(reshape_util.reshape_content(input_str), output_strs[idx])


if __name__ == '__main__':
    unittest.main()
