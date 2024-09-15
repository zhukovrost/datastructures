"""
Этот модуль содержит графы и алгоритмы, связанные с ними.
"""


from abc import ABC, abstractmethod
from .linear import Queue, Stack
from .heap import PriorityQueue


def _get_path(prev_nodes: list, target: int) -> list:
    """
    Находит путь до цели, используя список из индексов предыдущих узлов.

    :param prev_nodes: список из индексов предыдущих узлов
    :param target: целевой узел, до которого мы вычисляем путь
    :return: список -- последовательность индексов узлов
    """
    path = []
    trav = target
    while trav != -1:
        path.append(trav)
        trav = prev_nodes[trav]
    path.reverse()
    return path


def _default_heuristic(from_node: int, to_node: int) -> int:
    return abs(from_node - to_node)


class _GraphNode:
    """
    Узел графа. Нужен для реализации графа через *связанный список*
    """

    def __init__(self, v2: int, weight: int = 1):
        """
        Инициализатор.

        :param v2: куда
        :param weight: вес
        """
        self.v2 = v2
        self.weight = weight
        self.next = None

    def __str__(self):
        return f"(To: {self.v2}, Weight: {self.weight})"

    def __repr__(self):
        return self.__str__()


class _GraphParent(ABC):

    def __init__(self, size: int, directed: bool = True):
        """
        Инициализатор. Создает пустой граф.

        :param size: количество узлов / размер графа
        :param directed: направленный / ненаправленный граф
        """
        self.size = size
        self.directed = directed

    def __len__(self):
        return self.size

    def add_edge(self, v1: int, v2: int, weight: int = 1, repeat: bool = True):
        """
        Добавить грань.

        :param v1: номер 1го узла
        :param v2: номер 2го узла
        :param repeat: служебная переменная для избегания бесконечной рекурсии, \
        используется для ненаправленных графов
        :param weight: вес грани (его значение)
        """
        if not (0 <= v1 < self.size and 0 <= v2 < self.size):
            raise IndexError
        if not self.directed and repeat:
            self.add_edge(v2, v1, weight, False)

    def remove_edge(self, v1: int, v2: int, repeat: bool = True) -> int:
        """
        Убрать грань.

        :param v1: номер 1го узла
        :param v2: номер 2го узла
        :param repeat: служебная переменная для избегания бесконечной рекурсии, \
        используется для ненаправленных графов
        :return: вес удалённой грани
        """
        if not (0 <= v1 < self.size and 0 <= v2 < self.size):
            raise IndexError
        if not self.directed and repeat:
            self.remove_edge(v2, v1, False)

    @abstractmethod
    def print_adjacency(self):
        """
        Вывести в консоль список / матрицу смежности.
        """
        raise NotImplementedError

    @abstractmethod
    def traversal(self, from_node: int, storage_type: object):
        """
        Проходка по графу.

        :Сложность: O(V + E), где V -- количество вершин и E -- количество рёбер
        :param from_node: номер узла, от которого идёт проходка
        :param storage_type: структура, для управления узлами: \
        очередь -- если в ширину, стэк -- если в глубину
        :return: итерационный объект с номерами узлов
        """
        raise NotImplementedError

    def breadth_first_traversal(self, from_node: int):
        """
        Обход графа в ширину. (*BFT -- Breadth First Traversal*).

        .. image:: images/graph-bfs.gif
            :width: 400px

        :Сложность: O(V + E), где V -- количество вершин и E -- количество рёбер
        :param from_node: номер узла, от которого идёт проходка
        :return: итерационный объект с номерами узлов
        """
        return self.traversal(from_node, Queue)

    def depth_first_traversal(self, from_node: int):
        """
        Обход графа в глубину. (*DFT -- Depth First Traversal*).

        .. image:: images/graph-dfs.gif
            :width: 400px

        :Сложность: O(V + E), где V -- количество вершин и E -- количество рёбер
        :param from_node: номер узла, от которого идёт проходка
        :return: итерационный объект с номерами узлов
        """
        return self.traversal(from_node, Stack)

    @abstractmethod
    def dijkstra(self, from_node: int, to_node: int) -> (int, list):
        """
        Алгоритм Дейкстры. Находит самый короткий путь между двумя узлами.

        **Не поддерживает отрицательные веса.**

        :Сложность: O((V + E) log V), где V - количество вершин
        :param from_node: индекс первого узла (откуда проложить маршрут)
        :param to_node: индекс второго узла (куда проложить маршрут)
        :returns: tuple (int, list)
            - Первый элемент -- это минимальная длина маршрута
            - Второй элемент -- это кратчайший маршрут: последовательность индексов, \
            которые нужно посетить
        """
        raise NotImplementedError


    @abstractmethod
    def bellman_ford(self, from_node: int, to_node: int) -> (int, list):
        """
        Алгоритм Беллмана-Форда. Находит самый короткий путь между двумя узлами.

        **Не поддерживает убывающие циклы. Поддерживает отрицательные веса.**

        :Сложность: O(V * E), где V - количество вершин, а E - количество рёбер
        :param from_node: индекс первого узла (откуда проложить маршрут)
        :param to_node: индекс второго узла (куда проложить маршрут)
        :returns: tuple (int, list)
            - Первый элемент -- это минимальная длина маршрута
            - Второй элемент -- это кратчайший маршрут: последовательность индексов, \
            которые нужно посетить
        """
        raise NotImplementedError


    @abstractmethod
    def a_star(self, from_node: int, to_node: int, heuristic: callable) -> (int, list):
        """
        Алгоритм A*. Находит самый короткий путь между двумя узлами.
        Этот алгоритм является усовершенствованным алгоритмом Дейкстры.
        Он не рассматривает все возможные пути.

        .. image :: images/a_star.gif

        :Сложность: O((V + E) log V), где V - количество вершин, а E - количество рёбер в худшем случае
        :param from_node: индекс первого узла (откуда проложить маршрут)
        :param to_node: индекс второго узла (куда проложить маршрут)
        :param heuristic: функция эвристики для оценки стоимости пути (h(n))
        :returns: tuple (int, list)
            - Первый элемент -- это минимальная длина маршрута
            - Второй элемент -- это кратчайший маршрут: последовательность индексов, которые нужно посетить
        """
        raise NotImplementedError


