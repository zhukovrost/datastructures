from datastructures.LinkedLists import SinglyLinkedList


class StaticArray:
    """
    Обычный нерасширяемый список

    .. image:: images/static-array.png
        :width: 300px
    """
    def __init__(self, n):
        """
        Инициализация статичного списка.

        :param n: Длина списка
        """
        self.data = [None] * n

    def __iter__(self):
        for item in self.data:
            yield item

    def get_at(self, i):
        """
        Получить элемент.

        :Сложность: O(1)
        :param i: Индекс элемента
        :return: Данные под i-ым индексом
        """
        if not (0 <= i < len(self.data)):
            raise IndexError
        return self.data[i]

    def set_at(self, i, item):
        """
        Установить значение элемента.

        :Сложность: O(1)
        :param i: Индекс элемента
        :param item: Значение элемента
        """
        if not (0 <= i < len(self.data)):
            raise IndexError
        self.data[i] = item

    def search(self, item):
        """
        Поиск данных.

        :Сложность: O(n)
        :param item: Искомые данные
        :return: Индекс искомых данных
        """
        i = 0
        for data in self.data:
            if data == item:
                return i
            i += 1
        return -1


class Stack:
    """
    **Last in - First out** список (LIFO). Работает так же, как и стопка тарелок.

    .. image:: images/stack.png
        :width: 400px
    """
    def __init__(self):
        """
        Инициализатор. Стак работает с помощью
        :class:`~datastructures.LinkedLists.SinglyLinkedList`
        ,
        чтобы всё работало со сложностью алгоритма **O(1)**, вместо O(n). Такое решение было принято в связи с тем,
        что стаки работают на *сдвигах*. Если вы хотите работать со стаком как просто со списком, обращайтесь
        к параметру data: там находится
        :class:`~datastructures.LinkedLists.SinglyLinkedList`
        , на котором всё работает.
        """
        self.data = SinglyLinkedList()

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return self.data.__iter__()

    def push(self, item):
        """
        Положить наверх стопки новый элемент.

        :Сложность: O(1)
        :param item: Значение элемента, которого мы хотим положить наверх стопки
        """
        self.data.insert_first(item)

    def pop(self):
        """
        Удаляет верхний элемент.

        :Сложность: O(1)
        :return: Верхний элемент, который мы удаляем
        """
        return self.data.delete_first()

    def peek(self):
        """
        Узнать верхний элемент.

        :Сложность: O(1)
        :return: Значение верхнего элемента
        """
        return self.data.get_at(0)
