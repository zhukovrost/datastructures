from datastructures.LinkedLists import SinglyLinkedList, DoublyLinkedList


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
    **Last in - First out** список (LIFO). Альтернативное название: стак/стэк. Работает так же, как и стопка тарелок.

    .. image:: images/stack.png
        :width: 400px
    """
    def __init__(self):
        """
        Инициализатор. Стак работает с помощью
        :class:`~datastructures.LinkedLists.SinglyLinkedList`
        ,
        чтобы всё работало со сложностью алгоритма **O(1)**, вместо O(n). Такое решение было принято в связи с тем,
        что стаки работают на *сдвигах* и с *крайними элементами списка*. Если вы хотите работать со стаком как просто со списком, обращайтесь
        к параметру `data`: там находится
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

    def peek_bottom(self):
        """
        Узнать нижний элемент.

        :Сложность: O(n)
        :return: Значение нижнего элемента
        """
        return self.data.get_at(len(self))


class Queue:
    """
    **First in - First out** список (FIFO). Альтернативное название: очередь. Работает так же, как очередь в пивнушке.

    .. image:: images/queue.png
        :width: 400px
    """
    def __init__(self):
        """
        Инициализатор. Очередь работает с помощью
        :class:`~datastructures.LinkedLists.DoublyLinkedList`
        ,
        чтобы всё работало со сложностью алгоритма **O(1)**, вместо O(n). Такое решение было принято в связи с тем,
        что очереди работают на *сдвигах* и с *крайними элементами списка*. Если вы хотите работать с очередью как
        просто со списком, обращайтесь к параметру `data`: там находится
        :class:`~datastructures.LinkedLists.DoublyLinkedList`
        , на котором всё работает.
        """
        self.data = DoublyLinkedList()

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return self.data.__iter__()

    def enqueue(self, item):
        """
        Поставить в очередь предмет.

        :Сложность: O(1)
        :param item: Значение элемента очереди, который мы ставим
        """
        self.data.insert_last(item)

    def dequeue(self):
        """
        Вынуть из очереди следующий (первый) элемент.

        :Сложность: O(1)
        :return: Значение элемента, которого мы вынимаем
        """
        return self.data.delete_first()

    def peek_front(self):
        """
        Узнать первый элемент очереди. Он же голова, он же следующий элемент очереди.

        :Сложность: O(1)
        :return: Первый элемент очереди
        """
        return self.data.get_at(0)

    def peek_back(self):
        """
        Узнать последний элемент очереди. Он же хвост, он же конечный элемент очереди.

        :Сложность: O(1)
        :return: Последний элемент очереди
        """
        return self.data.get_at(len(self) - 1)