class ListAdjacency(_GraphParent):
    """
    Реализация графа через список смежности.
    """
    def __init__(self, size: int, directed: bool = True):
        super().__init__(size, directed)
        self.list = [None] * size

    def add_edge(self, v1: int, v2: int, weight: int = 1, repeat: bool = True):
        super().add_edge(v1, v2, weight, repeat)
        node = _GraphNode(v2, weight)
        node.next = self.list[v1]
        self.list[v1] = node

    def remove_edge(self, v1: int, v2: int, repeat: bool = True) -> int:
        super().remove_edge(v1, v2, repeat)
        head = self.list[v1]
        prev = None
        while head and head.v2 != v2:
            prev = head
            head = head.next

        if not head:
            return -1
        tmp = head.weight
        if prev:
            prev.next = head.next
        else:
            self.list[v1] = head.next

        if repeat:
            return tmp

        return 0

    def print_adjacency(self):
        """
        Вывести в консоль список смежности.
        """
        for i in range(self.size):
            v1 = self.list[i]
            print("From:", i, end="")
            while v1:
                print(' -> ', v1, sep='', end='')
                v1 = v1.next
            print()

    def dijkstra(self, from_node: int, to_node: int) -> (int, list):
        visited = [False] * self.size
        distance = [float('inf')] * self.size
        parent = [-1] * self.size
        distance[from_node] = 0

        h = PriorityQueue()
        h.enqueue(from_node, 0)

        while len(h) > 0:
            current_node = h.dequeue()
            if visited[current_node]:
                continue

            visited[current_node] = True
            node = self.list[current_node]
            while node:
                if node.weight < 0:
                    raise ValueError("Алгоритм Дейкстры не поддерживает отрицательные рёбра.")

                # перебор соседей
                if not visited[node.v2] and distance[current_node] + node.weight \
                        < distance[node.v2]:
                    distance[node.v2] = distance[current_node] + node.weight
                    parent[node.v2] = current_node
                    h.enqueue(node.v2, node.weight)
                node = node.next

        # построение маршрута
        if distance[to_node] == float('inf'):
            # нет маршрута
            return -1, []
        return distance[to_node], _get_path(parent, to_node)

    def a_star(self, from_node: int, to_node: int, heuristic: callable = None) -> (int, list):
        if heuristic is None:
            heuristic = _default_heuristic

        visited = [False] * self.size
        distance = [float('inf')] * self.size
        parent = [-1] * self.size
        distance[from_node] = 0

        h = PriorityQueue()
        h.enqueue(from_node, 0)

        while len(h) > 0:
            current_node = h.dequeue()
            if visited[current_node]:
                continue

            # Если мы достигли целевого узла, выходим из цикла
            if current_node == to_node:
                break

            visited[current_node] = True
            node = self.list[current_node]
            while node:
                # перебор соседей
                if not visited[node.v2]:
                    g = distance[current_node] + node.weight
                    if g < distance[node.v2]:
                        distance[node.v2] = g
                        parent[node.v2] = current_node
                        f_score = g + heuristic()
                        h.enqueue(node.v2, f_score)
                node = node.next

        # Построение маршрута
        if distance[to_node] == float('inf'):
            # Нет маршрута
            return -1, []

        return distance[to_node], _get_path(parent, to_node)

    def bellman_ford(self, from_node: int, to_node: int) -> (int, list):
        distance = [float('inf')] * self.size
        parent = [-1] * self.size
        distance[from_node] = 0

        for _ in range(self.size - 1):
            for i in range(self.size):
                node = self.list[i]
                while node:
                    if distance[i] != float('inf') and \
                            distance[i] + node.weight < distance[node.v2]:
                        distance[node.v2] = distance[i] + node.weight
                        parent[node.v2] = i
                    node = node.next

        # Проверяем наличие отрицательных циклов
        for i in range(self.size):
            node = self.list[i]
            while node:
                if distance[i] != float('inf') and distance[i] + node.weight < distance[node.v2]:
                    raise ValueError("Граф содержит отрицательный цикл")
                node = node.next

        if distance[to_node] == float('inf'):
            return -1, []

        return distance[to_node], _get_path(parent, to_node)

    def traversal(self, from_node: int, storage_type: type):
        storage = storage_type()
        storage.push(from_node)
        visited = set()
        visited.add(from_node)
        while storage:
            node_num = storage.pop()

            yield node_num

            trav = self.list[node_num]
            while trav:
                if trav.v2 not in visited:
                    storage.push(trav.v2)
                    visited.add(trav.v2)
                trav = trav.next


