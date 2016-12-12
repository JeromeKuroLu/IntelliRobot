import re
import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from util import matcher_factory

date_patterns = [
    r"((date)(\s*)(:)?(\s*))?(\d+)(\s*)(\.|/|\*|:)(\s*)(\d+)(\s*)(\.|/|\*|:)(\s*)(\d+)",
    r"((date)(\s*)(:)?(\s*))?(\d+)(\s*)(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)(\s*)(,|\.|/|\*|:)?(\s*)(\d+)",
    r"((date)(\s*)(:)?(\s*))?(\d+)(\s*)(of)(\s*)(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)(\s*)(,|\.|/|\*|:)?(\s*)(\d+)",
    r"((date)(\s*)(:)?(\s*))?(\d+)(\s*)(of)(\s*)(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)",
    r"((date)(\s*)(:)?(\s*))?(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)(\s*)(\.|/|\*|:)?(\s*)(\d+)(\s*)(th|st|nd)?(\s*)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\]|[`\-=\[\];',./~!@#$%^&*()_+{}:<>?\\])?(\s*)(\d+)",
    r"((date)(\s*)(:)?(\s*))?(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)(\s*)(\.|/|\*|:)?(\s*)(\d+)(\s*)(th|st|nd)?",
    r"((date)(\s*)(:)?(\s*))?(\d+)(\s*)(/)(\s*)(\d+)",
    r"((date)(\s*)(:)?(\s*))?(date)(\s*)(\.|/|\*|:)?(\s*)(\d+)",
    r"((date)(\s*)(:)?(\s*))?(pol|pod)(\s*)(\.|/|\*|:)(\s*)(\d+)",
    r"((date)(\s*)(:)?(\s*))?(\d+)(\s*)(th|st|nd)?(\s*)([`=\[\];',/~!@#$%^&*()_+{}:<>?\\]|[`\-=\[\];',./~!@#$%^&*()_+{}:<>?\\])?(\s*)(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)(\s*)(\.|/|\*|:)?(\s*)(\d+)?",
]


class DatePattern:
    date_pattern = matcher_factory.merge_regular_expressions(date_patterns)
    clean_result_pattern = re.compile(r"pol|pod|(date)(\s*)(:)?(\s*)", re.IGNORECASE)

    def extract(self, content):
        results = list()
        all_iterator = self.date_pattern.finditer(content)
        for iterator in all_iterator:
            phrase = iterator.group(0)
            # clean step
            phrase = re.sub(self.clean_result_pattern, "", phrase)
            results.append(phrase.strip())
        return results

    def replace(self, content):
        return self.date_pattern.sub(" _Date_ ", content)


if __name__ == '__main__':
    date = DatePattern()
    date1 = DatePattern()
    print(id(date.date_pattern) == id(date1.date_pattern))
    print(id(date.date_pattern))
    print(id(date1.date_pattern))
    test = '''
    "

Hi

Please book as per quote  00001719 – 16049



To load   16.8.16  9am

Load address



To Nashville TN

Load address

Denykem

UNIT 1

WAKEFIELD RD

OSSETT

WF5 9JA

Non haz Enzymes



Method 2 SL our badge  FUTUREFWDG



Please file AMS against master bill



Kind Regards
Rach





Rachael Silvester
Export Administrator
DDI: 01924 421382
Tel: +44 (0) 844 879 4977
Mobile: +44 (0)7713 436118 out of hours only
Skype: ffclrachaels
Future Forwarding Co Ltd.
Hawthorne House
Dark Lane
Birstall
Leeds
West
Yorkshire
WF17 9LW



All business is transacted under the Standard Trading Conditions of the British International Freight Association (latest edition) copies of which are available upon request. IMPORTANT - This e-mail and the information that it contains may be confidential, legally privileged and protected by law. Access by the intended recipient only is authorised. Any liability (in negligence or otherwise) arising from any third party acting, or refraining from acting, on any information contained in this e-mail is hereby excluded. If you are not the intended recipient, please notify the sender immediately and do not disclose the contents to any other person, use it for any purpose, or store or copy the information in any medium. Copyright in this e-mail and attachments created by us belongs to Future Forwarding Co. Ltd. The author also asserts the right to be identified as such and object to any misuse.

“Carrier has opted to be exempt from tariff publication requirements per 46 C.F.R. §520 and 532 by utilizing Negotiated Rate Arrangements (“NRAs”). Acceptance of quotations shall become binding after receipt of the cargo by the carrier or its agent (or the originating carrier in the case of through transportation). Carrier’s Rules Tariff are provided free of charge at futureforwarding.com . Carrier reserves the right to modify its NRA rate/charges offer prior to Carrier or its agent receiving the cargo for transport. All origin and destination local charges apply whether or not included in FFC’s Rules Tariff or in quotations”.

Registered in England and Wales No. 1376547 with Registered Office at Hawthorne House, Dark Lane, Birstall, West Yorkshire, WF17 9LW
"

        '''
    print(date.extract(test))
    print(date.extract('27-AUG'))

