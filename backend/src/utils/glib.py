import re
from collections import defaultdict
from typing import Tuple, Dict, List


class GilbFS:
    def __init__(self):
        self._FS_OPERATORS = [
            "++", "--", "::", "<=", ">=", "==", "<>", "<-", "->", "|>", "<|", "||", "&&",
            "+", "-", "*", "/", "%", "=", "<", ">", ":=",
            "not", "if", "then", "else", "elif", "for", "in", "while", "let", "return",
            "match", "with", "fun", "type", "module", "open", "do", "yield", "lazy",
            "use", "try", "finally", "when", "in"
        ]
        self.op_regex = self.__build_operator_pattern()

        self._OPERATOR_CATEGORIES = {
            "let": "Определение функции (let)",
            "<-": "Присваивание (<-)",
            "while": "Цикл while",
            "for": "Цикл for",
            "match": "Выбор (match)"
        }

        self._FUNC_CALL_PAREN = re.compile(r'\b([a-zA-Z_]\w*)\s*\(')
        self._FUNC_CALL_SPACE = re.compile(r'\b([a-zA-Z_]\w+)\s+[A-Za-z0-9_\[\]\(\)"]')

        self._NESTING_OPEN = re.compile(r'^\s*(?:if|elif|for|while|try)\b', re.IGNORECASE)
        self._MATCH_BRANCH = re.compile(r'^\s*\|')
        self._DEFAULT_BRANCH = re.compile(r'^\s*\|\s*_\s*->')
        self._MATCH_RE = re.compile(r'^\s*match\b\s*')

        self._BLOCK_COMMENT_RE = re.compile(r'\(\*.*?\*\)', re.DOTALL)
        self._LINE_COMMENT_RE = re.compile(r'//.*$')

        self._STRING_RE = re.compile(r'@"[^"]*"|\"(?:\\.|[^"\\])*\"|\'(?:\\.|[^\'\\])*\'')

    def __build_operator_pattern(self) -> re.Pattern:
        ops_sorted = sorted(set(self._FS_OPERATORS), key=len, reverse=True)
        parts = []
        for op in ops_sorted:
            if re.fullmatch(r"[A-Za-z_]\w*", op):
                parts.append(rf"\b{re.escape(op)}\b")
            else:
                parts.append(re.escape(op))
        pattern = "|".join(parts)
        return re.compile(pattern)

    def _strip_comments(self, code: str) -> List[str]:
        without_block = re.sub(self._BLOCK_COMMENT_RE, '', code)
        lines = []
        for line in without_block.splitlines():
            line = re.sub(self._LINE_COMMENT_RE, '', line)
            lines.append(line)
        return lines

    @staticmethod
    def _get_indent(line: str) -> int:
        expanded = line.expandtabs(4)
        return len(expanded) - len(expanded.lstrip(' '))

    def calculate(self, code: str) -> Tuple[Dict[str, float], List[Tuple[str, int]]]:
        code_nostr = re.sub(self._STRING_RE, '""', code)
        lines = self._strip_comments(code_nostr)

        in_match = False
        match_indent = None
        match_branch_count = 0
        operators = defaultdict(int)
        total_operators = 0
        conditional_operators = 0
        max_nesting = 0
        nesting_stack: List[int] = []

        conditional_words = {"if", "elif", "for", "while"}

        for raw_line in lines:
            line = raw_line.rstrip('\n')
            if not line.strip():
                continue

            indent = self._get_indent(line)

            if (
                    in_match and
                    (indent <= (match_indent if match_indent is not None else -1))
                    and not (
                    self._MATCH_BRANCH.match(line) or self._MATCH_RE.match(line))
            ):
                in_match = False
                match_indent = None
                match_branch_count = 0

            # Убрать уровни вложенности, если уменьшился отступ (обычные блоки)
            while nesting_stack and indent <= nesting_stack[-1]:
                nesting_stack.pop()

            if self._NESTING_OPEN.match(line):
                nesting_stack.append(indent)
                base = match_branch_count if in_match else 0
                max_nesting = max(max_nesting, base + len(nesting_stack))

            # Если встречаем сам 'match' — включаем is_match
            if self._MATCH_RE.match(line):
                in_match = True
                match_indent = indent
                match_branch_count = 0

            # Вызовы вида func(...)
            for call in self._FUNC_CALL_PAREN.findall(line):
                if call.lower() not in self._FS_OPERATORS:
                    operators["Вызов функции"] += 1

            # Вызовы вида func arg
            for call in self._FUNC_CALL_SPACE.findall(line):
                if call.lower() not in self._FS_OPERATORS:
                    operators["Вызов функции"] += 1

            # 1) если это ветка match (строка начинается с '|')
            if self._MATCH_BRANCH.match(line):
                operators['|'] += 1
                total_operators += 1

                if not self._DEFAULT_BRANCH.match(line):
                    match_branch_count += 1
                    conditional_operators += 1
                    max_nesting = max(max_nesting, len(nesting_stack) + match_branch_count)

            # 2) Находим все операторы по всей строке (ключевые слова и символьные)
            for m in self.op_regex.finditer(line):
                op_text = m.group(0)
                key = op_text.lower() if re.fullmatch(r"[A-Za-z_]\w*", op_text) else op_text
                operators[key] += 1
                total_operators += 1

                if key in conditional_words:
                    # если это обычный условный оператор внутри ветки match,
                    # его уровень = match_branch_count + текущая глубина стека
                    base = match_branch_count if in_match else 0
                    conditional_operators += 1
                    max_nesting = max(max_nesting, base + len(nesting_stack))

        relative = conditional_operators / total_operators if total_operators > 0 else 0.0

        metrics = {
            'Абсолютная сложность (CL)': conditional_operators,
            'Относительная сложность (cl)': round(relative, 3),
            'Макс. уровень вложенности (CLI)': max_nesting,
            'Всего операторов': total_operators,
        }

        grouped_operators = defaultdict(int)
        for op, count in operators.items():
            if op in self._OPERATOR_CATEGORIES:
                grouped_operators[self._OPERATOR_CATEGORIES[op]] += count
            else:
                grouped_operators[op] += count

        sorted_operators = sorted(grouped_operators.items(), key=lambda x: x[1], reverse=True)

        return metrics, sorted_operators