class MatrixAdjacency(_GraphParent):
    """
    Реализация графа через матрицу смежности.
    """
    def __init__(self, size: int, directed: bool = True):
        super().__init__(size, directed)
        self.matrix = []
        for _ in range(size):
            self.matrix.append([0 for _ in range(size)])

    def add_edge(self, v1: int, v2: int, weight: int = 1, repeat: bool = True) -> None:
        super().add_edge(v1, v2, weight, repeat)
        self.matrix[v1][v2] = weight

    def remove_edge(self, v1: int, v2: int, repeat: bool = True) -> int:
        super().remove_edge(v1, v2, repeat)
        tmp = self.matrix[v1][v2]
        self.matrix[v1][v2] = 0
        if repeat:
            return tmp
        return 0

    def print_adjacency(self):
        """
        Вывести матрицу в консоль.
        """
        for row in self.matrix:
            for column in row:
                print(column, end=" ")
            print()

    def dijkstra(self, from_node: int, to_node: int) -> (int, list):
        visited = [False] * self.size
        distance = [float('inf')] * self.size
        parent = [-1] * self.size
        distance[from_node] = 0

        h = PriorityQueue()
        h.enqueue(from_node, 0)

        while len(h) > 0:
            current_node = h.dequeue()
            if visited[current_node]:
                continue

            visited[current_node] = True
            for neighbour in range(self.size):
                if self.matrix[current_node][neighbour] == 0:
                    continue
                new_distance = self.matrix[current_node][neighbour] + distance[current_node]
                if new_distance < distance[neighbour]:
                    distance[neighbour] = new_distance
                    parent[neighbour] = current_node
                    h.enqueue(neighbour, new_distance)

        return distance[to_node], _get_path(parent, to_node)

    def bellman_ford(self, from_node: int, to_node: int) -> (int, list):
        distance = [float('inf')] * self.size
        parent = [-1] * self.size
        distance[from_node] = 0

        for _ in range(self.size - 1):
            for v1 in range(self.size):
                for v2 in range(self.size):
                    weight = self.matrix[v1][v2]
                    if weight != 0 and distance[v1] != float('inf') \
                            and distance[v1] + weight < distance[v2]:
                        distance[v2] = distance[v1] + weight
                        parent[v2] = v1

        # Проверяем наличие отрицательных циклов
        for v1 in range(self.size):
            for v2 in range(self.size):
                weight = self.matrix[v1][v2]
                if weight != 0 and distance[v1] != float('inf') \
                        and distance[v1] + weight < distance[v2]:
                    raise ValueError("Граф содержит отрицательный цикл")

        if distance[to_node] == float('inf'):
            return -1, []

        return distance[to_node], _get_path(parent, to_node)

    def a_star(self, from_node: int, to_node: int, heuristic: callable = None) -> (int, list):
        if heuristic is None:
            heuristic = _default_heuristic

        visited = [False] * self.size
        distance = [float('inf')] * self.size
        parent = [-1] * self.size
        distance[from_node] = 0

        h = PriorityQueue()
        h.enqueue(from_node, heuristic(from_node, to_node))

        while len(h) > 0:
            current_node = h.dequeue()
            if current_node == to_node:
                break
            if visited[current_node]:
                continue

            visited[current_node] = True

            for neighbour in range(self.size):
                if self.matrix[current_node][neighbour] == 0:
                    continue
                g = self.matrix[current_node][neighbour] + distance[current_node]
                if g < distance[neighbour]:
                    distance[neighbour] = g
                    parent[neighbour] = current_node
                    f_score = g + heuristic(neighbour, to_node)
                    h.enqueue(neighbour, f_score)

        if distance[to_node] == float('inf'):
            return -1, []

        return distance[to_node], _get_path(parent, to_node)

    def traversal(self, from_node: int, storage_type: type):
        storage = storage_type()
        storage.push(from_node)
        visited = set()
        visited.add(from_node)
        while storage:
            node_num = storage.pop()

            yield node_num

            for i in range(self.size):
                if self.matrix[node_num][i] > 0 and i not in visited:
                    storage.push(i)
                    visited.add(i)
    