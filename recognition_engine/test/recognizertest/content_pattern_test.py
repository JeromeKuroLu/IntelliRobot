import unittest
import os, sys

parentPath = os.path.abspath("../..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from recognizer import ContentPattern


class TestContentPattern(unittest.TestCase):
    def test_single_date(self):
        input_strs = [
            '''
            Please can we book 1 x 20’GP container, released merchant haulage for shipment to CFR Montreal – including Dest THC.

Please confirm container release depot address?



Quotation Folder: 00000661 / Doc 16061



We will collect empty from Thursday 23rd June

Export laden container can be returned to quay by Friday 24th June



Commodity: Non Haz – Steel Bars

Gross weight: 24,000 kgs



Our file ref: DE0163200



UCR: 6GB238712260000-DE0163200



Will await your confirmation. Many thanks



Regards

Emma Wood

Direct Dial +44 (0)1274 767422

WWW.ZEN-INTL.CO.UK <http://www.zen-intl.co.uk/>



Zenith House, Valley Court, Bradford. BD1 4SP

Telephone: 01274 727888 / Fax: 01274 727999



""The Company operates under BIFA Standard Trading Conditions latest edition, a copy of which is available upon request.""

""Zenith International Freight Ltd. is a limited company registered in England No. 3801743""



Unless Otherwise stated all prices exclude any customs clearance, duties, taxes and final delivery costs in the country of destination. The above is calculated at today's costs and rates of exchange, which are subject to alteration at the time of shipment.


"

            ''',
            '''
            Please can we make the following booking:



Equipment:  2 x 40'GP containers

Destination: CFR Busan, Korea - Quotation FE201203



UCR: 6GB114536492000-DE0163923



VGM: ZENITHINT*DE0163923*TL



Commodity: Iron Bars

Gross weight: approx 24,300 kgs



Load Address:

SHS Freight

Riverside Development

Chesterton Road

Eastwood Trading Estate

Rotherham

S65 1SU



Date / Time:

Thursday 4th August

@ 0800 hrs – Driver to quote: UCB 19388

@ 1000 hrs – Driver to quote: UCB 19389



Our file ref: DE0163923



Will await your confirmation.



Regards

Emma Wood

Direct Dial +44 (0)1274 767422

WWW.ZEN-INTL.CO.UK <http://www.zen-intl.co.uk/>



Zenith House, Valley Court, Bradford. BD1 4SP

Telephone: 01274 727888 / Fax: 01274 727999



""The Company operates under BIFA Standard Trading Conditions latest edition, a copy of which is available upon request.""

""Zenith International Freight Ltd. is a limited company registered in England No. 3801743""



Unless Otherwise stated all prices exclude any customs clearance, duties, taxes and final delivery costs in the country of destination. The above is calculated at today's costs and rates of exchange, which are subject to alteration at the time of shipment.


"

            ''',
            '''
            Your: 4024150400

Our: DE0163016



Please can we amend loading time to 1000 hrs - Mon 27th June



Regards

Emma Wood

Direct Dial +44 (0)1274 767422



From: Emma Wood
Sent: 08 June 2016 12:21
To: 'OOCLLEVNVO@oocl.com' <OOCLLEVNVO@oocl.com>
Cc: 'claire.ling@oocl.com' <claire.ling@oocl.com>; Malcolm Chilton <malc@zen-intl.co.uk>
Subject: Booking to Mississauga



Please can we make the following booking:

　

Equipment: 1 x 20’GP container

Destination: DAP Mississauga, ON – Quotation, Awaiting detail from Claire, rate detailed below



UCR: 6GB560982715000-EXP211729AR



Commodity:  Hazardous Class 8 Chemicals – DGN attached

Gross weight: 20,280 kgs



Load Address:

Chemtura

Tenax Road

Trafford Park

Manchester

M17 1WT

Driver to Quote: 845626 / 290040



Please DO NOT use Freightliner for transport – Shipper will not allow on site



Date / Time:

Monday 27th June @ 1400 hrs



Our file ref: DE0163016



Will await your confirmation. Many thanks



Regards

Emma Wood

Direct Dial +44 (0)1274 767422



SOLAS NEWS UPDATED

HAVE YOU REGISTERED YET WITH THE MCA TO BECOME A VERIFIED WEIGHER OF YOUR SHIPMENTS ?

Please refer to the following Link

https://www.gov.uk/government/publications/verification-of-the-gross-mass-of-packed-containers-by-sea <https://www.gov.uk/government/publications/verification-of-the-gross-mass-of-packed-containers-by-sea>

If clarification is required, please don’t hesitate to contact Zenith for assistance.



WWW.ZEN-INTL.CO.UK <http://www.zen-intl.co.uk/>



Zenith House, Valley Court, Bradford. BD1 4SP

Telephone: 01274 727888 / Fax: 01274 727999



""The Company operates under BIFA Standard Trading Conditions latest edition, a copy of which is available upon request.""

""Zenith International Freight Ltd. is a limited company registered in England No. 3801743""



Unless Otherwise stated all prices exclude any customs clearance, duties, taxes and final delivery costs in the country of destination. The above is calculated at today's costs and rates of exchange, which are subject to alteration at the time of shipment.





From: claire.ling@oocl.com <mailto:claire.ling@oocl.com>  [mailto:claire.ling@oocl.com]
Sent: 13 May 2016 11:15
To: Malcolm Chilton <malc@zen-intl.co.uk <mailto:malc@zen-intl.co.uk> >
Cc: craig.purves@oocl.com <mailto:craig.purves@oocl.com>
Subject: FW: Business Opportunity / Zenith



Hi Malc, further to clarification from Trade.

The max cargo weight is 20.87 tons/20. So if the shipment over 20.87 tons/20, it cannot be accepted.



For weight less than 20.87tons my rate offer can be used.



regards Claire



regards



Claire Ling

Inside Sales Coordinator

OOCL UK Branch

Tel. +44 1473 654222



Going Green:  We take it personally

for Sustainability





From: claire.ling@oocl.com <mailto:claire.ling@oocl.com>  [mailto:claire.ling@oocl.com]
Sent: 12 May 2016 12:34
To: Malcolm Chilton <malc@zen-intl.co.uk <mailto:malc@zen-intl.co.uk> >
Cc: craig.purves@oocl.com <mailto:craig.purves@oocl.com> ; hannah.mccarthy@oocl.com <mailto:hannah.mccarthy@oocl.com>
Subject: FW: Business Opportunity / Zenith



Hi Malc, thanks for the opportunity to review the below.



Based on the information provided, we can match your target rates as follows:-



20GP Approx 4/5x20 per month.



Door Trafford Park to Door Mississauga Ont.



FAK / HAZ Class 8, subject to vessel acceptance at time of booking

Non Haz = 20GP/ USD2525.

Haz Class 8 20GP/ USD2725



Validity to the end of June ’16.



Inclusive all other surcharges except any relating to weight

If the rate is acceptable, I can have an agreement sent over to you.



In order to comply with FMC Regulations, please advise us at least 48 hours prior to the intended cargo acceptance date of your intention to book.



regards



Claire Ling

Inside Sales Coordinator

OOCL UK Branch

Tel. +44 1473 654222



Going Green:  We take it personally

for Sustainability



From: Malcolm Chilton
Sent: 11 May 2016 14:59
To: 'craig.purves@oocl.com' <craig.purves@oocl.com <mailto:craig.purves@oocl.com> >
Cc: Brett Hanson <brett@zen-intl.co.uk <mailto:brett@zen-intl.co.uk> >
Subject: Business Opportunity



Hi Craig



We load reasonably regular 20ft business ex T/Park to door Mississauga Ont.



Approx 4/5x20 per month.



Non Haz & Haz boxes.



Target rate Non Haz = USD2525.

Target rate Haz = USD2725



The DG is class 8 and the same cargo you now handle re Chicago RH via Norfolk VA.



We have a 20ft non haz to load on Friday.



Can you please review and let me know if of any interest?



Regards



Malc



Mobile +44 (0)777 5000 298







Zenith House

Valley Court

Bradford

BD1 4SP



Telephone: 01274 727888

Fax: 01274 727999



""The Company operates under BIFA Standard Trading Conditions latest edition, a copy of which is available upon request.""
"

            ''',
        ]
        output_strs = [

            '\n'.join([
                "Please can we book 1 x 20’GP container, released merchant haulage for shipment to CFR Montreal – including Dest THC.",
                "Please confirm container release depot address?",
                "Quotation Folder: 00000661 / Doc 16061",
                "We will collect empty from Thursday 23rd June",
                "Export laden container can be returned to quay by Friday 24th June",
                "Commodity: Non Haz – Steel Bars",
                "Gross weight: 24,000 kgs",
                "Our file ref: DE0163200",
                "UCR: 6GB238712260000-DE0163200",
                "Will await your confirmation. Many thanks",
            ]),
            '\n'.join([
                "Please can we make the following booking:",
                "Equipment:  2 x 40'GP containers",
                "Destination: CFR Busan, Korea - Quotation FE201203",
                "UCR: 6GB114536492000-DE0163923",
                "VGM: ZENITHINT*DE0163923*TL",
                "Commodity: Iron Bars",
                "Gross weight: approx 24,300 kgs",
                "Load Address:",
                "SHS Freight",
                "Riverside Development",
                "Chesterton Road",
                "Eastwood Trading Estate",
                "Rotherham",
                "S65 1SU",
                "Date / Time:",
                "Thursday 4th August",
                "@ 0800 hrs – Driver to quote: UCB 19388",
                "@ 1000 hrs – Driver to quote: UCB 19389",
                "Our file ref: DE0163923",
                "Will await your confirmation.",
            ]),
            '\n'.join([
                "Your: 4024150400",
                "Our: DE0163016",
                "Please can we amend loading time to 1000 hrs - Mon 27th June",
            ])
        ]

        for idx, input_str in enumerate(input_strs):
            self.assertEqual(ContentPattern().extract(input_str), output_strs[idx])


if __name__ == '__main__':
    unittest.main()
