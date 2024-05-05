from math import floor
from .my_functions import swap


class MinHeap:
    """
    Куча минимума - это бинарное дерево, где ключ каждого узла всегда меньше или равен ключам его детей.
    Эта структура данных позволяет эффективно вставлять, удалять и находить минимальный элемент в куче.

    .. image:: images/heap.png
    """

    def __init__(self, arr=None):
        """
        Инициализировать новую кучу минимума.

        :Сложность: O(N log N), где n - количество элементов в arr.
        :param arr: Необязательный итерируемый объект, содержащий начальные элементы кучи.
        """
        if arr is None:
            arr = []
        elif not isinstance(arr, list) and hasattr(arr, '__iter__'):
            arr = list(arr)

        self.heap = arr.copy()

        if len(arr) <= 1:
            return

        for i in range(len(self) // 2, -1, -1):
            self.heapify_down(i)

    def __len__(self):
        """
        Возвращает количество элементов в куче.

        :Сложность: O(1).
        :return: Количество элементов в куче.
        """
        return len(self.heap)

    def __iter__(self):
        """
        Перебирает элементы кучи в порядке их приоритета.

        :Сложность: O(1).
        :return: Итератор по элементам кучи.
        """
        return self.heap.__iter__()

    def get_item(self, index):
        """
        Возвращает элемент по указанному индексу.

        :Сложность: O(1).
        :param index: Индекс элемента для возврата.
        :return: Элемент по указанному индексу.
        """
        return self.heap[index]

    def __getitem__(self, item):
        return self.get_item(item)

    @staticmethod
    def get_left_child_index(index):
        """
        Возвращает индекс левого потомка указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Индекс левого потомка узла.
        """
        return 2 * index + 1

    @staticmethod
    def get_right_child_index(index):
        """
        Возвращает индекс правого потомка указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Индекс правого потомка узла.
        """
        return 2 * index + 2

    @staticmethod
    def get_parent_index(index):
        """
        Возвращает индекс родителя указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Индекс родителя узла.
        """
        return floor((index - 1) / 2)

    def count(self, item):
        """
        Возвращает количество вхождений указанного элемента в кучу.

        :Сложность: O(n), где n - количество элементов в куче.
        :param item: Элемент для подсчета.
        :return: Количество вхождений элемента в кучу.
        """
        return self.heap.count(item)

    def has_left_child(self, index) -> bool:
        """
        Проверяет, есть ли у указанного узла левый потомок.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: True, если узел имеет левого потомка, иначе False.
        """
        return self.get_left_child_index(index) < len(self)

    def has_right_child(self, index) -> bool:
        """
        Проверяет, есть ли у указанного узла правый потомок.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: True, если узел имеет правого потомка, иначе False.
        """
        return self.get_right_child_index(index) < len(self)

    def has_parent(self, index) -> bool:
        """
        Проверяет, есть ли у указанного узла родитель.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: True, если узел имеет родителя, иначе False.
        """
        return self.get_parent_index(index) >= 0

    def left_child(self, index):
        """
        Возвращает левого потомка указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Левый потомок узла.
        """
        return self.heap[self.get_left_child_index(index)]

    def right_child(self, index):
        """
        Возвращает правого потомка указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Правый потомок узла.
        """
        return self.heap[self.get_right_child_index(index)]

    def parent(self, index):
        """
        Возвращает родителя указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Родитель узла.
        """
        return self.heap[self.get_parent_index(index)]

    def peek(self):
        """
        Возвращает минимальный элемент в куче без его удаления.

        :Сложность: O(1).
        :return: Минимальный элемент в куче.
        """
        if len(self) == 0:
            raise IndexError
        return self.heap[0]

    def poll(self, index=None):
        """
        Удаляет и возвращает минимальный элемент из кучи.

        :Сложность: O(log n), где n - количество элементов в куче.
        :param index: Индекс элемента для удаления. Если не указан, удаляется минимальный элемент.
        :return: Минимальный элемент в куче.
        """
        if len(self) == 0:
            raise IndexError

        if index is None:
            index = 0

        item = self.heap[index]
        self.heap[index] = self.heap[len(self) - 1]
        self.heap.pop()
        self.heapify_down(index)
        return item

    def add(self, item):
        """
        Добавляет элемент в кучу.

        :Сложность: O(log n), где n - количество элементов в куче.
        :param item: Элемент для добавления.
        """
        self.heap.append(item)
        self.heapify_up()

    def heapify_down(self, index=None):
        """
        Перестраивает элементы в куче вниз от указанного узла.

        :Сложность: O(log n), где n - количество элементов в куче.
        :param index: Индекс узла для начала. Если не указан, используется корень кучи.
        """
        if len(self) <= 1:
            return

        if index is None:
            index = 0

        while self.has_left_child(index):
            min_child_index = self.get_left_child_index(index)

            if self.has_right_child(index) and self.right_child(index) < self.left_child(index):
                min_child_index = self.get_right_child_index(index)

            if self[min_child_index] > self[index]:
                break

            swap(self.heap, index, min_child_index)
            index = min_child_index

    def heapify_up(self, index=None):
        """
        Перестраивает элементы в куче вверх от указанного узла.

        :Сложность: O(log n), где n - количество элементов в куче.
        :param index: Индекс узла для начала. Если не указан, используется последний элемент кучи.
        """
        if len(self) <= 1:
            return

        if index is None:
            index = len(self) - 1

        while self.has_parent(index) and self.parent(index) > self.heap[index]:
            p_i = self.get_parent_index(index)
            swap(self.heap, index, p_i)
            index = p_i


class PriorityQueueNode:
    """
    Узел приоритетной очереди.
    """
    def __init__(self, val, priority):
        self.val = val
        self.priority = priority

    def __lt__(self, other):
        if isinstance(other, PriorityQueueNode):
            return self.priority < other.priority
        elif isinstance(other, tuple):
            if len(other) == 2:
                return self.priority < other[1]
        else:
            raise TypeError

    def __eq__(self, other):
        if isinstance(other, PriorityQueueNode):
            return self.priority == other.priority
        elif isinstance(other, tuple):
            if len(other) == 2:
                return self.priority == other[1]
        else:
            raise TypeError

    def __le__(self, other):
        return self < other or self == other

    def __repr__(self):
        return f"({self.val}, {self.priority})"


class PriorityQueue(MinHeap):
    """
    Приоритетная очередь, реализованная на основе мин-кучи.
    """

    def enqueue(self, item, priority=0):
        """
        Добавляет элемент в приоритетную очередь с указанным приоритетом.

        :Сложность: O(log n)
        :param item: Элемент для добавления.
        :param priority: Приоритет элемента. (По умолчанию 0 -- самый высокий приоритет)
        """
        self.add(PriorityQueueNode(item, priority))

    def dequeue(self):
        """
        Извлекает и возвращает элемент с наивысшим приоритетом из приоритетной очереди.

        :Сложность: O(log n)
        :return: Самый приоритетный узел.
        """
        return self.poll()

