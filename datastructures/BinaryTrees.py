class BinaryTreeNode:

    def __init__(self, item):
        """
        Инициализатор.

        :param item: Значение узла
        """
        self.data = item
        self.parent = None
        self.right = None
        self.left = None

    def subtree_iter(self):
        """
        Рекурсивный обход дерева `по порядку` (in-order traversal).
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

    def subtree_first(self):
        """
        Получить первый по порядку узел дерева (самый левый).

        :Сложность: O(h), где h -- высота дерева
        :return: Первый узел дерева
        """
        if self.left:
            return self.left.subtree_first()
        else:
            return self

    def subtree_last(self):
        """
        Получить последний по порядку узел дерева (самый правый).

        :Сложность: O(h), где h -- высота дерева
        :return: Последний узел дерева
        """
        if self.right:
            return self.right.subtree_last()
        else:
            return self

    def successor(self):
        """
        Найти преемника этого узла (узел, который идёт следующий по порядку).

        :Сложность: O(h), где h -- высота дерева
        :return: Преемник этого узла
        """
        trav = self
        if trav.right:
            return trav.right.subtree_first()

        while trav.parent and (trav is trav.parent.right):
            trav = trav.parent

        return trav

    def predecessor(self):
        """
        Найти предшественника этого узла (узел, который идёт предыдущий по порядку).

        :Сложность: O(h), где h -- высота дерева
        :return: Предшественник этого узла
        """
        trav = self
        if trav.left:
            return trav.left.subtree_last()
        while trav.parent and (trav is trav.parent.left):
            trav = trav.parent

        return trav

    def subtree_insert_before(self, node):
        """
        Вставить узел (node) перед текущим по порядку.

        :Сложность: O(h), где h -- высота дерева
        :param node: Узел, который мы хотим вставить перед текущим
        """
        if self.left:
            trav = self.left.subtree_last()
            trav.right = node
            node.parent = trav
        else:
            self.left = node
            node.parent = self

    def subtree_insert_after(self, node):
        """
        Вставить узел (node) после текущего по порядку.

        :Сложность: O(h), где h -- высота дерева
        :param node: Узел, который мы хотим вставить после текущего
        """
        if self.right:
            trav = self.right.subtree_first()
            trav.left = node
            node.parent = trav
        else:
            self.right = node
            node.parent = self

    def subtree_delete(self):
        """
        Рекурсивная функция удаления узла дерева.

        :return: Удаляемый узел
        """
        if self.right or self.left:
            if self.left:
                node = self.predecessor()
            else:
                node = self.successor()
            node.data, self.data = self.data, node.data
            return node.subtree_delete()
        else:
            if self.parent.left is self:
                self.parent.left = None
            else:
                self.parent.right = None

        self.parent = None
        return self


class BinaryTree:
    """
    Бинарное дерево. Дерево называется бинарным, потому что у каждого узла не может быть более чем 2 ребёнка.

    .. image:: images/binary-tree.png
        :width: 500px

    Немного терминологии:
        * Узел - элемент дерева
        * Корень - самый верхний элемент, из которого идет всё дерево
        * Лист - узел без детей
        * Поддерево - дерево внутри другого дерева.
        * Ребёнок - один из узлов, выходящих из определённого
        * Родитель - узел, из которого выходит определённый
        * Грань - связь между ребёнком и родителем
        * Предшественник - тот, кто идёт раньше определённого узла по порядку обхода в глубину in order :class:`~datastructures.BinaryTrees.BinaryTreeNode.subtree_iter`
        * Преемник - тот, кто идёт позже определённого узла по порядку обхода в глубину in order :class:`~datastructures.BinaryTrees.BinaryTreeNode.subtree_iter`
    Типы деревьев:
        * Полное: у каждого узла либо 0, либо 2 ребёнка.
        * Дегенеративное: у каждого узла либо 0, либо 1 ребёнок
        * Перекошенное: дегенеративное дерево, у узлов которого есть либо **только** правый ребёнок или нет ребёнка, либо **только** левый ребёнок или нет ребёнка
        * Полное: все слои дереве, кроме, возможно, последнего, полностью заполнены
        * Идеальное: полное дерево, у которого все листья на одном уровне
        * Сбалансированное: дерево, у которого разница между высотой левого и правого поддерева меньше или равна 1

    **Специальные типы деревьев я вынес в отдельные классы**
    """
    def __init__(self, TreeNodeType = BinaryTreeNode):
        """
        Инициализатор.

        :param TreeNodeType: Тип узлов дерева. По умолчанию :class:`~datastructures.BinaryTrees.BinaryTreeNode`
        """
        self.root = None
        self.size = 0
        self.TreeNodeType = TreeNodeType

    def __len__(self):
        return self.size

    def __iter__(self):
        if self.root:
            for node in self.root.subtree_iter():
                yield node
