from . import Queue, Stack


def get_path(prev_nodes: list, target: int) -> list:
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


class GraphNode:
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


class GraphParent(object):

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
        :param repeat: служебная переменная для избегания бесконечной рекурсии, используется для ненаправленных графов
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
        :param repeat: служебная переменная для избегания бесконечной рекурсии, используется для ненаправленных графов
        :return: вес удалённой грани
        """
        if not (0 <= v1 < self.size and 0 <= v2 < self.size):
            raise IndexError
        if not self.directed and repeat:
            self.remove_edge(v2, v1, False)

    def print_adjacency(self):
        """
        Вывести в консоль список / матрицу смежности.
        """
        raise NotImplementedError

    def traversal(self, from_node: int, storage_type: object = Queue):
        """
        Проходка по графу.

        :Сложность: O(V + E), где V -- количество вершин и E -- количество рёбер
        :param from_node: номер узла, от которого идёт проходка
        :param storage_type: структура, для управления узлами: очередь -- если в ширину, стэк -- если в глубину
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

    def shortest_path(self, from_node: int, to_node: int) -> (int, list):
        # TODO: Optimize, using heap / priority queue
        """
        Алгоритм Дейкстры. Находит самый короткий путь между двумя узлами.

        :Сложность: O(V\ :sup:`2`), где V - количество вершин
        :param from_node: индекс первого узла (откуда проложить маршрут)
        :param to_node: индекс второго узла (куда проложить маршрут)
        :returns: tuple (int, list)
            - Первый элемент -- это минимальная длина маршрута
            - Второй элемент -- это кратчайший маршрут: последовательность индексов, которые нужно посетить
        """
        raise NotImplementedError


class ListAdjacency(GraphParent):
    """
    Реализация графа через список смежности.
    """
    def __init__(self, size: int, directed: bool = True):
        super().__init__(size, directed)
        self.list = [None] * size

    def add_edge(self, v1: int, v2: int, weight: int = 1, repeat: bool = True):
        super().add_edge(v1, v2, weight, repeat)
        node = GraphNode(v2, weight)
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
            assert "No such edge"
            return -1
        tmp = head.weight
        if prev:
            prev.next = head.next
        else:
            self.list[v1] = head.next

        if repeat:
            return tmp

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

    def shortest_path(self, from_node: int, to_node: int) -> (int, list):
        visited = [False] * self.size
        distance = [float('inf')] * self.size
        parent = [-1] * self.size
        distance[from_node] = 0

        while True:
            # пока есть непосещённые узлы
            min_unvisited_node = -1
            min_dist = float('inf')

            for i in range(self.size):
                # поиск непосещённого узла, с минимальной дистанцией
                if not visited[i] and distance[i] < min_dist:
                    min_unvisited_node = i
                    min_dist = distance[i]

            if min_unvisited_node == -1:
                # выход из цикла
                break

            visited[min_unvisited_node] = True

            node = self.list[min_unvisited_node]
            while node:
                # перебор соседей
                if not visited[node.v2] and distance[min_unvisited_node] + node.weight < distance[node.v2]:
                    distance[node.v2] = distance[min_unvisited_node] + node.weight
                    parent[node.v2] = min_unvisited_node
                node = node.next

        # построение маршрута
        if distance[to_node] == float('inf'):
            # нет маршрута
            return -1, []
        return distance[to_node], get_path(parent, to_node)

    def traversal(self, from_node: int, storage_type: object):
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


class MatrixAdjacency(GraphParent):
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

    def print_adjacency(self):
        """
        Вывести матрицу в консоль.
        """
        for row in self.matrix:
            for column in row:
                print(column, end=" ")
            print()

    def shortest_path(self, from_node: int, to_node: int) -> (int, list):
        visited = [False] * self.size
        distance = [float('inf')] * self.size
        parent = [-1] * self.size
        distance[from_node] = 0

        while True:
            min_unvisited_node = -1
            min_dist = float("inf")

            for i in range(self.size):
                if not visited[i] and distance[i] < min_dist:
                    min_unvisited_node = i
                    min_dist = distance[i]

            if min_unvisited_node == -1:
                break

            visited[min_unvisited_node] = True

            for target in range(self.size):
                if self.matrix[min_unvisited_node][target] == 0:
                    continue
                new_distance = self.matrix[min_unvisited_node][target] + distance[min_unvisited_node]
                if new_distance < distance[target]:
                    distance[target] = new_distance
                    parent[target] = min_unvisited_node

        return distance[to_node], get_path(parent, to_node)

    def traversal(self, from_node: int, storage_type: object):
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
    