import re
import math
from collections import defaultdict

FS_OPERATORS = [
    r"\+", r"-", r"\*", r"/", r"%", r"\+\+", r"--", r"=", r"\<\-", r"\->", r"\|>", r"\|\|", r"\&\&",
    r"==", r"<>", r"<=", r">=", r"<", r">",
    r"not", r"&&", r"||", r"if", r"then", r"else", r"for", r"in", r"while", r"let", r"return"
]

class HalsteadFS:
    def __init__(self):
        self.operators = defaultdict(int)
        self.operands = defaultdict(int)

    def calculate(self, code: str):
        for op in FS_OPERATORS:
            matches = re.findall(rf"\b{op}\b|{op}", code)
            if matches:
                self.operators[op] += len(matches)

        tokens = re.findall(r"\b[a-zA-Z_]\w*\b|\b\d+(\.\d+)?\b", code)
        for token in tokens:
            if token not in [o.strip("\\") for o in FS_OPERATORS]:
                self.operands[token] += 1

        unique_operators = len(self.operators)
        unique_operands = len(self.operands)
        total_operators = sum(self.operators.values())
        total_operands = sum(self.operands.values())

        vocabulary = unique_operators + unique_operands
        length = total_operators + total_operands
        volume = length * math.log2(vocabulary) if vocabulary > 0 else 0

        metrics = {
            "η1 (уникальные операторы)": unique_operators,
            "η2 (уникальные операнды)": unique_operands,
            "N1 (всего операторов)": total_operators,
            "N2 (всего операндов)": total_operands,
            "Словарь программы": vocabulary,
            "Длина программы": length,
            "Объем программы": volume
        }

        return metrics, dict(self.operators), dict(self.operands)