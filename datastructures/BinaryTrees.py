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

    def subtree_insert_before(self, node: "BinaryTreeNode"):
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

    def subtree_insert_after(self, node: "BinaryTreeNode"):
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


class BSTNode(BinaryTreeNode):
    def subtree_find(self, item):
        if item < self.data:
            if self.left is not None:
                return self.left.subtree_find(item)

        elif item > self.data:
            if self.right is not None:
                return self.right.subtree_find(item)

        else:
            return self

        return None

    def subtree_find_next(self, item):
        if self.data <= item:
            # идти вправо, чтобы увеличить значение узла
            if self.right:
                return self.right.subtree_find_next(item)
            else:
                return None
        else:
            # когда значение узла больше:
            # самый левый элемент поддерева (если он есть),
            # чтобы максимально приблизиться к искомому значению (убывание)
            if self.left:
                node = self.left.subtree_find_next(item)
                if node:
                    return node

        # если нет узлов в левом поддереве, вернуть текущий узел
        return self

    def subtree_find_prev(self, item):
        if self.data >= item:
            if self.left:
                return self.left.subtree_find_prev(item)
            else:
                return None
        else:
            if self.right:
                node = self.right.subtree_find_prev(item)
                if node:
                    return node
        return self

    def subtree_insert(self, new_node: "BSTNode"):
        if new_node.data < self.data:
            if self.left:
                self.left.subtree_insert(new_node)
            else:
                self.subtree_insert_before(new_node)

        elif new_node.data > self.data:
            if self.right:
                self.right.subtree_insert_before(new_node)
            else:
                self.subtree_insert_after(new_node)

        else:
            # if new_node.data == self.data:
            self.data = new_node.data


class SetBinaryTree(BinaryTree):
    def __init__(self):
        """
        Инициализатор дерева с типом узлов :class:`~datastructures.BinaryTree.BSTNode`
        """
        super().__init__(BSTNode)

    def build(self, arr: list):
        for item in arr:
            self.insert(item)

    def find_min(self):
        if self.root:
            return self.root.subtree_first().data

    def find_max(self):
        if self.root:
            return self.root.subtree_last().data

    def find(self, item):
        if self.root:
            node = self.root.subtree_find(item)
            if node is not None:
                return node.data

    def find_next(self, item):
        if self.root:
            node = self.root.subtree_find_next(item)
            if node is not None:
                return node.data

    def find_prev(self, item):
        if self.root:
            node = self.root.subtree_find_prev(item)
            if node is not None:
                return node.data

    def insert(self, item) -> bool:
        new_node = BSTNode(item)
        if self.root:
            self.root.subtree_insert(new_node)
            if new_node.parent is None:
                # if the value repeats
                return False
        else:
            self.root = new_node

        self.size += 1
        return True

    def delete(self, item):
        assert self.root
        node = self.root.subtree_find(item)
        assert node
        temp = node.subtree_delete()
        if temp.parent is None:
            self.root = None
        self.size -= 1
        return temp.data
