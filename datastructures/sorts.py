from . import MinHeap
from .my_functions import swap


def heap_sort(arr: list, **kwargs):
    """
    Сортирует входной список с использованием алгоритма сортировки кучей.

    :Сложность: O(N log N)
    :param arr: Список, который требуется отсортировать.
    :param kwargs: Дополнительные параметры для настройки поведения сортировки.
                   Возможные параметры:

                   - reverse (bool): Если установлено в True, возвращает список в обратном порядке.
                   - inplace (bool): Если установлено в True, сортирует список на месте (in-place).

    :return: Отсортированный список.
    """
    inplace = kwargs.get("inplace", False)
    reverse = kwargs.get("reverse", False)

    if not inplace:
        arr = arr.copy()

    heap = MinHeap(arr)
    for i in range(len(arr)):
        arr[i] = heap.poll()

    if reverse:
        arr.reverse()

    return arr


def bubble_sort(arr: list, **kwargs):
    """
    Сортировка пузырьком.

    :Сложность: O(N^2)
    :param arr: Список, который требуется отсортировать.
    :param kwargs: Дополнительные параметры для настройки поведения сортировки.
                   Возможные параметры:

                   - reverse (bool): Если установлено в True, возвращает список в обратном порядке.
                   - inplace (bool): Если установлено в True, сортирует список на месте (in-place).

    :return: Отсортированный список.
    """
    inplace = kwargs.get("inplace", False)
    reverse = kwargs.get("reverse", False)

    if len(arr) <= 1:
        return arr

    if not inplace:
        arr = arr.copy()

    for i in range(len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                swap(arr, i, j)

    if reverse:
        return arr[::-1]

    return arr
