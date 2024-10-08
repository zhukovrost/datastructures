"""
Этот модуль содержит реализации различных бинарных и не только деревьев.
"""


from abc import ABC
from collections import defaultdict
from .nodes import BinaryNode, SearchNode, SegmentNode, \
    AVLNode, TrieNode, RedBlackNode, TwoThreeTreeNode, HuffmanNode
from ..heap import MinHeap


class _BinaryTree(ABC):
    def __init__(self, tree_node_type=BinaryNode):
        """
        Инициализатор.

        :param tree_node_type: Тип узлов дерева. По умолчанию :class:`~BinaryTreeNode`
        """
        self.root = None
        self.size = 0
        self.tree_node_type = tree_node_type

    def __len__(self):
        return self.size

    def __iter__(self):
        if self.root:
            for node in self.root.subtree_iter():
                yield node

    def __repr__(self):
        if self.root:
            return f"BinaryTree({[node.__repr__() for node in self.root.subtree_iter()]})"
        return "BinaryTree([])"


class SearchTree(_BinaryTree):
    """
    Это то же самое бинарное дерево, но значения узлов будут возрастать в порядке обхода.
    Повторяющиеся элементы пропадают. По другому это дерево можно назвать бинарное
    дерево-множество или дерево бинарного поиска.

    .. image:: /images/bst.png
        :width: 500px

    Если обойти это дерево по порядку (:class:`~BinaryTreeNode.subtree_iter`),
    то на выходе мы получим узлы в порядке возрастания:
    **2 4 6 8 9 10 11 12 14 16 18**

    .. image:: images/BST_complexity.png
    """

    def __init__(self, tree_node_type=SearchNode):
        """
        Инициализатор дерева с типом узлов :class:`~BSTNode`.
        """
        super().__init__(tree_node_type)

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
        return None

    def find_max(self):
        """
        Максимальный элемент - последний, поэтому вызываем :class:`~BSTNode.subtree_last`

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :return: значение максимального узла
        """
        if self.root:
            return self.root.subtree_last().data
        return None

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
        return None

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
        return None

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
        return None

    def _insert_fix(self, n):
        pass

    def insert(self, item: int) -> bool:
        """
        Вставить узел.

        :Сложность: O(log n), *(если дерево не сбалансировано - O(h))*
        :param item: значение нового узла
        :return: *True*, если узел был добавлен, иначе *False*
        """
        new_node = self.tree_node_type(item)
        if self.root:
            self.root.subtree_insert(new_node)
            if new_node.parent is None:
                # if the value repeats
                return False
        else:
            self.root = new_node

        self.size += 1
        self._insert_fix(new_node)
        return True

    def _delete_fix(self, x):
        pass

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
        self.size -= 1

        if self.size == 0:
            self.root = None

        self._delete_fix(node)

        return temp.data


class RedBlackTree(SearchTree):
    """
    Красно-черное дерево - это самобалансирующееся дерево бинарного поиска.
    Оно поддерживает балансировку за счет следующих правил:

    1. Каждый узел либо красный, либо черный.
    2. Корень всегда черный.
    3. Все листья (NULL узлы) черные.
    4. Оба ребенка каждого красного узла черные.
    5. Любой путь от узла до листьев имеет одинаковое количество черных узлов.

    .. image:: images/redblack.png

    """

    def __init__(self):
        """
        Инициализатор.
        """
        super().__init__(tree_node_type=RedBlackNode)

    def _insert_fix(self, node):
        while node.parent and node.parent.color is RedBlackNode.RED:
            if node.parent == node.grandparent.left:
                uncle = node.uncle
                if uncle and uncle.color is RedBlackNode.RED:
                    node.parent.color = RedBlackNode.BLACK
                    uncle.color = RedBlackNode.BLACK
                    node.grandparent.color = RedBlackNode.RED
                    node = node.grandparent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.color = RedBlackNode.BLACK
                    node.grandparent.color = RedBlackNode.RED
                    self._rotate_right(node.grandparent)
            else:
                uncle = node.uncle
                if uncle and uncle.color is RedBlackNode.RED:
                    node.parent.color = RedBlackNode.BLACK
                    uncle.color = RedBlackNode.BLACK
                    node.grandparent.color = RedBlackNode.RED
                    node = node.grandparent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = RedBlackNode.BLACK
                    node.grandparent.color = RedBlackNode.RED
                    self._rotate_left(node.grandparent)
        self.root.color = RedBlackNode.BLACK

    def _delete_fix(self, node):
        while node != self.root and node.color is RedBlackNode.BLACK:
            if node == node.parent.left:
                sibling = node.sibling
                if sibling.color is RedBlackNode.RED:
                    sibling.color = RedBlackNode.BLACK
                    node.parent.color = RedBlackNode.RED
                    self._rotate_left(node.parent)
                    sibling = node.sibling
                if (sibling.left is None or sibling.left.color is RedBlackNode.BLACK) \
                        and (sibling.right is None or sibling.right.color is RedBlackNode.BLACK):
                    sibling.color = RedBlackNode.RED
                    node = node.parent
                else:
                    if sibling.right is None or sibling.right.color is RedBlackNode.BLACK:
                        sibling.left.color = RedBlackNode.BLACK
                        sibling.color = RedBlackNode.RED
                        self._rotate_right(sibling)
                        sibling = node.sibling
                    sibling.color = node.parent.color
                    node.parent.color = RedBlackNode.BLACK
                    if sibling.right:
                        sibling.right.color = RedBlackNode.BLACK
                    self._rotate_left(node.parent)
                    node = self.root
            else:
                sibling = node.sibling
                if sibling.color is RedBlackNode.RED:
                    sibling.color = RedBlackNode.BLACK
                    node.parent.color = RedBlackNode.RED
                    self._rotate_right(node.parent)
                    sibling = node.sibling
                if (sibling.left is None or sibling.left.color is RedBlackNode.BLACK) and \
                        (sibling.right is None or sibling.right.color is RedBlackNode.BLACK):
                    sibling.color = RedBlackNode.RED
                    node = node.parent
                else:
                    if sibling.left is None or sibling.left.color is RedBlackNode.BLACK:
                        sibling.right.color = RedBlackNode.BLACK
                        sibling.color = RedBlackNode.RED
                        self._rotate_left(sibling)
                        sibling = node.sibling
                    sibling.color = node.parent.color
                    node.parent.color = RedBlackNode.BLACK
                    if sibling.left:
                        sibling.left.color = RedBlackNode.BLACK
                    self._rotate_right(node.parent)
                    node = self.root
        node.color = RedBlackNode.BLACK

    def _rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def _rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child


