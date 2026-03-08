import re
from collections import defaultdict
from typing import Tuple, Dict, List


class GilbFS:
    # Токены, увеличивающие вложенность
    _NESTING_OPEN = re.compile(
        r'^\s*(?:'
        r'if\b'
        r'|elif\b'
        r'|for\b.+\bdo\b'
        r'|while\b.+\bdo\b'
        r'|match\b'
        r')',
        re.IGNORECASE
    )

    # Токены, считающиеся условными операторами (CL)
    _CONDITIONAL = re.compile(
        r'^\s*(?:'
        r'if\b'
        r'|elif\b'
        r'|for\b.+\bdo\b'
        r'|while\b.+\bdo\b'
        r')',
        re.IGNORECASE
    )

    # match-ветки
    _MATCH_BRANCH = re.compile(r'^\s*\|(?!\s*(?:'
                               r'_'
                               r'|None'
                               r'|False'
                               r'|True\s*->)'
                               r'\s*->).+->'
                               )

    # Управляющие конструкции
    _OPERATOR = re.compile(
        r'^\s*(?:'
        r'let\b'
        r'|if\b|elif\b|else\b'
        r'|for\b|while\b'
        r'|match\b'
        r'|return\b|yield\b|yield!\b'
        r'|do\b'
        r'|raise\b|failwith\b|invalidArg\b'
        r'|try\b|with\b|finally\b'
        r'|use\b'
        r'|ignore\b'
        r'|<-'
        r')',
        re.IGNORECASE
    )


    @staticmethod
    def _strip_comments(code: str) -> list[str]:
        code = re.sub(r'\(\*.*?\*\)', '', code, flags=re.DOTALL)
        lines = []
        for line in code.splitlines():
            line = re.sub(r'//.*$', '', line)
            lines.append(line)
        return lines


    @staticmethod
    def _get_indent(line: str) -> int:
        expanded = line.expandtabs(4)
        return len(expanded) - len(expanded.lstrip(' '))


    def calculate(self, code: str) -> Tuple[Dict[str, float], List[Tuple[str, int]]]:
        lines = self._strip_comments(code)

        total_operators = 0
        conditional_operators = 0
        max_nesting = 0
        operators_counter = defaultdict(int)
        nesting_stack: List[int] = []

        for raw_line in lines:
            line = raw_line.rstrip()
            if not line.strip():
                continue

            indent = self._get_indent(line)

            # Убрать уровни вложенности, если уменьшился отступ
            while nesting_stack and indent <= nesting_stack[-1]:
                nesting_stack.pop()

            # Проверяем, открывает ли текущая строка новый блок вложенности
            opens_nesting = bool(self._NESTING_OPEN.match(line))
            if opens_nesting:
                nesting_stack.append(indent)

            current_nesting = len(nesting_stack)

            is_operator = bool(self._OPERATOR.match(line))
            is_match_branch = bool(self._MATCH_BRANCH.match(line))

            if is_operator or is_match_branch:
                total_operators += 1
                op_name = line.strip().split()[0] if line.strip() else "unknown"
                if is_match_branch:
                    op_name = "|"
                operators_counter[op_name] += 1

            # Условный оператор либо ветка match
            is_conditional = bool(self._CONDITIONAL.match(line))
            is_conditional_branch = is_match_branch

            if is_conditional or is_conditional_branch:
                conditional_operators += 1
                max_nesting = max(max_nesting, current_nesting)

        relative = conditional_operators / total_operators if total_operators > 0 else 0.0

        metrics = {
            'Абсолютная сложность (CL)': conditional_operators,
            'Относительная сложность (cl)': round(relative, 3),
            'Макс. уровень вложенности (CLI)': max_nesting,
            'Всего операторов': total_operators,
        }

        sorted_operators = sorted(operators_counter.items(), key=lambda x: x[1], reverse=True)

        return metrics, sorted_operators
