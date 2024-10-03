"""
Этот модуль содержит различные узлы бинарных деревьев.
Эти узы используются в , но их также можно использовать отдельно.
У узлов :class:`~BinaryNode`
и :class:`~BalancingNode` нет своих деревьев.
"""


from abc import ABC, abstractmethod

from aptdaemon.logger import BLACK

from ..linear import Queue


def height(node) -> int:
    """
    Возвращает высоту входящего узла. Сложность алгоритма является **O(1)**
    вместо O(h), потому что каждый узел хранит в себе значение его высоты.
    При каждом изменении дерева это значение обновляется при необходимости.

    :Сложность: O(1)
    :param node: узел, высоту которого надо узнать
    :return: высота узла и, если узла нет, -1
    """
    if node:
        return node.height
    return -1


class Node(ABC):
    """
    Абстрактный класс, который описывает основные свойства узлов дерева.
    """

    @property
    @abstractmethod
    def parent(self):
        raise NotImplementedError

    @parent.setter
    @abstractmethod
    def parent(self, value):
        raise NotImplementedError

    @property
    @abstractmethod
    def left(self):
        raise NotImplementedError

    @left.setter
    @abstractmethod
    def left(self, value):
        raise NotImplementedError

    @property
    @abstractmethod
    def right(self):
        raise NotImplementedError

    @right.setter
    @abstractmethod
    def right(self, value):
        raise NotImplementedError

    @abstractmethod
    def maintain(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self):
        raise NotImplementedError

    @data.setter
    @abstractmethod
    def data(self, value):
        raise NotImplementedError


