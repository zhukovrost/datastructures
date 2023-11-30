class SinglyLinkedListNode:
    """
    Этот класс представляет собой узел связанного списка (
    :class:`~datastructures.LinkedLists.SinglyLinkedList`
    ).
    """

    def __init__(self, data):
        """
        Инициализация узла

        :param data: данные, которые хранит узел
        """
        self.data = data
        self.next = None

    def later_node(self, i):
        """
        Рекурсивная функция обхода списка. От начала до конца.

        :Сложность: O(i)
        :param i: номер узла последовательности
        :return: i-ый узел последовательности
        """
        if i == 0:
            return self
        assert self.next
        return self.next.later_node(i - 1)


class SinglyLinkedList:
    """
    Список связан единичными узлами (
    :class:`~datastructures.LinkedLists.SinglyLinkedListNode`
    ): они хранят указатели **только** на следующий узел.

    .. image:: images/singly-linked-list.png
    """
    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        trav = self.head
        while trav:
            yield trav.data
            trav = trav.next

    def build(self, datalist):
        """
        Преобразует входящий список в LinkedList.

        :Сложность: O(n)
        :param datalist: обычный список
        """
        for data in reversed(datalist):
            self.insert_first(data)

    def get_at(self, i):
        """
        Получить данные i-го узла.

        :Сложность: O(i)
        :param i: индекс искомого узла
        :return: данные искомого узла
        """
        node = self.head.later_node(i)
        return node.data

    def set_at(self, i, data):
        """
        Меняет данные на data в i-ом узле.

        :Сложность: O(i)
        :param i: индекс узла
        :param data: устанавливаемые данные
        """
        node = self.head.later_node(i)
        node.data = data

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

    def insert_at(self, i, data):
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

    def delete_at(self, i):
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
    Этот класс представляет собой узел двойного связанного списка (
    :class:`~datastructures.LinkedLists.DoublyLinkedList`
    ). Он занимает в два раза больше памяти, потому что имеет указатель как и на следующий, так и на предыдущий узел.
    """

    def __init__(self, data):
        """
        Инициализация узла

        :param data: данные, которые хранит узел
        """
        super().__init__(data)
        self.previous = None

    def earlier_node(self, i):
        """
        Рекурсивная функция обхода списка от конца до начала.

        :Сложность: O(i)
        :param i: номер узла последовательности **от конца**
        :return: i-ый узел последовательности **от конца**
        """
        if i == 0:
            return self
        assert self.previous
        return self.previous.earlier_node(i - 1)


class DoublyLinkedList(SinglyLinkedList):
    """
    Список связан двойными узлами (
    :class:`~datastructures.LinkedLists.DoublyLinkedListNode`
    ): они хранят указатели как на предыдущий узел, так и на следующий.

    .. image:: images/doubly-linked-list.png
    """
    def __init__(self):
        super().__init__()
        self.tail = None

    # __len__ и __iter__ из наследуемого класса

    def build(self, datalist):
        """
        Преобразует входящий список в LinkedList.

        :Сложность: O(n)
        :param datalist: обычный список
        """
        for data in datalist:
            self.insert_last(data)

    def get_at(self, i):
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

    def set_at(self, i, data):
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
        self.tail.next = None
        self.size -= 1
        return data

    def insert_at(self, i, data):
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

    def delete_at(self, i):
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