class SegmentTree(_BinaryTree):
    """
    Бинарное дерево, к элементам которого можно обращаться по индексу (*Sequence Binary Tree*).
    **Индексация идет по порядку обхода дерева**.
    """
    def __init__(self, tree_node_type=SegmentNode):
        super().__init__(tree_node_type)

    def build(self, iterable: list):
        """
        Построить дерево из входящего списка. Но алгоритм не просто поочерёдно вставлять элементы,
        а корнем каждого поддерева является центр среза входящего списка, что способствует балансу
        дерева.

        :Сложность: O(n)
        :param iterable: входящий список
        """
        def build_subtree(_iterable: list, _from: int, _to: int):
            center = (_from + _to) // 2
            root = self.tree_node_type(_iterable[center])
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
        new_node = self.tree_node_type(data)
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
        if temp is self.root and temp.left is None and temp.right is None:
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


class AVLTree(SearchTree):
    """
    AVL дерево - бинарное балансирующее дерево поиска.
    Балансировка осуществляется засчёт поворотов дерева.
    """
    def __init__(self, tree_node_type=AVLNode):
        super().__init__(tree_node_type)


class Trie:
    """
    Trie (также известно как префиксное дерево) - это древовидная структура данных,
    которая хранит динамический набор или ассоциативный массив.
    Ключ обычно является строкой, а связанное значение часто является None.
    """

    def __init__(self):
        """
        Инициализирует пустое дерево Trie.
        """
        self.root = TrieNode()

    def insert(self, *words):
        """
        Вставляет слова (строки) в дерево Trie.

        :param words: Переменная длина аргумента списка слов для вставки.
        :raises TypeError: Если слово не является строкой.
        """
        for word in words:
            if not isinstance(word, str):
                raise TypeError("Метод Trie.insert() принимает только строки")
            node = self.root
            for char in word.lower():
                if char not in node:
                    node[char] = TrieNode()
                node = node[char]
            node.is_word = True

    def search(self, word):
        """
        Ищет слово в дереве Trie.

        :param word: Слово для поиска.
        :return: True, если слово найдено, иначе False.
        :raises TypeError: Если слово не является строкой.
        """
        if not isinstance(word, str):
            raise TypeError("Метод Trie.search() принимает только строки")
        node = self.root
        for char in word:
            if char not in node:
                return False
            node = node[char]
        return node.is_word

    def __contains__(self, word):
        """
        Проверяет, содержится ли слово в дереве Trie.

        :param word: Слово для проверки.
        :return: True, если слово есть в дереве Trie, иначе False.
        """
        return self.search(word)

    def __iter__(self):
        """
        Перебирает все слова в дереве Trie.

        :return: Итератор по всем словам в дереве Trie.
        """
        return self.root.get_words()

    def get_words_with_prefix(self, prefix=""):
        """
        Получает все слова в дереве Trie с указанным префиксом.

        :param prefix: Префикс для проверки.
        :return: Список слов с указанным префиксом.
        :raises TypeError: Если префикс не является строкой.
        """
        if not isinstance(prefix, str):
            raise TypeError("Метод Trie.get_words() принимает только строки")
        node = self.root
        for char in prefix:
            if char not in node:
                return []
            node = node[char]
        return list(node.get_words(prefix))


