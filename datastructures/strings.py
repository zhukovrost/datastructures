"""
Этот модуль содержит алгоритмы, связанные с работой со строками.
"""

def brute_force_search(text: str, substring: str) -> int:
    """
    Грубый поиск подстроки.

    .. image:: images/brute-force-string-search.gif
        :width: 400px

    :Сложность: O(N * M), где N - длина строки, а M - длина подстроки
    :param text: Исходный текст.
    :param substring: искомая подстрока. 
    
    :return: Индекс начала подстроки в строке (если не найдено, то -1).
    """

    n = len(text)
    m = len(substring)

    if m == 0:
        return -1

    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == substring[j]:
            j += 1
        if j == m:
            return i
    return -1


def _calculate_hash(s, length, base, prime):
    """
    Функция, создающая хэш подстроки. Она создает хэш плавающего окна.
    """
    h = 0
    for i in range(length):
        h = (base * h + ord(s[i])) % prime
    return h

def _update_hash(current_hash, old_char, new_char, h, base, prime):
    """
    Функция, обновляющая хэш подстроки. Она сдвигает плавающее окно вправо.
    """
    current_hash = (base * (current_hash - ord(old_char) * h) + ord(new_char)) % prime
    if current_hash < 0:
        current_hash += prime
    return current_hash

def rabin_karp(text: str, substring: str, base=256, prime=89) -> int:
    """
    Алгоритм Рабина-Карпа создан для поиска подстроки в строке за линейное время.
    Вместо того, чтобы сравнивать строки, мы сравниваем из хэши, что позволяет
    проверять совпадают ли строки за O(1).

    .. image:: images/rabin-karp.gif
        :width: 400px

    :Сложность: O(N + M), где N - длина строки, а M - длина подстроки
    :param text: Исходный текст.
    :param substring: искомая подстрока.
    :param base: количество символов в алфавите строки. По умолчанию 256 (ASCII).
    :param prime: простое число для генерации хэша. По умолчанию 89.

    :return: Индекс начала подстроки в строке (если не найдено, то -1).
    """

    n = len(text)
    m = len(substring)

    if n < m or m == 0:
        return -1

    h = 1 # значение хэша для сдвига вправо
    for i in range(m - 1):
        h = (h * base) % prime

    substring_hash = _calculate_hash(substring, m, base, prime)
    current_hash = _calculate_hash(text, m, base, prime)

    for i in range(n - m + 1):
        if substring_hash == current_hash:
            if text[i:i + m] == substring:
                return i

        if i < n - m:
            current_hash = _update_hash(current_hash, text[i], text[i + m], h, base, prime) # O(1)

    return -1