class BinaryNode(Node):
    """
    Узел бинарного дерева.
    """

    def __init__(self, item):
        """
        Инициализатор.

        :param item: Значение узла
        """
        self._data = item
        self._parent = None
        self._right = None
        self._left = None

    def __repr__(self):
        return f"Node({self.data})"

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def maintain(self):
        """
        Функция вызывается после удаления или вставки узла (*уже прописано в коде*).
        Заготовка.
        """

    def subtree_iter(self):
        """
        Рекурсивный обход дерева `по порядку` (in-order traversal), также `центрированный`.
        Является одним из трёх обходов в глубину (**DFS** - `Depth First Search`).

        Алгоритм обхода по порядку:
            #. Обойти левое *поддерево* (рекурсивно).
            #. *Выбросить* (оператор yield) *корень*.
            #. Обойти правое *поддерево* (рекурсивно).

        .. image:: images/inorder-traversal.gif
            :width: 400px

        :Сложность: O(n)
        :return: Итерационный объект, состоящий из узлов бинарного дерева по порядку.
        """
        if self.left:
            yield from self.left.subtree_iter()
        yield self
        if self.right:
            yield from self.right.subtree_iter()

    def inorder_traversal(self):
        """
        Рекурсивный обход дерева `по порядку` (in-order traversal), также `центрированный`.
        Является одним из трёх обходов в глубину (**DFS** - `Depth First Search`).

        Смотри также:

        * :class:`~BinaryTreeNode.preorder_traversal`
        * :class:`~BinaryTreeNode.postorder_traversal`

        Обход дерева по умолчанию (:class:`~BinaryTreeNode.subtree_iter`.).

        Алгоритм обхода по порядку:
            #. Обойти левое *поддерево* (рекурсивно).
            #. *Выбросить* (оператор yield) *корень*.
            #. Обойти правое *поддерево* (рекурсивно).

        .. image:: images/inorder-traversal.gif
            :width: 400px

        :Сложность: O(n)
        :return: Итерационный объект, состоящий из узлов бинарного дерева по порядку.
        """
        return self.subtree_iter()

    def preorder_traversal(self):
        """
        Рекурсивный обход дерева `по порядку` (preorder traversal), также `прямой`.
        Является одним из трёх обходов в глубину (**DFS** - `Depth First Search`).

        Смотри также:

        * :class:`~BinaryTreeNode.inorder_traversal`
        * :class:`~BinaryTreeNode.postorder_traversal`

        Алгоритм прямого обхода:
            #. *Выбросить* (оператор yield) *корень*.
            #. Обойти левое *поддерево* (рекурсивно).
            #. Обойти правое *поддерево* (рекурсивно).

        .. image:: images/preorder-traversal.gif
            :width: 400px

        :Сложность: O(n)
        :return: Итерационный объект, состоящий из узлов бинарного дерева.
        """
        yield self
        if self.left:
            yield from self.left.preorder_traversal()
        if self.right:
            yield from self.right.preorder_traversal()

    def postorder_traversal(self):
        """
        Рекурсивный обход дерева `по порядку` (postorder traversal), также `обратный`.
        Является одним из трёх обходов в глубину (**DFS** - `Depth First Search`).

        Смотри также:

        * :class:`~BinaryTreeNode.preorder_traversal`
        * :class:`~BinaryTreeNode.inorder_traversal`

        Алгоритм обратного обхода:
            #. Обойти левое *поддерево* (рекурсивно).
            #. Обойти правое *поддерево* (рекурсивно).
            #. *Выбросить* (оператор yield) *корень*.

        .. image:: images/postorder-traversal.gif
            :width: 400px

        :Сложность: O(n)
        :return: Итерационный объект, состоящий из узлов бинарного дерева.
        """
        if self.left:
            yield from self.left.postorder_traversal()
        if self.right:
            yield from self.right.postorder_traversal()
        yield self

    def level_order_traversal(self):
        """
        Обход в ширину (**BFS** - `Breadth First Search`).

        Алгоритм обхода в ширину:
            #. *Выбросить* (оператор yield) *корень*.
            #. Обойти следующий слой

        .. image:: images/level-order-traversal.gif
            :width: 400px

        :Сложность: O(n)
        :return: Итерационный объект, состоящий из узлов бинарного дерева.
        """

        queue = Queue()
        queue.enqueue(self)
        visited = set()

        while queue:
            node = queue.dequeue()
            visited.add(node)

            yield node

            if node.left and node.left not in visited:
                queue.enqueue(node.left)
            if node.right and node.right not in visited:
                queue.enqueue(node.right)

    def subtree_first(self):
        """
        Получить первый по порядку узел дерева (самый левый).

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :return: Первый узел дерева
        """
        if self.left:
            return self.left.subtree_first()
        return self

    def subtree_last(self):
        """
        Получить последний по порядку узел дерева (самый правый).

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :return: Последний узел дерева
        """
        if self.right:
            return self.right.subtree_last()
        return self

    def successor(self):
        """
        Найти преемника этого узла (узел, который идёт следующий по порядку).

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :return: Преемник этого узла
        """
        if self.right:
            return self.right.subtree_first()

        while self.parent and (self is self.parent.right):
            self = self.parent

        return self

    def predecessor(self):
        """
        Найти предшественника этого узла (узел, который идёт предыдущий по порядку).

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :return: Предшественник этого узла
        """
        if self.left:
            return self.left.subtree_last()
        while self.parent and (self is self.parent.left):
            self = self.parent

        return self

    def subtree_insert_before(self, node: Node):
        """
        Вставить узел (node) перед текущим по порядку.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param node: Узел, который мы хотим вставить перед текущим
        """
        if self.left:
            self = self.left.subtree_last()
            self.right, node.parent = node, self
        else:
            self.left = node
            node.parent = self

        self.maintain()

    def subtree_insert_after(self, node: Node):
        """
        Вставить узел (node) после текущего по порядку.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param node: Узел, который мы хотим вставить после текущего
        """
        if self.right:
            self = self.right.subtree_first()
            self.left, node.parent = node, self
        else:
            self.right, node.parent = node, self

        self.maintain()

    def subtree_delete(self) -> Node:
        """
        Рекурсивная функция удаления узла дерева.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :return: Удаляемый узел
        """
        if self.right or self.left:
            if self.left:
                node = self.predecessor()
            else:
                node = self.successor()
            node.data, self.data = self.data, node.data
            return node.subtree_delete()
        if self.parent:
            if self.parent.left is self:
                self.parent.left = None
            else:
                self.parent.right = None
            self.parent.maintain()
            self.parent = None

        return self