class TwoThreeTree:
    """
    Дерево 2-3 - это B-дерево порядка 3.

    Свойства дерева 2-3:

     - Узлы с двумя дочерними элементами называются 2-узлами. 2-узлы имеют одно \
      значение данных и два дочерних узла.
     - Узлы с тремя детьми называются 3-узлами. \
     3-узлы имеют два значения данных и три дочерних узла.
     - Данные хранятся в отсортированном порядке.
     - Это сбалансированное дерево.
     - Все листовые узлы находятся на одном уровне.
     - Каждый узел может быть либо листом, либо 2-узловым, либо 3-узловым.
     - Вставка всегда выполняется в лист.

    .. image:: images/2-3.jpg

    """
    def __init__(self):
        """
        Инициализатор.
        """
        self.root = None

    def search(self, key, node=None) -> bool:
        """
        Поиск ключа в дереве.

        Выполняет рекурсивный поиск ключа в узлах дерева.
        Если ключ найден, возвращает True, иначе - False.

        :Сложность: O(logN)
        :param key: Ключ, который нужно найти.
        :param node: Узел, с которого начинается поиск (по умолчанию корневой узел).
        :return: True, если ключ найден, иначе False.
        """
        if node is None:
            node = self.root

        if node is None:
            return False

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return True
        if node.is_leaf():
            return False
        return self.search(key, node.children[i])

    def insert(self, key):
        """
        Вставка ключа в дерево 2-3.

        Если дерево пустое, создается новый корневой узел.
        Если в результате вставки происходит разделение узла,
        то корень обновляется.

        :Сложность: O(log n)
        :param key: Ключ, который нужно вставить.
        """
        if self.root is None:
            self.root = TwoThreeTreeNode([key])
        else:
            new_node, new_key = self._insert(self.root, key)
            if new_node:
                self.root = TwoThreeTreeNode([new_key], [self.root, new_node])

    def _insert(self, node, key):
        if node.is_leaf():
            return self._insert_into_leaf(node, key)
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        new_node, new_key = self._insert(node.children[i], key)
        if new_node:
            return self._insert_into_internal(node, new_key, new_node)
        return None, None

    def _insert_into_leaf(self, node, key):
        node.keys.append(key)
        node.keys.sort()
        if node.is_full():
            return self._split(node)
        return None, None

    def _insert_into_internal(self, node, key, child):
        node.keys.append(key)
        node.keys.sort()
        i = node.keys.index(key)
        node.children.insert(i + 1, child)
        if node.is_full():
            return self._split(node)
        return None, None

    def _split(self, node):
        mid_key = node.keys[1]
        if node.is_leaf():
            new_node = TwoThreeTreeNode([node.keys[2]])
        else:
            new_node = TwoThreeTreeNode([node.keys[2]], node.children[2:])
        node.keys = [node.keys[0]]
        node.children = node.children[:2] if node.children else []
        return new_node, mid_key


class HuffmanTree(_BinaryTree):
    """
    Дерево Хаффмана - это структура, на которой держится алгоритм сжатия Хаффмана.
    Алгоритм заключается в том, что мы кодируем элементы строки по-своему:
    элементы, которые встречаются чаще, кодируются короче.

    .. image:: images/huffman_tree.png

    """
    def __init__(self, tree_node_type=HuffmanNode):
        super().__init__(tree_node_type)

    @staticmethod
    def get_frequency_map(s: str) -> dict:
        """
        Статический метод для образования словаря частот.

        :param s: строка, для которой нужен словарь частот
        :return: Словарь, где ключи — символы, а значения — их частоты
        """
        res = defaultdict(int)
        for char in s:
            res[char] += 1
        return dict(res)


    def build(self, frequency_map=None):
        """
        Построение дерева Хаффмана из словаря частот символов.

        :param frequency_map: Словарь, где ключи — символы, а значения — их частоты.
        """
        if frequency_map is None:
            frequency_map = {}

        heap = MinHeap([HuffmanNode(char, freq) for char, freq in frequency_map.items()])

        while len(heap) > 1:
            left = heap.poll()
            right = heap.poll()

            merged_node = HuffmanNode(None, left.freq + right.freq)
            merged_node.left = left
            merged_node.right = right

            heap.add(merged_node)

        self.root = heap.poll()  # Устанавливаем корень дерева
        self.size = len(frequency_map)

    def generate_codes(self):
        """
        Генерация кодов Хаффмана для каждого символа на основе дерева.

        :return: Словарь, где ключ — символ, значение — его код Хаффмана.
        """
        codes = {}

        def _generate_codes(node, current_code=""):
            if node is None:
                return

            # Если это листовой узел, сохраняем код
            if node.data is not None:
                codes[node.data] = current_code

            _generate_codes(node.left, current_code + "0")
            _generate_codes(node.right, current_code + "1")

        _generate_codes(self.root)
        return codes

    def encode(self, text):
        """
        Кодирование текста с использованием дерева Хаффмана.

        :param text: Текст, который нужно закодировать.
        :return: Закодированная строка.
        """
        codes = self.generate_codes()
        return ''.join(codes[char] for char in text)

    def decode(self, encoded_text):
        """
        Декодирование строки, используя дерево Хаффмана.

        :param encoded_text: Закодированная строка.
        :return: Декодированная строка.
        """
        decoded_text = []
        current_node = self.root

        for bit in encoded_text:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right

            if current_node.data is not None:  # Листовой узел
                decoded_text.append(current_node.data)
                current_node = self.root

        return ''.join(decoded_text)
