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
    else:
        return -1


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
        self.height = None
        self.subtree_update()

    def subtree_update(self):
        """
        Обновляет высоту узла. *Высота самого высокого ребёнка + 1*.

        :Сложность: O(1)
        """
        self.height = 1 + max(height(self.left), height(self.right))

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

    def maintain(self):
        """
        Функция вызывается после удаления или вставки узла (*уже прописано в коде*).
        Она поддерживает дерево сбалансированным за счёт :class:`~BinaryTreeNode.rebalance`
        и поддерживает корректность высот у узлов за счёт :class:`~BinaryTreeNode.subtree_update`.
        Также оно проходиться вверх по дереву с той же целью.

        :Сложность: O(log n)
        """
        self.rebalance()
        self.subtree_update()
        if self.parent:
            self.parent.maintain()

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

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :return: Первый узел дерева
        """
        if self.left:
            return self.left.subtree_first()
        else:
            return self

    def subtree_last(self):
        """
        Получить последний по порядку узел дерева (самый правый).

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :return: Последний узел дерева
        """
        if self.right:
            return self.right.subtree_last()
        else:
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

    def skew(self):
        """
        Найти *скос* дерева. *Скос* - это разница между высотами поддеревьев
        (*в данном случае высота правого минус высота левого*). Если эта разница больше нуля, то дерево накренено
        **вправо**. Если эта разница меньше нуля, то дерево накренено **влево**. Если эта разница равна нулю,
        то дерево **полное** (не накренено).

        :Сложность: O(1)
        :return: разница высот.
        """
        return height(self.right) - height(self.left)

    def subtree_rotate_left(self):
        """
        Функция поворота дерева налево нужна для поддержки баланса дерева. Она уменьшает скос дерева,
        не меняя при этом порядок узлов при обходе дерева по порядку. **Алгоритм:**

        .. image:: images/left_rotation.gif
            :width: 400px

        :Сложность: O(1)
        """
        assert self.right
        left, right = self.left, self.right
        right_left, right_right = right.left, right.right
        self, right = right, self
        self.data, right.data = right.data, self.data
        right.left, right.right = self, right_right
        self.left, self.right = left, right_left
        if left:
            left.parent = self
        if right_right:
            right_right.parent = right
        self.subtree_update()
        right.subtree_update()

    def subtree_rotate_right(self):
        """
        Функция поворота дерева направо нужна для поддержки баланса дерева. Она уменьшает скос дерева,
        не меняя при этом порядок узлов при обходе дерева по порядку. **Алгоритм:**

        .. image:: images/right_rotation.gif
            :width: 400px

        :Сложность: O(1)
        """
        assert self.left
        left, right = self.left, self.right
        left_left, left_right = left.left, left.right
        self, left = left, self
        self.data, left.data = left.data, self.data
        left.left, left.left = left_left, self
        self.left, self.right = left_right, right
        if left_left:
            left_left.parent = left
        if right:
            right.parent = self

        left.subtree_update()
        self.subtree_rotate_left()

    def subtree_insert_before(self, node: "BinaryTreeNode"):
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

    def subtree_insert_after(self, node: "BinaryTreeNode"):
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

    def subtree_delete(self):
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
        else:
            if self.parent.left is self:
                self.parent.left = None
            else:
                self.parent.right = None
            self.parent.maintain()

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
        * Предшественник - тот, кто идёт раньше определённого узла по порядку обхода в глубину in order :class:`~BinaryTreeNode.subtree_iter`
        * Преемник - тот, кто идёт позже определённого узла по порядку обхода в глубину in order :class:`~BinaryTreeNode.subtree_iter`
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

        :param TreeNodeType: Тип узлов дерева. По умолчанию :class:`~BinaryTreeNode`
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
    def subtree_find(self, item: int) -> "BSTNode":
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
            else:
                return None
        else:
            if self.right:
                node = self.right.subtree_find_prev(item)
                if node:
                    return node
        return self

    def subtree_insert(self, new_node: "BSTNode"):
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


class BST(BinaryTree):
    def __init__(self):
        """
        Инициализатор дерева с типом узлов :class:`~BSTNode`.
        Это то же самое бинарное дерево, но значения узлов будут возрастать в порядке обхода.
        Повторяющиеся элементы пропадают. По другому это дерево можно назвать бинарное дерево-множество или
        дерево бинарного поиска.

        .. image:: /images/bst.png
            :width: 500px

        Если обойти это дерево по порядку (:class:`~BinaryTreeNode.subtree_iter`),
        то на выходе мы получим узлы в порядке возрастания:
        **2 4 6 8 9 10 11 12 14 16 18**
        """
        super().__init__(BSTNode)

    def build(self, arr: list):
        """
        Строит дерево бинарного поиска из входящего списка.

        :Сложность: O(n)
        :param arr: входящий список значений узлов
        """
        for item in arr:
            self.insert(item)

    def find_min(self):
        """
        Минимальный элемент - первый, поэтому вызываем :class:`~BSTNode.subtree_first`

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :return: значение минимального узла
        """
        if self.root:
            return self.root.subtree_first().data

    def find_max(self):
        """
        Максимальный элемент - последний, поэтому вызываем :class:`~BSTNode.subtree_last`

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :return: значение максимального узла
        """
        if self.root:
            return self.root.subtree_last().data

    def find(self, item: int):
        """
        Найти элемент.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param item: искомое значение
        :return: значение искомого элемента, если элемент не найден возвращает None
        """
        if self.root:
            node = self.root.subtree_find(item)
            if node is not None:
                return node.data

    def find_next(self, item: int):
        """
        Найти элемент, идущий после данного.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param item: значение элемента, после которого идёт искомый
        :return: значение искомого элемента, если элемент не найден возвращает None
        """
        if self.root:
            node = self.root.subtree_find_next(item)
            if node is not None:
                return node.data

    def find_prev(self, item: int):
        """
        Найти элемент, идущий перед данным.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param item: значение элемента, перед которым идёт искомый
        :return: значение искомого элемента, если элемент не найден возвращает None
        """
        if self.root:
            node = self.root.subtree_find_prev(item)
            if node is not None:
                return node.data

    def insert(self, item: int) -> bool:
        """
        Вставить узел.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param item: значение нового узла
        :return: *True*, если узел был добавлен, иначе *False*
        """
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

    def delete(self, item: int):
        """
        Удалить узел.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param item: значение удаляемого узла
        :return: значение удаляемого узла
        """
        assert self.root
        node = self.root.subtree_find(item)
        assert node
        temp = node.subtree_delete()
        if temp.parent is None:
            self.root = None
        self.size -= 1
        return temp.data
