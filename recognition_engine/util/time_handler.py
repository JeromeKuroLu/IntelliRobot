month = r"(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)"
week = r"(Mon(day)?|Tue(sday)?|Wed(nesday)?|Thu(rsday)?|Fri(day)?|Sat(turday)?|Sun(day)?)"
unit = "(st|nd|rd|th)"

time_patterns = [
    r"(\d\d\d\d(\s*)(hrs|noon))",
    r"(\d(\d?):(\d?)\d(\s*)(hrs|noon))",
    r"(\d(\d?)(\s*)(am|pm))",
    r"(\d+)(\s*):(\s*)(\d+)(\s*)((am|pm|hrs)?)",
    r"\d(\d?)(am|pm)",
    r"\d{4}(\s*)hrs",
    r"\d\d(\s*)\.(\s*)\d\d(\s*)(hrs)"
]

date_patterns = [
    r"(\d+(\s*)<unit>(\s+)<month>)",
    r"(\d\d*\.\d\d*\.\d\d*)",
    r"(<week>(\s*)\d+(\s*)<unit>(\s+)<month>)",
    r"(\d\d/\d(\d?))",
    r"(\d+)(\s+)<month>(\s+)\d\d\d\d",
    r"<month>(\s+)(\d+)",
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

specify_time = '(' + '|'.join(time_patterns) + ')'
date_time = '(' + '|'.join(
    [item.replace('<week>', week).replace('<unit>', unit).replace('<month>', month) for item in date_patterns]) + ')'


if __name__ == '__main__':
    import re
    print(date_time)
    pattern = re.compile(date_time, re.DOTALL | re.IGNORECASE)
    print(pattern.search('27-AUG'))
