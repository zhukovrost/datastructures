def bubble_sort(arr):
    """
    Сортировка пузырьком.

    .. image:: images/bubble-sort.gif
        :width: 400px

    :Сложность: O(n\ :sup:`2`)
    :param arr: список, который нужно отсортировать
    """
    n = len(arr)
    for i in range(0, n):
        swap_flag = False
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swap_flag = True

        if not swap_flag:
            break
