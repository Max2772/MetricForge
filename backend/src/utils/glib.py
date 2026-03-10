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

        self._NESTING_OPEN = re.compile(r'^\s*(?:if|elif|for|while|match|try)\b', re.IGNORECASE)
        self._CONDITIONAL_WORD = re.compile(r'\b(?:if|elif|for|while|match|when)\b', re.IGNORECASE)
        self._MATCH_BRANCH = re.compile(r'^\s*\|')

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

    def _strip_comments(self, code: str) -> list[str]:
        without_block = re.sub(self._BLOCK_COMMENT_RE, '', code)
        lines = []
        for line in without_block.splitlines():
            line = re.sub(self._LINE_COMMENT_RE, '', line)
            lines.append(line)
        return lines

    def _strip_strings(self, line: str) -> str:
        return re.sub(self._STRING_RE, '""', line)

    @staticmethod
    def _get_indent(line: str) -> int:
        expanded = line.expandtabs(4)
        return len(expanded) - len(expanded.lstrip(' '))

    def calculate(self, code: str) -> Tuple[Dict[str, float], List[Tuple[str, int]]]:
        lines = self._strip_comments(code)

        operators = defaultdict(int)
        total_operators = 0
        conditional_operators = 0
        max_nesting = 0
        nesting_stack: List[int] = []

        conditional_words = {"if", "elif", "for", "while", "match", "when"}

        for raw_line in lines:
            line = raw_line.rstrip('\n')
            if not line.strip():
                continue

            indent = self._get_indent(line)

            # Убрать уровни вложенности, если уменьшился отступ
            while nesting_stack and indent <= nesting_stack[-1]:
                nesting_stack.pop()

            # Проверяем, открывает ли текущая строка новый блок вложенности
            if self._NESTING_OPEN.match(line):
                nesting_stack.append(indent)

            current_nesting = len(nesting_stack)

            # Удаляем строки (литералы) перед поиском операторов
            line_nostr = self._strip_strings(line)

            # Вызовы вида func(...)
            for call in self._FUNC_CALL_PAREN.findall(line_nostr):
                if call.lower() not in self._FS_OPERATORS:
                    operators["Вызов функции"] += 1

            # Вызовы вида func arg
            for call in self._FUNC_CALL_SPACE.findall(line_nostr):
                if call.lower() not in self._FS_OPERATORS:
                    operators["Вызов функции"] += 1

            # 1) Если это ветка match (строка начинается с '|'), считаем '|' как оператор-ветку
            if self._MATCH_BRANCH.match(line):
                operators['|'] += 1
                conditional_operators += 1
                total_operators += 1
                max_nesting = max(max_nesting, current_nesting)

            # 2) Находим все операторы по всей строке (ключевые слова и символьные)
            for m in self.op_regex.finditer(line_nostr):
                op_text = m.group(0)
                key = op_text.lower() if re.fullmatch(r"[A-Za-z_]\w*", op_text) else op_text
                operators[key] += 1
                total_operators += 1

                if isinstance(key, str) and key in conditional_words:
                    conditional_operators += 1
                    max_nesting = max(max_nesting, current_nesting)

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