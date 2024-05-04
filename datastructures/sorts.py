from . import MinHeap
from .my_functions import swap


def heap_sort(arr: list, **kwargs):
    """
    Сортирует входной список с использованием алгоритма сортировки кучей (heap sort).

    :Сложность: O(N log N)
    :param arr: Список, который требуется отсортировать.
    :param kwargs: Дополнительные параметры для настройки поведения сортировки.
                   Возможные параметры:

                   - reverse (bool): Если установлено в True, возвращает список в обратном порядке.

    :return: Отсортированный список.
    """
    heap = MinHeap(arr)
    sorted_arr = []
    while len(heap) > 0:
        sorted_arr.append(heap.poll())

    if "reverse" in kwargs:
        if kwargs["reverse"]:
            return sorted_arr[::-1]

    return sorted_arr


def bubble_sort(arr:list):
    if len(arr) <= 1:
        return arr
    for i in range(len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                swap(arr, i, j)
    return arr