class BalancingNode(BinaryNode):
    """
    Узел балансирующего узла.
    """
    def __init__(self, item):
        super().__init__(item)
        self.height = None
        self.subtree_update()

    def subtree_rotate_left(self):
        """
        Функция поворота дерева налево нужна для поддержки баланса дерева.
        Она уменьшает скос дерева, не меняя при этом порядок узлов при обходе дерева по порядку.
        Функция вызывается относительно корня поддерева, которое надо повернуть.
        Функция вызывается при каждом обновлении дерева,
        см. :class:`~BinaryTreeNode.maintain`.

        **Алгоритм:**

        1. Обозначить временные переменные для хранения узлов: \
        *root_left_subtree*, *pivot_left_subtree*, *pivot_right_subtree*
        2. Поменять местами корень (*root*) и опорную точку (*pivot*). Теперь *pivot* - корень
        3. Сделать левым ребенком *pivot*'a корень (*root*), а правым -- *pivot_right_subtree*
        4. Сделать левым ребёнком *root*'a *root_left_subtree*, а правым -- *pivot_left_subtree*
        5. Не забыть поставить указатели на своих родителей для \
        *pivot_right_subtree* и *root_left_subtree*
        6. Обновить дерево относительно *pivot*'a и *root*'a

        .. image:: images/left_rotation.gif
            :width: 400px

        :Сложность: O(1)
        """
        assert self.right
        root_left_subtree, pivot = self.left, self.right
        pivot_left_subtree, pivot_right_subtree = pivot.left, pivot.right
        self, pivot = pivot, self
        self.data, pivot.data = pivot.data, self.data
        pivot.left, pivot.right = self, pivot_right_subtree
        self.left, self.right = root_left_subtree, pivot_left_subtree
        if root_left_subtree:
            root_left_subtree.parent = self
        if pivot_right_subtree:
            pivot_right_subtree.parent = pivot
        self.subtree_update()
        pivot.subtree_update()

    def subtree_rotate_right(self):
        """
        Функция поворота дерева направо нужна для поддержки баланса дерева.
        Она уменьшает скос дерева, не меняя при этом порядок узлов при
        обходе дерева по порядку. Функция вызывается относительно корня поддерева,
        которое надо повернуть. Функция вызывается при каждом обновлении дерева,
        см. :class:`~BinaryTreeNode.maintain`.

        **Алгоритм:**

        1. Обозначить временные переменные для хранения узлов: \
        *root_right_subtree*, *pivot_left_subtree*, *pivot_right_subtree*
        2. Поменять местами корень (*root*) и опорную точку (*pivot*). Теперь *pivot* - корень
        3. Сделать правым ребенком *pivot*'a корень (*root*), а левым -- *pivot_left_subtree*
        4. Сделать правым ребёнком *root*'a *root_right_subtree*, а левым -- *pivot_right_subtree*
        5. Не забыть поставить указатели на своих родителей для \
        *pivot_left_subtree* и *root_right_subtree*
        6. Обновить дерево относительно *pivot*'a и *root*'a

        .. image:: images/right_rotation.gif
            :width: 400px

        :Сложность: O(1)
        """
        assert self.left
        pivot, root_right_subtree = self.left, self.right
        pivot_left_subtree, pivot_right_subtree = pivot.left, pivot.right
        self, pivot = pivot, self
        self.data, pivot.data = pivot.data, self.data
        pivot.left, pivot.right = pivot_left_subtree, self
        self.left, self.right = pivot_right_subtree, root_right_subtree
        if pivot_left_subtree:
            pivot_left_subtree.parent = pivot
        if root_right_subtree:
            root_right_subtree.parent = self

        pivot.subtree_update()
        self.subtree_update()

    def subtree_update(self):
        """
        Обновляет высоту узла. *Высота самого высокого ребёнка + 1*.

        :Сложность: O(1)
        """
        self.height = 1 + max(height(self.left), height(self.right))

    def skew(self):
        """
        Найти *скос* дерева. *Скос* - это разница между высотами поддеревьев
        (*в данном случае высота правого минус высота левого*).
        Если эта разница больше нуля, то дерево накренено **вправо**.
        Если эта разница меньше нуля, то дерево накренено **влево**.
        Если эта разница равна нулю, то дерево **полное** (не накренено).

        :Сложность: O(1)
        :return: разница высот.
        """
        return height(self.right) - height(self.left)


    def maintain(self):
        """
        Функция вызывается после удаления или вставки узла (*уже прописано в коде*).
        Она поддерживает дерево сбалансированным за счёт :class:`~BalancingNode.rebalance`
        Также оно проходиться вверх по дереву с той же целью.

        :Сложность: O(log n)
        """
        self.rebalance()
        self.subtree_update()
        if self.parent:
            self.parent.maintain()

    def rebalance(self):
        """
        Сбалансировать дерево, если оно слишком накренено:

        * Если накренено вправо, повернуть налево
            * Перед этим сбалансировать правое поддерево (*повернуть направо*) при необходимости
        * Если накренено влево, повернуть направо
            * Перед этим сбалансировать левое поддерево (*повернуть налево*) при необходимости

        :Сложность: O(1)
        """
        if self.skew() == 2:
            if self.right.skew() < 0:
                self.right.subtree_rotate_right()
            self.subtree_rotate_left()

        elif self.skew() == -2:
            if self.left.skew() > 0:
                self.left.subtree_rotate_left()
            self.subtree_rotate_right()


