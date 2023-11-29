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
