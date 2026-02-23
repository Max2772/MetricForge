import re
import math
from collections import defaultdict
from typing import Tuple, Dict


FS_OPERATORS = [
    "++", "--", "::", "<=", ">=", "==", "<>", "<-", "->", "|>", "||", "&&",
    "+", "-", "*", "/", "%", "=", "<", ">", ":=",
    "not", "if", "then", "else", "for", "in", "while", "let", "return",
    "match", "with", "fun", "type", "module", "open", "do", "yield", "lazy",
    "use", "try", "finally", "when"
]


class HalsteadFS:
    def __init__(self):
        self.operators = defaultdict(int)
        self.operands = defaultdict(int)
        self.op_regex = self._build_operator_pattern()


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


    def _blank_replace(self, match: re.Match) -> str:
        return " " * (match.end() - match.start())


    def calculate(self, code: str, string_as_operand: bool = False) -> Tuple[Dict[str, float], Dict[str, int], Dict[str, int]]:
        self.operators = defaultdict(int)
        self.operands = defaultdict(int)

        if not code:
            return {}, {}, {}

        code_no_comments = re.sub(r'//.*$', self._blank_replace, code, flags=re.MULTILINE)
        code_no_comments = re.sub(r'\(\*.*?\*\)', self. _blank_replace, code_no_comments, flags=re.DOTALL)

        string_pattern = re.compile(r'@?"(?:\\.|[^"\\])*"', flags=re.DOTALL)
        if string_as_operand:
            for match in string_pattern.finditer(code_no_comments):
                s = match.group(0)
                self.operands[s] += 1
        code_no_strings = string_pattern.sub(self._blank_replace, code_no_comments)

        for match in self.op_regex.finditer(code_no_strings):
            op_text = match.group(0)
            self.operators[op_text] += 1

        code_no_ops = self.op_regex.sub(self._blank_replace, code_no_strings)

        number_pattern = re.compile(r'\b\d+(?:\.\d+)?\b')
        for match in number_pattern.finditer(code_no_ops):
            num = match.group(0)
            self.operands[num] += 1
        code_no_numbers = number_pattern.sub(self._blank_replace, code_no_ops)

        identifier_pattern = re.compile(r"\b[a-zA-Z_][\w']*\b")
        word_ops = {op for op in FS_OPERATORS if re.fullmatch(r"[A-Za-z_]\w*", op)}
        for match in identifier_pattern.finditer(code_no_numbers):
            ident = match.group(0)
            if ident not in word_ops and ident != "_":
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
        time_seconds = effort / 18.0

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