import re
import math
from collections import defaultdict
from typing import Tuple, Dict


FS_OPERATORS = [
    "++", "--", "::", "<=", ">=", "==", "<>", "<-", "->", "|>", "||", "&&", "+", "-", "*", "/", "%", "=", "<", ">", ":=",
    "not", "if", "then", "else", "for", "in", "while", "let", "return", "match", "with", "fun", "type", "module",
    "open", "do", "yield", "lazy", "use", "try", "finally", "when", "->", "<-"
]


class HalsteadFS:
    def __init__(self):
        self.operators = defaultdict(int)
        self.operands = defaultdict(int)

    def _build_operator_pattern(self):
        ops_sorted = sorted(set(FS_OPERATORS), key=lambda s: -len(s))
        parts = []
        for op in ops_sorted:
            if re.fullmatch(r"[A-Za-z_]\w*", op):
                parts.append(rf"\b{re.escape(op)}\b")
            else:
                parts.append(re.escape(op))
        pattern = "|".join(parts)
        return re.compile(pattern)

    def calculate(self, code: str) -> Tuple[Dict[str, float], Dict[str, int], Dict[str, int]]:
        self.operators = defaultdict(int)
        self.operands = defaultdict(int)

        if not code:
            return {}, {}, {}

        code_no_comments = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        code_no_comments = re.sub(r'\(\*.*?\*\)', '', code_no_comments, flags=re.DOTALL)

        op_regex = self._build_operator_pattern()
        op_matches = list(op_regex.finditer(code_no_comments))
        for m in op_matches:
            op_text = m.group(0)
            self.operators[op_text] += 1

        code_without_ops = list(code)
        for m in op_matches:
            start, end = m.start(), m.end()
            for i in range(start, end):
                code_without_ops[i] = " "
        code_no_ops = "".join(code_without_ops)

        string_pattern = re.compile(r'@?"(?:\\.|[^"\\])*"')
        for m in string_pattern.finditer(code_no_ops):
            s = m.group(0)
            self.operands[s] += 1
        code_no_strings = string_pattern.sub(" ", code_no_ops)

        number_pattern = re.compile(r'\b\d+(?:\.\d+)?\b')
        for m in number_pattern.finditer(code_no_strings):
            num = m.group(0)
            self.operands[num] += 1
        code_no_numbers = number_pattern.sub(" ", code_no_strings)

        identifier_pattern = re.compile(r'\b[a-zA-Z_]\w*\b')
        word_ops = {op for op in FS_OPERATORS if re.fullmatch(r"[A-Za-z_]\w*", op)}
        for m in identifier_pattern.finditer(code_no_numbers):
            ident = m.group(0)
            if ident not in word_ops:
                self.operands[ident] += 1

        unique_operators = len(self.operators)
        unique_operands = len(self.operands)
        total_operators = sum(self.operators.values())
        total_operands = sum(self.operands.values())

        vocabulary = unique_operators + unique_operands
        length = total_operators + total_operands
        volume = length * math.log2(vocabulary) if vocabulary > 0 else 0.0

        difficulty = 0.0
        if unique_operands > 0:
            difficulty = (unique_operators / 2.0) * (total_operands / unique_operands)
        effort = difficulty * volume
        time_seconds = effort / 18.0  # по Холстеду: E/18 секунд

        metrics = {
            "η1 (уникальные операторы)": unique_operators,
            "η2 (уникальные операнды)": unique_operands,
            "N1 (всего операторов)": total_operators,
            "N2 (всего операндов)": total_operands,
            "Словарь программы": vocabulary,
            "Длина программы": length,
            "Объем программы": round(volume, 3),
            "Сложность": round(difficulty, 3),
            "Трудоёмкость": round(effort, 3),
            "Время": round(time_seconds, 3)
        }

        return metrics, dict(self.operators), dict(self.operands)