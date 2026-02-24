import math
import re
from collections import defaultdict
from typing import Tuple, Dict, List

FS_OPERATORS = [
    "++", "--", "::", "<=", ">=", "==", "<>", "<-", "->", "|>", "||", "&&",
    "+", "-", "*", "/", "%", "=", "<", ">", ":=",
    "not", "if", "then", "else", "for", "in", "while", "let", "return",
    "match", "with", "fun", "type", "module", "open", "do", "yield", "lazy",
    "use", "try", "finally", "when"
]

FS_COMPOSITE_PATTERNS = [
    ("if..then..else", re.compile(r'\bif\b.*?\bthen\b.*?\belse\b', flags=re.DOTALL)),
    ("if..then", re.compile(r'\bif\b.*?\bthen\b', flags=re.DOTALL)),
    ("match..with", re.compile(r'\bmatch\b.*?\bwith\b', flags=re.DOTALL)),
    ("fo..in..do", re.compile(r'\bfor\b.*?\bin\b.*?\bdo\b', flags=re.DOTALL)),
    ("while..do", re.compile(r'\bwhile\b.*?\bdo\b', flags=re.DOTALL)),
    ("try..with..finally", re.compile(r'\btry\b.*?\bwith\b.*?\bfinally\b', flags=re.DOTALL)),
    ("try..with", re.compile(r'\btry\b.*?\bwith\b', flags=re.DOTALL)),
    ("try..finally", re.compile(r'\btry\b.*?\bfinally\b', flags=re.DOTALL)),
    ("let..in", re.compile(r'\blet\b.*?\bin\b', flags=re.DOTALL)),
]


class HalsteadFS:
    def __init__(self):
        self.operators = defaultdict(int)
        self.operands = defaultdict(int)
        self.op_regex = self.__build_operator_pattern()

    def __build_operator_pattern(self) -> re.Pattern:
        ops_sorted = sorted(set(FS_OPERATORS), key=len, reverse=True)
        parts = []
        for op in ops_sorted:
            if re.fullmatch(r"[A-Za-z_]\w*", op):
                parts.append(rf"\b{re.escape(op)}\b")
            else:
                parts.append(re.escape(op))
        pattern = "|".join(parts)
        return re.compile(pattern)

    def __blank_replace(self, match: re.Match) -> str:
        return " " * (match.end() - match.start())

    def __extract_composite_operators(self, code: str) -> str:
        for name, regex in FS_COMPOSITE_PATTERNS:
            while True:
                m = regex.search(code)
                if not m:
                    break
                self.operators[name] += 1
                code = code[:m.start()] + self.__blank_replace(m) + code[m.end():]
        return code

    def __extract_composite_operators(self, code: str) -> str:
        for name, regex in FS_COMPOSITE_PATTERNS:
            while True:
                m = regex.search(code)
                if not m:
                    break
                self.operators[name] += 1

                segment = code[m.start():m.end()]

                keywords = [kw for kw in name.split("..")]
                for kw in keywords:
                    segment = re.sub(
                        rf'\b{kw}\b',
                        lambda x: " " * len(x.group(0)),
                        segment,
                        count=1
                    )

                code = code[:m.start()] + segment + code[m.end():]
        return code

    def calculate(
            self,
            code: str,
            string_as_operand: bool = False
    ) -> Tuple[Dict[str, float], List[Tuple[str, int]], List[Tuple[str, int]]]:

        self.operators = defaultdict(int)
        self.operands = defaultdict(int)

        if not code:
            return {}, [], []

        code_no_comments = re.sub(r'//.*$', self.__blank_replace, code, flags=re.MULTILINE)
        code_no_comments = re.sub(r'\(\*.*?\*\)', self.__blank_replace, code_no_comments, flags=re.DOTALL)

        string_pattern = re.compile(r'@?"(?:\\.|[^"\\])*"', flags=re.DOTALL)
        if string_as_operand:
            for match in string_pattern.finditer(code_no_comments):
                s = match.group(0)
                self.operands[s] += 1
        code_no_strings = string_pattern.sub(self.__blank_replace, code_no_comments)

        code_after_composites = self.__extract_composite_operators(code_no_strings)

        for match in self.op_regex.finditer(code_after_composites):
            op_text = match.group(0)
            self.operators[op_text] += 1

        code_no_ops = self.op_regex.sub(self.__blank_replace, code_after_composites)

        number_pattern = re.compile(r'\b\d+(?:\.\d+)?\b')
        for match in number_pattern.finditer(code_no_ops):
            num = match.group(0)
            self.operands[num] += 1
        code_no_numbers = number_pattern.sub(self.__blank_replace, code_no_ops)

        identifier_pattern = re.compile(r"\b[a-zA-Z_][\w']*\b")
        for match in identifier_pattern.finditer(code_no_numbers):
            ident = match.group(0)
            if ident != "_":
                self.operands[ident] += 1

        unique_operators = len(self.operators)
        unique_operands = len(self.operands)
        total_operators = sum(self.operators.values())
        total_operands = sum(self.operands.values())

        vocabulary = unique_operators + unique_operands
        length = total_operators + total_operands
        volume = length * math.log2(vocabulary) if vocabulary > 0 else 0.0

        difficulty = (unique_operators / 2.0) * (total_operands / unique_operands) if unique_operands > 0 else 0.0
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

        sorted_operators = sorted(self.operators.items(), key=lambda x: x[1], reverse=True)
        sorted_operands = sorted(self.operands.items(), key=lambda x: x[1], reverse=True)

        return metrics, sorted_operators, sorted_operands
