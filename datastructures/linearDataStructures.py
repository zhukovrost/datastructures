class SinglyLinkedListNode:
    """
    Этот класс представляет собой узел связанного списка (:class:`~SinglyLinkedList`).
    """

    def __init__(self, data):
        """
        Инициализация узла

        :param data: данные, которые хранит узел
        """
        self.data = data
        self.next = None

    def later_node(self, i: int):
        """
        Рекурсивная функция обхода списка. От начала до конца.

        :Сложность: O(i)
        :param i: номер узла последовательности
        :return: i-ый узел последовательности
        """
        if i == 0:
            return self
        if not self.next:
            raise IndexError
        return self.next.later_node(i - 1)

    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.data == other.data
        return self.data == other

    def __lt__(self, other):
        if hasattr(other, '__lt__'):
            return self.data < other
        return False

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        if hasattr(other, '__gt__'):
            return self.data > other
        return False

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)


class SinglyLinkedList:
    """
    Список связан единичными узлами (:class:`~SinglyLinkedListNode`): они хранят указатели **только** на следующий узел.

    .. image:: images/singly-linked-list.png
    """

    def __init__(self):
        """
        Инициализатор.
        """
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        trav = self.head
        while trav:
            yield trav.data
            trav = trav.next

    def __str__(self):
        return " -> ".join(map(str, self.__iter__()))

    def __bool__(self):
        return len(self) > 0

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(self) != len(other):
                return False

            for node_self, node_other in zip(self, other):
                if node_self != node_other:
                    return False

            return True

        elif hasattr(other, '__iter__'):
            return list(self) == list(other)

        return False

    def build(self, datalist: list):
        """
        Преобразует входящий список в LinkedList.

        :Сложность: O(n)
        :param datalist: обычный список
        """
        for data in reversed(datalist):
            self.insert_first(data)

    def get_at(self, i: int):
        """
        Получить данные i-го узла.

        :Сложность: O(i)
        :param i: индекс искомого узла
        :return: данные искомого узла
        """
        node = self.head.later_node(i)
        return node.data

    def __getitem__(self, i):
        return self.get_at(i)

    def set_at(self, i: int, data):
        """
        Меняет данные на data в i-ом узле.

        :Сложность: O(i)
        :param i: индекс узла
        :param data: устанавливаемые данные
        """
        node = self.head.later_node(i)
        node.data = data

    def __setitem__(self, key, value):
        self.set_at(key, value)

    def insert_first(self, data):
        """
        Вставляет узел на 0-ую позицию.

        :Сложность: O(1)
        :param data: Данные, которые будут вставлены в список
        """
        new_node = SinglyLinkedListNode(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def delete_first(self):
        """
        Удаляет первый узел списка.

        :Сложность: O(1)
        :return: удаляемый узел списка
        """
        temp = self.head.data
        self.head = self.head.next
        self.size -= 1
        return temp

    def insert_at(self, i: int, data):
        """
        Вставляет новый узел на i-ую позицию.

        :Сложность: O(i)
        :param i: индекс позиции нового узла
        :param data: данные нового узла
        """
        if i == 0:
            self.insert_first(data)
            return

        prev_node = self.head.later_node(i - 1)
        new_node = SinglyLinkedListNode(data)
        new_node.next = prev_node.next
        prev_node.next = new_node
        self.size += 1

    def delete_at(self, i: int):
        """
        Удаляет узел на i-ой позиции.

        :Сложность: O(i)
        :param i: индекс узла
        :return: данные удаляемого узла
        """
        if i == 0:
            return self.delete_first()

        prev_node = self.head.later_node(i - 1)
        data = prev_node.next.data
        prev_node.next = prev_node.next.next
        self.size -= 1
        return data

    def insert_last(self, data):
        """
        Добавляет узел в конец списка.

        :Сложность: O(n)
        :param data: данные нового узла
        """
        self.insert_at(len(self), data)

    def delete_last(self):
        """
        Удаляет последний узел.

        :Сложность: O(n)
        :return: данные удаляемого узла
        """
        return self.delete_at(len(self) - 1)

    def search(self, data):
        """
        Поиск узла.

        :Сложность: O(n)
        :param data: искомое значение
        :return: индекс узла, либо -1, если узел не найден
        """
        for item in enumerate(self):
            if item[1] == data:
                return item[0]
        return -1

    def consists(self, data):
        """
        Содержит ли список узел.

        :Сложность: O(n)
        :param data: искомое значение
        :return: True - если содержит, иначе False
        """
        return self.search(data) != -1


class DoublyLinkedListNode(SinglyLinkedListNode):
    """
    Этот класс представляет собой узел двойного связанного списка (:class:`~DoublyLinkedList`).
    Он занимает в два раза больше памяти, потому что имеет указатель как и на следующий, так и на предыдущий узел.
    """

    def __init__(self, data):
        """
        Инициализация узла

        :param data: данные, которые хранит узел
        """
        super().__init__(data)
        self.previous = None

    def earlier_node(self, i: int):
        """
        Рекурсивная функция обхода списка от конца до начала.

        :Сложность: O(i)
        :param i: номер узла последовательности **от конца**
        :return: i-ый узел последовательности **от конца**
        """
        if i == 0:
            return self
        if not self.previous:
            raise IndexError
        return self.previous.earlier_node(i - 1)


class DoublyLinkedList(SinglyLinkedList):
    """
    Список связан двойными узлами (:class:`~DoublyLinkedListNode`):
    они хранят указатели как на предыдущий узел, так и на следующий.

    .. image:: images/doubly-linked-list.png
    """

    def __init__(self):
        """
        Инициализатор.
        """
        super().__init__()
        self.tail = None

    # __len__ и __iter__ из наследуемого класса

    def build(self, datalist: list):
        """
        Преобразует входящий список в LinkedList.

        :Сложность: O(n)
        :param datalist: обычный список
        """
        for data in datalist:
            self.insert_last(data)

    def get_at(self, i: int):
        """
        Получить данные i-го узла.

        :Сложность: O(i/2)
        :param i: индекс искомого узла
        :return: данные искомого узла
        """
        if len(self) - i - 1 < i:
            node = self.tail.earlier_node(len(self) - i - 1)
        else:
            node = self.head.later_node(i)
        return node.data

    def set_at(self, i: int, data):
        """
        Меняет данные на data в i-ом узле.

        :Сложность: O(i/2)
        :param i: индекс узла
        :param data: устанавливаемые данные
        """
        if len(self) - i - 1 < i:
            node = self.tail.earlier_node(len(self) - i - 1)
        else:
            node = self.head.later_node(i)
        node.data = data

    def insert_first(self, data):
        """
        Вставляет узел на 0-ую позицию.

        :Сложность: O(1)
        :param data: Данные, которые будут вставлены в список
        """
        new_node = DoublyLinkedListNode(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

        if self.size == 1:
            self.tail = new_node
            return

        new_node.next.previous = new_node

    def insert_last(self, data):
        """
        Вставляет узел на последнюю позицию.

        :Сложность: O(1)
        :param data: Данные, которые будут вставлены в список
        """
        new_node = DoublyLinkedListNode(data)
        new_node.previous = self.tail
        self.tail = new_node
        self.size += 1

        if self.size == 1:
            self.head = new_node
            return

        new_node.previous.next = new_node

    def delete_first(self):
        """
        Удаляет первый узел списка.

        :Сложность: O(1)
        :return: удаляемый узел списка
        """
        data = self.head.data
        self.head = self.head.next
        if self.head:
            self.head.previous = None
        self.size -= 1
        return data

    def delete_last(self):
        """
        Удаляет последний узел списка.

        :Сложность: O(1)
        :return: удаляемый узел списка
        """

        data = self.tail.data
        self.tail = self.tail.previous
        if self.tail:
            self.tail.next = None
        self.size -= 1
        return data

    def insert_at(self, i: int, data):
        """
        Вставляет новый узел на i-ую позицию.

        :Сложность: ~O(i/2)
        :param i: индекс позиции нового узла
        :param data: данные нового узла
        """
        if i == 0:
            self.insert_first(data)
            return
        if i == len(self):
            self.insert_last(data)
            return

        if i <= len(self) - i - 2:
            prev_node = self.head.later_node(i - 1)
        else:
            prev_node = self.tail.earlier_node(len(self) - i)

        new_node = DoublyLinkedListNode(data)
        new_node.next = prev_node.next
        prev_node.next = new_node
        new_node.previous = prev_node
        new_node.next.previous = new_node
        self.size += 1

    def delete_at(self, i: int):
        """
        Удаляет узел на i-ой позиции.

        :Сложность: ~O(i/2)
        :param i: индекс узла
        :return: данные удаляемого узла
        """
        if i == 0:
            self.delete_first()
            return
        if i == len(self) - 1:
            self.delete_last()

        if i <= len(self) - i - 2:
            prev_node = self.head.later_node(i - 1)
        else:
            prev_node = self.tail.earlier_node(len(self) - i)

        data = prev_node.next.data
        prev_node.next.next.prev = prev_node
        prev_node.next = prev_node.next.next
        self.size -= 1
        return data


class StaticArray:
    """
    Обычный нерасширяемый список

    .. image:: images/static-array.png
        :width: 300px
    """

    def __init__(self, n: int):
        """
        Инициализация статичного списка.

        :param n: Длина списка
        """
        self.data = [None] * n

    def __iter__(self):
        for item in self.data:
            yield item

    def __bool__(self):
        return len(self.data) > 0

    def __str__(self):
        return self.data.__str__()

    def __eq__(self, other):
        if hasattr(other, '__iter__'):
            return list(self) == list(other)

        return False

    def get_at(self, i: int):
        """
        Получить элемент.

        :Сложность: O(1)
        :param i: Индекс элемента
        :return: Данные под i-ым индексом
        """
        if not (0 <= i < len(self.data)):
            raise IndexError
        return self.data[i]

    def __getitem__(self, i):
        return self.get_at(i)

    def set_at(self, i: int, item):
        """
        Установить значение элемента.

        :Сложность: O(1)
        :param i: Индекс элемента
        :param item: Значение элемента
        """
        if not (0 <= i < len(self.data)):
            raise IndexError
        self.data[i] = item

    def __setitem__(self, key, value):
        self.set_at(key, value)

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
        Инициализатор. Стак работает с помощью :class:`~SinglyLinkedList`,
        чтобы всё работало со сложностью алгоритма **O(1)**, вместо O(n). Такое решение было принято в связи с тем,
        что стаки работают на *сдвигах* и с *крайними элементами списка*. Если вы хотите работать со
        стаком как просто со списком, обращайтесь к параметру `data`:
        там находится :class:`~SinglyLinkedList`, на котором всё работает.
        """
        self.data = SinglyLinkedList()

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return self.data.__iter__()

    def __bool__(self):
        return len(self.data) > 0

    def __str__(self):
        return self.data.__str__()

    def __getitem__(self, i):
        return self.data.__getitem__(i)

    def __setitem__(self, key, value):
        self.data.__setitem__(key, value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.data == other.data
        elif hasattr(other, '__iter__'):
            return list(self) == list(other)
        return False

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
        Инициализатор. Очередь работает с помощью :class:`~DoublyLinkedList`,
        чтобы всё работало со сложностью алгоритма **O(1)**, вместо O(n). Такое решение было принято в связи с тем,
        что очереди работают на *сдвигах* и с *крайними элементами списка*. Если вы хотите работать с очередью как
        просто со списком, обращайтесь к параметру `data`: там находится
        :class:`~DoublyLinkedList`, на котором всё работает.
        """
        self.data = DoublyLinkedList()

    def __len__(self):
        return self.data.__len__()

    def __iter__(self):
        return self.data.__iter__()

    def __bool__(self):
        return len(self.data) > 0

    def __str__(self):
        return self.data.__str__()

    def __getitem__(self, i):
        return self.data.__getitem__(i)

    def __setitem__(self, key, value):
        self.data.__setitem__(key, value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.data == other.data
        elif hasattr(other, '__iter__'):
            return list(self) == list(other)
        return False

    def enqueue(self, item):
        """
        Поставить в очередь предмет. (Сделать последним элементом *item*)

        :Сложность: O(1)
        :param item: Значение элемента очереди, который мы ставим
        """
        self.data.insert_last(item)

    def push(self, item):
        self.enqueue(item)

    def dequeue(self):
        """
        Вынуть из очереди следующий (первый) элемент.

        :Сложность: O(1)
        :return: Значение элемента, которого мы вынимаем
        """
        return self.data.delete_first()

    def pop(self):
        return self.dequeue()

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


class Deque(Queue):
    """
    Двусторонняя очередь.

    .. image:: images/deque.jpg
    """
    def push_front(self, item):
        """
        Поставить новый элемент в начало по порядку.

        :Сложность: O(1)
        :param item: значение нового элемента.
        """
        self.data.insert_first(item)

    def push_back(self, item):
        """
        Поставить новый элемент в конец по порядку.

        :Сложность: O(1)
        :param item: значение нового элемента.
        """
        super().enqueue(item)

    def pop_front(self):
        """
        Выбрасывает из очереди первый элемент по порядку.

        :Сложность: O(1)
        :return: значение выбрасываемого элемента
        """
        return super().dequeue()

    def pop_back(self):
        """
        Выбрасывает из очереди последний элемент по порядку.

        :Сложность: O(1)
        :return: значение выбрасываемого элемента
        """
        return self.data.delete_last()

    def enqueue(self, item):
        """
        **Для работы как с обычной очередью:** поставить в очередь предмет. (Сделать последним элементом *item*)

        :Сложность: O(1)
        :param item: Значение элемента очереди, который мы ставим
        """
        super().enqueue(item)

    def dequeue(self):
        """
        **Для работы как с обычной очередью:** вынуть из очереди следующий (первый) элемент.

        :Сложность: O(1)
        :return: Значение элемента, которого мы вынимаем
        """
        return super().dequeue()