class SearchNode(BinaryNode):
    """
    Узел бинарного дерева поиска.
    """
    def subtree_find(self, item: int):
        """
        Найти узел.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param item: значение искомого узла
        :return: искомый узел
        """
        if item < self.data:
            if self.left is not None:
                return self.left.subtree_find(item)

        elif item > self.data:
            if self.right is not None:
                return self.right.subtree_find(item)

        else:
            return self

        return None

    def subtree_find_next(self, item: int):
        """
        Найти следующий узел.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param item: значение, после которого идет значение искомого узла
        :return: узел, значение которого идёт после входного значения
        """
        if self.data <= item:
            # идти вправо, чтобы увеличить значение узла
            if self.right:
                return self.right.subtree_find_next(item)
            return None

        # когда значение узла больше:
        # самый левый элемент поддерева (если он есть),
        # чтобы максимально приблизиться к искомому значению (убывание)
        if self.left:
            node = self.left.subtree_find_next(item)
            if node:
                return node

        # если нет узлов в левом поддереве, вернуть текущий узел
        return self

    def subtree_find_prev(self, item: int):
        """
        Найти предыдущий узел.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param item: значение, перед которым идет значение искомого узла
        :return: узел, значение которого идёт перед входным значением
        """
        if self.data >= item:
            if self.left:
                return self.left.subtree_find_prev(item)
            return None

        if self.right:
            node = self.right.subtree_find_prev(item)
            if node:
                return node

        return self

    def subtree_insert(self, new_node: Node):
        """
        Добавить новый узел и не нарушить порядок возрастания при обходе по порядку.

        .. image:: images/bst_insert.gif

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param new_node: новый узел, который мы добавляем
        """
        if new_node.data < self.data:
            if self.left:
                self.left.subtree_insert(new_node)
            else:
                self.subtree_insert_before(new_node)

        elif new_node.data > self.data:
            if self.right:
                self.right.subtree_insert(new_node)
            else:
                self.subtree_insert_after(new_node)

        else:
            # if new_node.data == self.data:
            self.data = new_node.data
            return

        new_node.maintain()


