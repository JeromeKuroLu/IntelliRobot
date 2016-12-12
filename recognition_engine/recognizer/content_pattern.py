import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import split_content


class ContentPattern:
    @staticmethod
    def extract(content, join_char='\n'):
        result = split_content.split_content(content)
        result = result.strip()
        result = [item for item in result.split('\n') if item != '']
        return join_char.join(result)


if __name__ == '__main__':
    test = '''
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



Kind Regards

Emma Wood

Direct Dial +44 (0)1274 767422

WWW.ZEN-INTL.CO.UK <http://www.zen-intl.co.uk/>



Zenith House, Valley Court, Bradford. BD1 4SP

Telephone: 01274 727888 / Fax: 01274 727999



""The Company operates under BIFA Standard Trading Conditions latest edition, a copy of which is available upon request.""

""Zenith International Freight Ltd. is a limited company registered in England No. 3801743""



Unless Otherwise stated all prices exclude any customs clearance, duties, taxes and final delivery costs in the country of destination. The above is calculated at today's costs and rates of exchange, which are subject to alteration at the time of shipment.


"

        '''
    print(ContentPattern.extract(test))
    result = ContentPattern.extract(test)
    test1 = '\n'.join([
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
    ])
    print(result == test1)

