import re


content_patterns = [
    re.compile(r"Thanks(\s+)Rach(\s+)Rachael(\s+)Silvester(\s+)Export(\s+)Administrator(\s+)DDI", re.IGNORECASE),
    re.compile(r"Many Thanks[^\w]", re.IGNORECASE),
    re.compile(r"Thanks(\s+)and(\s+)B\.rgds", re.IGNORECASE),
    re.compile(r"(\n)(\s*)regard(s?)[^\w]", re.IGNORECASE),
    re.compile(r"(\n)(\s*)Rgd(s?)[^\w]", re.IGNORECASE),
    re.compile(r"(Thanks(\s+)and(\s*)|Thanks(\s+)&(\s*))?(best|kind)?[^\w]+regard(s?)[^\w]", re.IGNORECASE),
    re.compile(r"(Thanks(\s+)and(\s*)|Thanks(\s+)&(\s*))?(best|kind)?[^\w]+Rgd(s?)[^\w]", re.IGNORECASE),
    re.compile(r"From:(.*?)Sent:(.*?)To:", re.DOTALL | re.IGNORECASE),
    re.compile(r"From:(.*?)Date:(.*?)To:", re.DOTALL | re.IGNORECASE),
    re.compile(r"Please note my working hours", re.IGNORECASE),
    re.compile(r"-----")
]


def split_content(contents):
    for content_pattern in content_patterns:
        contents = content_pattern.split(contents)[0]
    return contents
