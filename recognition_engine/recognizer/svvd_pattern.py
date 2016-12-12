import re

svvd_patterns = [
    r"([\w]{3}(\d)?-[\w]{3}-[\d]{3}(\s)*(E|S|W|N))"
]

clean_result_pattern = r"(\s)*"

class SvvdPattern:
    @staticmethod
    def extract(content):
        results = []
        for pattern in svvd_patterns:
            match = re.findall(pattern, content, flags=re.IGNORECASE)
            if match and type(match) is list:
                for result in match:
                    clean_result = re.sub(clean_result_pattern, "", result[0], flags=re.IGNORECASE).strip()
                    clean_result = clean_result[:-1] + " " + clean_result[-1:]
                    results.append(clean_result)

        return results

    @staticmethod
    def replace(content):
        for pattern in svvd_patterns:
            content = re.sub(pattern, " _svvd_number_ ", content, flags=re.IGNORECASE)
        return content
