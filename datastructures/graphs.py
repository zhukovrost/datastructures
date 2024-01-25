# TODO: zero weight parameter
# TODO: Refactor, Graph interface maybe


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


class GraphList:
    def __init__(self, size: int, directed: bool = True):
        """
        Инициализатор. Создает пустой список, в котором будут узлы графа.

        :param size: размер матрицы
        :param directed: направленный/ненаправленный граф
        """
        self.size = size
        self.directed = directed
        self.list = [None] * size

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
        assert 0 <= v1 < self.size and 0 <= v2 < self.size
        node = GraphNode(v2, weight)
        node.next = self.list[v1]
        self.list[v1] = node
        if not self.directed and repeat:
            self.add_edge(v2, v2, False)

    def remove_edge(self, v1: int, v2: int, repeat: bool = True) -> int:
        """
        Убрать грань.

        :param v1: номер 1го узла
        :param v2: номер 2го узла
        :param repeat: служебная переменная для избегания бесконечной рекурсии, используется для ненаправленных графов
        :return: вес удалённой грани
        """
        assert 0 <= v1 < self.size and 0 <= v2 < self.size
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

        if not self.directed and repeat:
            self.remove_edge(v2, v1, False)

        return tmp

    def print_list(self):
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
        # TODO: Optimize, using heap / priority queue
        """
        Алгоритм Дейкстры. Находит самый короткий путь между двумя узлами.

        :Сложность: O(n\ :sup:`2`)
        :param from_node: индекс первого узла (откуда проложить маршрут)
        :param to_node: индекс второго узла (куда проложить маршрут)
        :returns: tuple (int, list)
            - Первый элемент -- это минимальная длина маршрута
            - Второй элемент -- это кратчайший маршрут: последовательность индексов, которые нужно посетить
        """
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


class GraphMatrix:
    """
    Реализация графа через матрицу смежности.
    """
    def __init__(self, size: int, directed: bool = True):
        """
        Инициализатор. Создает пустую матрицу смежности размером *size x size*.

        :param size: размер матрицы
        :param directed: направленный/ненаправленный граф
        """
        self.size = size
        self.directed = directed
        self.matrix = []
        for i in range(size):
            self.matrix.append([0 for _ in range(size)])

    def __len__(self):
        return self.size

    def add_edge(self, v1: int, v2: int, weight: int = 1) -> None:
        """
        Добавить грань.

        :param v1: номер 1го узла
        :param v2: номер 2го узла
        :param weight: вес грани (его значение)
        """
        assert 0 <= v1 < self.size and 0 <= v2 < self.size
        self.matrix[v1][v2] = weight
        if not self.directed:
            self.matrix[v2][v1] = weight

    def remove_edge(self, v1: int, v2: int) -> int:
        """
        Убрать грань.

        :param v1: номер 1го узла
        :param v2: номер 2го узла
        :return: вес удалённой грани
        """
        assert 0 <= v1 < self.size and 0 <= v2 < self.size
        tmp = self.matrix[v1][v2]
        self.matrix[v1][v2] = 0
        if not self.directed:
            self.matrix[v2][v1] = 0
        return tmp

    def print_matrix(self):
        """
        Вывести матрицу в консоль.
        """
        for row in self.matrix:
            for column in row:
                print(column, end=" ")
            print()

    def shortest_path(self, from_node: int, to_node: int) -> (int, list):
        # TODO: Optimize, using heap
        """
        Алгоритм Дейкстры. Находит самый короткий путь между двумя узлами.

        :Сложность: O(n\ :sup:`2`)
        :param from_node: индекс первого узла (откуда проложить маршрут)
        :param to_node: индекс второго узла (куда проложить маршрут)
        :returns: tuple (int, list)
            - Первый элемент -- это минимальная длина маршрута
            - Второй элемент -- это кратчайший маршрут: последовательность индексов, которые нужно посетить
        """
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
