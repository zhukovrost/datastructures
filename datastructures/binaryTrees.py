from math import floor
from . import Queue


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
            yield from self.left.preorder_traversal()
        if self.right:
            yield from self.right.preorder_traversal()
        yield self

    def level_order_traversal(self):
        """
        Обход в ширину (**BFS** - `Breadth First Search`).

        Алгоритм обхода в ширину:
            #. *Выбросить* (оператор yield) *корень*.
            #. Обойти следующий слой

        .. image:: images/levelorder-traversal.gif
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

    def subtree_rotate_left(root):
        """
        Функция поворота дерева налево нужна для поддержки баланса дерева. Она уменьшает скос дерева, не меняя при этом
        порядок узлов при обходе дерева по порядку. Функция вызывается относительно корня поддерева,
        которое надо повернуть. Функция вызывается при каждом обновлении дерева, см. :class:`~BinaryTreeNode.maintain`.

        **Алгоритм:**

        1. Обозначить временные переменные для хранения узлов: *root_left_subtree*, *pivot_left_subtree*, *pivot_right_subtree*
        2. Поменять местами корень (*root*) и опорную точку (*pivot*). Теперь *pivot* - корень
        3. Сделать левым ребенком *pivot*'a корень (*root*), а правым -- *pivot_right_subtree*
        4. Сделать левым ребёнком *root*'a *root_left_subtree*, а правым -- *pivot_left_subtree*
        5. Не забыть поставить указатели на своих родителей для *pivot_right_subtree* и *root_left_subtree*
        6. Обновить дерево относительно *pivot*'a и *root*'a

        .. image:: images/left_rotation.gif
            :width: 400px

        :Сложность: O(1)
        """
        assert root.right
        root_left_subtree, pivot = root.left, root.right
        pivot_left_subtree, pivot_right_subtree = pivot.left, pivot.right
        root, pivot = pivot, root
        root.data, pivot.data = pivot.data, root.data
        pivot.left, pivot.right = root, pivot_right_subtree
        root.left, root.right = root_left_subtree, pivot_left_subtree
        if root_left_subtree:
            root_left_subtree.parent = root
        if pivot_right_subtree:
            pivot_right_subtree.parent = pivot
        root.subtree_update()
        pivot.subtree_update()

    def subtree_rotate_right(root):
        """
        Функция поворота дерева направо нужна для поддержки баланса дерева. Она уменьшает скос дерева, не меняя при этом
        порядок узлов при обходе дерева по порядку. Функция вызывается относительно корня поддерева,
        которое надо повернуть. Функция вызывается при каждом обновлении дерева, см. :class:`~BinaryTreeNode.maintain`.

        **Алгоритм:**

        1. Обозначить временные переменные для хранения узлов: *root_right_subtree*, *pivot_left_subtree*, *pivot_right_subtree*
        2. Поменять местами корень (*root*) и опорную точку (*pivot*). Теперь *pivot* - корень
        3. Сделать правым ребенком *pivot*'a корень (*root*), а левым -- *pivot_left_subtree*
        4. Сделать правым ребёнком *root*'a *root_right_subtree*, а левым -- *pivot_right_subtree*
        5. Не забыть поставить указатели на своих родителей для *pivot_left_subtree* и *root_right_subtree*
        6. Обновить дерево относительно *pivot*'a и *root*'a

        .. image:: images/right_rotation.gif
            :width: 400px

        :Сложность: O(1)
        """
        assert root.left
        pivot, root_right_subtree = root.left, root.right
        pivot_left_subtree, pivot_right_subtree = pivot.left, pivot.right
        root, pivot = pivot, root
        root.data, pivot.data = pivot.data, root.data
        pivot.left, pivot.right = pivot_left_subtree, root
        root.left, root.right = pivot_right_subtree, root_right_subtree
        if pivot_left_subtree:
            pivot_left_subtree.parent = pivot
        if root_right_subtree:
            root_right_subtree.parent = root

        pivot.subtree_update()
        root.subtree_update()

    def subtree_insert_before(self, node: "TreeNodeType"):
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

    def subtree_insert_after(self, node: "TreeNodeType"):
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
    Бинарное дерево AVL. Дерево называется бинарным, потому что у каждого узла не может быть более чем 2 ребёнка.
    AVL значит, что дерево автоматически *балансируется* (читай далее), что позволяет сократить сложность выполнения
    большинства алгоритмов с O(n) или O(h) до **O(log n)**!

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

    **В этих таблицах вы можете видеть преимущество AVL деревьев:**
    ---------------------------------------------------------------

    .. image:: images/BST_complexity.png

    .. image:: images/SQT_complexity.png

    **Эти типы деревьев я вынес в отдельные классы**
    """
    def __init__(self, TreeNodeType=BinaryTreeNode):
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

    def subtree_insert(self, new_node: "TreeNodeType"):
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

        .. image:: images/BST_complexity.png
        """
        super().__init__(BSTNode)

    def build(self, arr: list):
        """
        Строит дерево бинарного поиска из входящего списка.

        :Сложность: O(nlog n)
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


