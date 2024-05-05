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

    if len(arr) <= 1:
        return arr

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

    .. image:: images/bubble-sort.gif

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
        arr.reverse()

    return arr


def quicksort(arr, left=None, right=None, **kwargs):
    """
    Выполняет алгоритм быстрой сортировки на входном списке.

    .. image:: images/quicksort.gif

    :Сложность: O(N log N)
    :param arr: Список для сортировки.
    :param left: Начальный индекс подсписка для сортировки. По умолчанию 0.
    :param right: Конечный индекс подсписка для сортировки. По умолчанию len(arr) - 1.

    :param kwargs: Дополнительные параметры для поведения сортировки.

                   - inplace (bool): Если True, сортирует список на месте. По умолчанию False.
                   - reverse (bool): Если True, сортирует список в обратном порядке. По умолчанию False.

    :return: Отсортированный список.
    """
    if len(arr) <= 1:
        return arr

    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1

    inplace = kwargs.get("inplace", False)
    reverse = kwargs.get("reverse", False)

    if not inplace:
        arr = arr.copy()

    if left < right:
        sep_index = partition(arr, left, right, reverse)
        quicksort(arr, left, sep_index - 1, reverse=reverse, inplace=True)
        quicksort(arr, sep_index + 1, right, reverse=reverse, inplace=True)

    return arr


def partition(arr, left, right, reverse):
    """
    Эта функция реализует логику разделения для алгоритма быстрой сортировки.
    Она выбирает последний элемент в качестве опорного и переставляет массив так,
    чтобы все элементы меньше опорного были слева, а все элементы больше опорного - справа,
    либо наоборот, если reverse == True.

    :param arr: Список для сортировки.
    :param left: Начальный индекс подсписка для сортировки.
    :param right: Конечный индекс подсписка для сортировки.
    :param reverse: Если True, сортирует список в обратном порядке. Если False, сортирует в прямом порядке.

    :return: Индекс опорного элемента после разделения.
    """
    pivot = arr[right]
    i = left - 1

    for j in range(left, right):
        if not reverse and arr[j] < pivot or reverse and arr[j] > pivot:
            i += 1
            swap(arr, i, j)

    swap(arr, i + 1, right)
    return i + 1
