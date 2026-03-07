import re
from typing import Dict, List

class GilbAnalyzer:
    """
    Анализатор метрик Джилба для кода на F#.
    Подсчитывает абсолютную сложность (CL), относительную сложность (cl)
    и максимальный уровень вложенности (CLI).
    """

    # Ключевые слова, которые считаются условными операторами
    COND_KEYWORDS = {'if', 'elif', 'for', 'while', 'match', 'try', 'with', 'finally'}

    @staticmethod
    def remove_comments(code: str) -> str:
        """
        Удаляет однострочные (//) и многострочные (* ... *) комментарии.
        Предполагается, что комментарии не вложены.
        """
        # Удаляем многострочные комментарии (* ... *)
        code = re.sub(r'\(\*.*?\*\)', '', code, flags=re.DOTALL)
        # Удаляем однострочные комментарии //
        lines = []
        for line in code.splitlines():
            # Ищем // вне строковых литералов (упрощённо)
            # В учебных целях считаем, что // всегда комментарий
            if '//' in line:
                line = line[:line.index('//')]
            lines.append(line)
        return '\n'.join(lines)

    @staticmethod
    def _count_in_line(line: str, in_match: bool, match_indent: int, current_indent: int) -> Dict:
        """
        Обрабатывает одну строку: ищет условные ключевые слова и символы '|'.
        Возвращает словарь с количеством найденных условных операторов и флагом состояния match.
        """
        cond_count = 0
        new_in_match = in_match
        new_match_indent = match_indent

        # Поиск ключевых слов условных операторов
        # Используем границы слов, чтобы не захватывать части идентификаторов
        for match in re.finditer(r'\b(' + '|'.join(GilbAnalyzer.COND_KEYWORDS) + r')\b', line):
            kw = match.group()
            cond_count += 1
            if kw == 'match':
                new_in_match = True
                new_match_indent = current_indent

        # Если мы внутри match, ищем символы '|' (ветки)
        if new_in_match and current_indent >= new_match_indent:
            # Находим все '|' в строке
            pipes = re.findall(r'\|', line)
            cond_count += len(pipes)

        # Если текущий отступ меньше, чем у match, выходим из режима match
        if new_in_match and current_indent < new_match_indent:
            new_in_match = False
            new_match_indent = 0

        return {
            'cond': cond_count,
            'in_match': new_in_match,
            'match_indent': new_match_indent
        }

    def calculate(self, code: str) -> Dict[str, float]:
        """
        Основной метод: принимает строку с кодом на F#, возвращает словарь с метриками.
        """
        # Удаляем комментарии
        clean_code = self.remove_comments(code)

        # Разбиваем на строки и удаляем пустые (для подсчёта общего числа операторов)
        lines = clean_code.splitlines()
        non_empty_lines = [ln for ln in lines if ln.strip()]
        total_operators = len(non_empty_lines)   # упрощение: каждая непустая строка = один оператор

        # Переменные для подсчёта
        conditional_operators = 0
        max_nesting = 0
        current_nesting = 0
        in_match = False
        match_indent = 0

        for line in lines:
            # Вычисляем отступ (количество пробелов в начале строки)
            stripped = line.lstrip(' ')
            indent = len(line) - len(stripped)

            # Текущий уровень вложенности (считаем, что 1 уровень = 4 пробела)
            current_nesting = indent // 4
            max_nesting = max(max_nesting, current_nesting)

            # Обрабатываем строку
            result = self._count_in_line(line, in_match, match_indent, indent)
            conditional_operators += result['cond']
            in_match = result['in_match']
            match_indent = result['match_indent']

        relative = conditional_operators / total_operators if total_operators > 0 else 0.0

        return {
            'Абсолютная сложность (CL)': conditional_operators,
            'Относительная сложность (cl)': round(relative, 4),
            'Макс. уровень вложенности (CLI)': max_nesting,
            'Всего операторов': total_operators
        }