class SQTNode(BinaryTreeNode):
    """
    Индексируемый узел имеет параметр размера. Размер -- это сумма размеров детей + 1.
    Это нужно для индексации узлов.
    """
    def __init__(self, item):
        super().__init__(item)
        self.size = 0

    def subtree_update(self):
        """
        Обновляет высоту узла (*высота самого высокого ребёнка + 1*)
        и размер (*это сумма размеров детей + 1*).

        :Сложность: O(1)
        """
        super().subtree_update()
        self.size = 1
        if self.left:
            self.size += self.left.size

        if self.right:
            self.size += self.right.size

    def subtree_at(self, i):
        """
        Найти i-ый узел. Поиск происходит через размеры узлов:
        
        * Если размер левого ребёнка больше индекса, найти i-ый узел в левом поддереве.
        * Если размер левого ребёнка меньше индекса, найти узел в правом поддереве с индексом: *индекс - размер левого ребёнка - 1*.
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
        elif i > left_size:
            return self.right.subtree_at(i - left_size - 1)
        else:
            return self


class SQT(BinaryTree):
    """
    Бинарное дерево, к элементам которого можно обращаться по индексу (*Sequence Binary Tree*).
    **Индексация идет по порядку обхода дерева**.

    .. image:: images/SQT_complexity.png
    """
    def __init__(self):
        super().__init__(SQTNode)

    def build(self, iterable: list):
        """
        Построить дерево из входящего списка. Но алгоритм не просто поочерёдно вставлять элементы,
        а корнем каждого поддерева является центр среза входящего списка, что способствует балансу дерева.

        :Сложность: O(n)
        :param iterable: входящий список
        """
        def build_subtree(_iterable: list, _from: int, _to: int):
            center = (_from + _to) // 2
            root = self.TreeNodeType(_iterable[center])
            if _from < center:
                root.left = build_subtree(_iterable, _from, center - 1)
                root.left.parent = root
            if _to > center:
                root.right = build_subtree(_iterable, center + 1, _to)
                root.right.parent = root
            root.subtree_update()
            return root

        self.root = build_subtree(iterable, 0, len(iterable) - 1)
        self.size = self.root.size

    def get_at(self, i):
        """
        Получить i-ый узел.

        :Сложность: O(log n)
        :param i: индекс узла
        :return: значение искомого узла
        """
        assert self.root
        return self.root.subtree_at(i).data

    def __getitem__(self, i):
        return self.get_at(i)

    def set_at(self, i, data):
        """
        Установить значение i-го узла.

        :Сложность: O(log n)
        :param i: индекс узла
        :param data: новое значение узла
        """
        assert self.root
        self.root.subtree_at(i).data = data

    def __setitem__(self, key, value):
        self.set_at(key, value)

    def insert_at(self, i, data):
        """
        Вставить новый узел на i-ую позицию.

        :Сложность: O(log n)
        :param i: индекс нового узла
        :param data: значение нового узла
        """
        new_node = self.TreeNodeType(data)
        if i == 0:
            if self.root:
                node = self.root.subtree_first()
                node.subtree_insert_before(new_node)
            else:
                self.root = new_node
        else:
            node = self.root.subtree_at(i - 1)
            node.subtree_insert_after(new_node)
        self.size += 1

    def delete_at(self, i):
        """
        Удаляет i-ый элемент.

        :Сложность: O(log n)
        :param i: индекс удаляемого узла
        :return: значение удаляемого узла
        """
        assert self.root
        node = self.root.subtree_at(i)
        temp = node.subtree_delete()
        if temp.parent is None:
            self.root = None
        self.size -= 1
        return temp.data

    def delete_first(self):
        """
        Удаляет первый узел.

        :Сложность: O(log n)
        :return: значение удаляемого узла
        """
        return self.delete_at(0)

    def delete_last(self):
        """
        Удаляет последний узел.

        :Сложность: O(log n)
        :return: значение удаляемого узла
        """
        return self.delete_at(len(self) - 1)

    def insert_first(self, data):
        """
        Вставляет новый узел в начало дерева (0 позиция).

        :Сложность: O(log n)
        :param data: значение нового узла
        """
        self.insert_at(0, data)

    def insert_last(self, data):
        """
        Вставляет новый узел в конец дерева (len(self) позиция).

        :Сложность: O(log n)
        :param data: значение нового узла
        """
        self.insert_at(len(self), data)


# ==================== HEAP ====================

def heap_sort(arr: list, **kwargs):
    """
    Сортирует входной список с использованием алгоритма сортировки кучей (heap sort).

    :Сложность: O(N log N)
    :param arr: Список, который требуется отсортировать.
    :param kwargs: Дополнительные параметры для настройки поведения сортировки.
                   Возможные параметры:

                   - reverse (bool): Если установлено в True, возвращает список в обратном порядке.

    :return: Отсортированный список.
    """
    heap = MinHeap(arr)
    sorted_arr = []
    while len(heap) > 0:
        sorted_arr.append(heap.poll())

    if "reverse" in kwargs:
        if kwargs["reverse"]:
            return sorted_arr[::-1]

    return sorted_arr


class MinHeap:
    """
    Куча минимума - это бинарное дерево, где ключ каждого узла всегда меньше или равен ключам его детей.
    Эта структура данных позволяет эффективно вставлять, удалять и находить минимальный элемент в куче.

    .. image:: images/heap.png
    """

    def __init__(self, arr=None):
        """
        Инициализировать новую кучу минимума.

        :Сложность: O(N log N), где n - количество элементов в arr.
        :param arr: Необязательный итерируемый объект, содержащий начальные элементы кучи.
        """
        if arr is None:
            arr = []
        elif not isinstance(arr, list) and hasattr(arr, '__iter__'):
            arr = list(arr)

        self.heap = arr

        for i in range(len(self) // 2, -1, -1):
            self.heapify_down(i)

    def __len__(self):
        """
        Возвращает количество элементов в куче.

        :Сложность: O(1).
        :return: Количество элементов в куче.
        """
        return len(self.heap)

    def __iter__(self):
        """
        Перебирает элементы кучи в порядке их приоритета.

        :Сложность: O(1).
        :return: Итератор по элементам кучи.
        """
        return self.heap.__iter__()

    def get_item(self, index):
        """
        Возвращает элемент по указанному индексу.

        :Сложность: O(1).
        :param index: Индекс элемента для возврата.
        :return: Элемент по указанному индексу.
        """
        return self.heap[index]

    def __getitem__(self, item):
        return self.get_item(item)

    @staticmethod
    def get_left_child_index(index):
        """
        Возвращает индекс левого потомка указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Индекс левого потомка узла.
        """
        return 2 * index + 1

    @staticmethod
    def get_right_child_index(index):
        """
        Возвращает индекс правого потомка указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Индекс правого потомка узла.
        """
        return 2 * index + 2

    @staticmethod
    def get_parent_index(index):
        """
        Возвращает индекс родителя указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Индекс родителя узла.
        """
        return floor((index - 1) / 2)

    def count(self, item):
        """
        Возвращает количество вхождений указанного элемента в кучу.

        :Сложность: O(n), где n - количество элементов в куче.
        :param item: Элемент для подсчета.
        :return: Количество вхождений элемента в кучу.
        """
        return self.heap.count(item)

    def has_left_child(self, index) -> bool:
        """
        Проверяет, есть ли у указанного узла левый потомок.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: True, если узел имеет левого потомка, иначе False.
        """
        return self.get_left_child_index(index) < len(self)

    def has_right_child(self, index) -> bool:
        """
        Проверяет, есть ли у указанного узла правый потомок.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: True, если узел имеет правого потомка, иначе False.
        """
        return self.get_right_child_index(index) < len(self)

    def has_parent(self, index) -> bool:
        """
        Проверяет, есть ли у указанного узла родитель.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: True, если узел имеет родителя, иначе False.
        """
        return self.get_parent_index(index) >= 0

    def left_child(self, index):
        """
        Возвращает левого потомка указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Левый потомок узла.
        """
        return self.heap[self.get_left_child_index(index)]

    def right_child(self, index):
        """
        Возвращает правого потомка указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Правый потомок узла.
        """
        return self.heap[self.get_right_child_index(index)]

    def parent(self, index):
        """
        Возвращает родителя указанного узла.

        :Сложность: O(1).
        :param index: Индекс узла.
        :return: Родитель узла.
        """
        return self.heap[self.get_parent_index(index)]

    def swap(self, i1, i2):
        """
        Обменивает элементы с указанными индексами.

        :Сложность: O(1).
        :param i1: Индекс первого элемента.
        :param i2: Индекс второго элемента.
        """
        self.heap[i1], self.heap[i2] = self.heap[i2], self.heap[i1]

    def peek(self):
        """
        Возвращает минимальный элемент в куче без его удаления.

        :Сложность: O(1).
        :return: Минимальный элемент в куче.
        """
        if len(self) == 0:
            raise IndexError
        return self.heap[0]

    def poll(self, index=None):
        """
        Удаляет и возвращает минимальный элемент из кучи.

        :Сложность: O(log n), где n - количество элементов в куче.
        :param index: Индекс элемента для удаления. Если не указан, удаляется минимальный элемент.
        :return: Минимальный элемент в куче.
        """
        if len(self) == 0:
            raise IndexError

        if index is None:
            index = 0

        item = self.heap[index]
        self.heap[index] = self.heap[len(self) - 1]
        self.heap.pop()
        self.heapify_down(index)
        return item

    def add(self, item):
        """
        Добавляет элемент в кучу.

        :Сложность: O(log n), где n - количество элементов в куче.
        :param item: Элемент для добавления.
        """
        self.heap.append(item)
        self.heapify_up()

    def heapify_down(self, index=None):
        """
        Перестраивает элементы в куче вниз от указанного узла.

        :Сложность: O(log n), где n - количество элементов в куче.
        :param index: Индекс узла для начала. Если не указан, используется корень кучи.
        """
        if len(self) <= 1:
            return

        if index is None:
            index = 0

        while self.has_left_child(index):
            min_child_index = self.get_left_child_index(index)

            if self.has_right_child(index) and self.right_child(index) < self.left_child(index):
                min_child_index = self.get_right_child_index(index)

            if self[min_child_index] > self[index]:
                break

            self.swap(index, min_child_index)
            index = min_child_index

    def heapify_up(self, index=None):
        """
        Перестраивает элементы в куче вверх от указанного узла.

        :Сложность: O(log n), где n - количество элементов в куче.
        :param index: Индекс узла для начала. Если не указан, используется последний элемент кучи.
        """
        if len(self) <= 1:
            return

        if index is None:
            index = len(self) - 1

        while self.has_parent(index) and self.parent(index) > self.heap[index]:
            p_i = self.get_parent_index(index)
            self.swap(index, p_i)
            index = p_i
