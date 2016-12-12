import re

bkg_patterns = [
    r"(booking|book|shipment|bkg|oolu|shipping (instructions)?){1}[\s]*(number|no|num|ref|reference|#|\||:|\.|;|/|\-},)?[\s]*[(oolu)*(\d){10}(\s#\|:\.;,/\-)*]*"
]
num_pattern = r"((\s)*(oolu)?(\d){10}(\s)*)"
clean_result_pattern = r"(oolu)"


class BkgPattern:
    @staticmethod
    def extract(content):
        results = []
        for pattern in bkg_patterns:
            match = re.search(pattern, content, flags=re.IGNORECASE)
            if match is not None:
                phrase = match.group(0)
                nums = re.findall(num_pattern, phrase, flags=re.IGNORECASE)
                if nums and type(nums) is list:
                    for num in nums:
                        clean_result = re.sub(clean_result_pattern, "", num[0], flags=re.IGNORECASE).strip()
                        results.append(clean_result)

        return results

    @staticmethod
    def replace(content):
        local_stack = list()
        for pattern in bkg_patterns:
            # content = re.sub(pattern, " _bkg_number_ ", content, flags=re.IGNORECASE)
            matches = re.finditer(pattern, content, flags=re.IGNORECASE)
            for match in matches:
                phrase = match.group(0)
                nums = re.findall(num_pattern, phrase, flags=re.IGNORECASE)
                if nums and type(nums) is list:
                    # content = content[:match.start()] + ' _bkg_number_ ' + content[match.end():]
                    local_stack.append((match.start(), match.end()))
            while len(local_stack) != 0:
                replace_item = local_stack.pop()
                content = content[:replace_item[0]] + ' _bkg_number_ ' + content[replace_item[1]:]
        return content