class RedBlackNode(SearchNode):
    """
    Узел красно-чёрного дерева.
    """
    RED = True
    BLACK = False

    def __init__(self, item: int, color=RED):
        super().__init__(item)
        self.color = color

    @property
    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    @property
    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    @property
    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling


class SegmentNode(BalancingNode):
    """
    Индексируемый узел имеет параметр размера. Размер -- это сумма размеров детей + 1.
    Это нужно для индексации узлов.
    """
    def __init__(self, item):
        super().__init__(item)
        self.size = 1


    def subtree_update(self):
        """
        Обновляет размер узла (*это сумма размеров детей + 1*).

        :Сложность: O(1)
        """
        self.size = 1
        if self.left:
            self.size += self.left.size

        if self.right:
            self.size += self.right.size

        super().subtree_update()

    def subtree_at(self, i):
        """
        Найти i-ый узел. Поиск происходит через размеры узлов:

        * Если размер левого ребёнка больше индекса, найти i-ый узел в левом поддереве.
        * Если размер левого ребёнка меньше индекса, найти узел в правом поддереве с индексом: \
        *индекс - размер левого ребёнка - 1*.
        * Если размер левого ребенка равен индексу, вернуть текущий узел.

        :Сложность: O(log n)
        :param i: индекс искомого узла
        :return: искомый узел
        """
        assert i >= 0
        if self.left:
            left_size = self.left.size
        else:
            left_size = 0

        if i < left_size:
            return self.left.subtree_at(i)
        if i > left_size:
            return self.right.subtree_at(i - left_size - 1)

        return self


class AVLNode(BalancingNode, SearchNode):
    """
    Узел дерева AVL. AVL-дерево — это сбалансированное бинарное дерево поиска,
    в котором для каждого узла высота его левого и правого поддерева может отличаться
    не более чем на 1.

    Наследует функциональность как от BSTNode (для операций поиска и вставки),
    так и от BalancingNode (для поддержания баланса дерева).
    """


class TrieNode:
    """
    Узел в структуре данных Trie.
    """

    def __init__(self):
        """
        Инициализирует узел TrieNode пустым словарём дочерних узлов и флагом is_word,
        установленным в False.
        """
        self.children = {}
        self.is_word = False

    def __repr__(self):
        return str(self.children)

    def __contains__(self, char):
        """
        Проверяет, есть ли у узла TrieNode дочерний узел с указанным символом.

        :param char: Символ для проверки.
        :return: True, если у узла TrieNode есть дочерний узел с указанным символом, иначе False.
        """
        return char in self.children

    def __setitem__(self, key, value):
        """
        Устанавливает дочерний узел для узла TrieNode с указанным символом и значением.

        :param key: Символ для установки в качестве дочернего узла.
        :param value: Узел TrieNode для установки в качестве дочернего узла.
        """
        self.children[key] = value

    def __getitem__(self, key):
        """
        Получает дочерний узел узла TrieNode с указанным символом.

        :param key: Символ для получения дочернего узла.
        :return: Узел TrieNode-дочерний с указанным символом.
        """
        return self.children[key]

    def get_words(self, prefix=""):
        """
        Генерирует все слова в поддереве, корнем которого является этот узел TrieNode
        с указанным префиксом.

        :param prefix: Префикс для добавления к словам.
        :return: Генератор, выдающий слова с указанным префиксом.
        """
        if self.is_word:
            yield prefix
        for char, node in self.children.items():
            yield from node.get_words(prefix + char)


class TwoThreeTreeNode:
    """
    Узел 2-3 дерева.
    """
    def __init__(self, keys=None, children=None):
        self.keys = keys if keys else []
        self.children = children if children else []

    def __repr__(self):
        return f"Node({self.keys}})"

    def is_leaf(self):
        return len(self.children) == 0

    def is_full(self):
        return len(self.keys) == 3
