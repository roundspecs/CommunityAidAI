from langchain.schema import BaseOutputParser
import re

class NumberedListOutputParser(BaseOutputParser):
    def parse(self, text: str) -> list:
        pattern = r"\d+\.\s*(.*)"
        matches = re.findall(pattern, text)
        solutions = [match.strip() for match in matches]
        return solutions