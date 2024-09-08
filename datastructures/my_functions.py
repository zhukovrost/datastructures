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

def merge(arr1, arr2):
    arr = []
    i = j = 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            arr.append(arr1[i])
            i += 1
        else:
            arr.append(arr2[j])
            j += 1

    arr.extend(arr1[i:])
    arr.extend(arr2[j:])

    return arr
