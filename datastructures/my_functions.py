"""
Дополнительный модуль, который содержит некоторые функции.
"""


def swap(arr, i, j):
    """
    Меняет местами два элемента в массиве.
    """
    arr[i], arr[j] = arr[j], arr[i]


def is_sorted(arr):
    """
    Проверяет, является ли массив отсортированным по возрастанию.
    """
    if len(arr) <= 1:
        return True

    # Проверяем список на возрастание
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            return False

    return True
