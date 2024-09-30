from datastructures.trees.nodes import *
from pytest import raises, fixture


class TestBinaryNode:
    @fixture
    def tree_fixture(self):
        """
        Фикстура для создания бинарного дерева.
        """
        # Создаем корневой узел
        root = BinaryNode(10)

        # Вставляем узлы перед и после существующих узлов, чтобы построить дерево
        node1 = BinaryNode(5)
        node2 = BinaryNode(15)
        root.subtree_insert_before(node1)  # Вставляем узел 5 перед 10
        root.subtree_insert_after(node2)   # Вставляем узел 15 после 10

        node3 = BinaryNode(3)
        node4 = BinaryNode(7)
        node1.subtree_insert_before(node3)  # Вставляем узел 3 перед 5
        node1.subtree_insert_after(node4)   # Вставляем узел 7 после 5

        node5 = BinaryNode(12)
        node6 = BinaryNode(18)
        node2.subtree_insert_before(node5)  # Вставляем узел 12 перед 15
        node2.subtree_insert_after(node6)   # Вставляем узел 18 после 15

        return root

    def test_inorder_traversal(self, tree_fixture):
        values = [node.data for node in tree_fixture.inorder_traversal()]
        assert values == [3, 5, 7, 10, 12, 15, 18]

    def test_preorder_traversal(self, tree_fixture):
        values = [node.data for node in tree_fixture.preorder_traversal()]
        assert values == [10, 5, 3, 7, 15, 12, 18]

    def test_postorder_traversal(self, tree_fixture):
        values = [node.data for node in tree_fixture.postorder_traversal()]
        assert values == [3, 7, 5, 12, 18, 15, 10]

    def test_level_order_traversal(self, tree_fixture):
        values = [node.data for node in tree_fixture.level_order_traversal()]
        assert values == [10, 5, 15, 3, 7, 12, 18]

    def test_subtree_first(self, tree_fixture):
        first_node = tree_fixture.subtree_first()
        assert first_node.data == 3

    def test_subtree_last(self, tree_fixture):
        last_node = tree_fixture.subtree_last()
        assert last_node.data == 18

    def test_successor(self, tree_fixture):
        node = tree_fixture.left  # Узел с данными 5
        successor = node.successor()
        assert successor.data == 7

        node = tree_fixture  # Корневой узел с данными 10
        successor = node.successor()
        assert successor.data == 12

    def test_predecessor(self, tree_fixture):
        node = tree_fixture.right  # Узел с данными 15
        predecessor = node.predecessor()
        assert predecessor.data == 12

        node = tree_fixture  # Корневой узел с данными 10
        predecessor = node.predecessor()
        assert predecessor.data == 7

    def test_subtree_insert_before(self, tree_fixture):
        new_node = BinaryNode(6)
        print(tree_fixture.left)
        tree_fixture.left.subtree_insert_before(new_node)
        values = [node.data for node in tree_fixture.inorder_traversal()]
        assert values == [3, 6, 5, 7, 10, 12, 15, 18]

    def test_subtree_insert_after(self, tree_fixture):
        new_node = BinaryNode(16)
        tree_fixture.right.subtree_insert_after(new_node)
        values = [node.data for node in tree_fixture.inorder_traversal()]
        assert values == [3, 5, 7, 10, 12, 15, 16, 18]

    def test_subtree_delete(self, tree_fixture):
        node_to_delete = tree_fixture.left.right  # Узел с данными 7
        deleted_node = node_to_delete.subtree_delete()
        assert deleted_node.data == 7

        values = [node.data for node in tree_fixture.inorder_traversal()]
        assert values == [3, 5, 10, 12, 15, 18]


class TestBalancingNode:
    @fixture
    def balancing_tree(self):
        """
        Фикстура для создания сбалансированного бинарного дерева.
        """
        # Создаем корневой узел
        root = BalancingNode(10)

        # Вставляем узлы перед и после существующих узлов, чтобы построить дерево
        node1 = BalancingNode(5)
        node2 = BalancingNode(15)
        root.subtree_insert_before(node1)  # Вставляем узел 5 перед 10
        root.subtree_insert_after(node2)   # Вставляем узел 15 после 10

        node3 = BalancingNode(3)
        node4 = BalancingNode(7)
        node1.subtree_insert_before(node3)  # Вставляем узел 3 перед 5
        node1.subtree_insert_after(node4)   # Вставляем узел 7 после 5

        node5 = BalancingNode(12)
        node6 = BalancingNode(18)
        node2.subtree_insert_before(node5)  # Вставляем узел 12 перед 15
        node2.subtree_insert_after(node6)   # Вставляем узел 18 после 15

        return root

    def test_height(self, balancing_tree):
        """
        Тест метода height.
        """
        assert height(balancing_tree) == 2  # Корень имеет высоту 2
        assert height(balancing_tree.left) == 1  # Узел 5 имеет высоту 1
        assert height(balancing_tree.right) == 1  # Узел 15 имеет высоту 1
        assert height(None) == -1  # Проверка на отсутствие узла

    def test_skew(self, balancing_tree):
        """
        Тест вычисления скоса дерева.
        """
        assert balancing_tree.skew() == 0  # Дерево сбалансировано
        balancing_tree.left.left.subtree_delete()  # Удалим левый узел (3)
        balancing_tree.subtree_update()  # Обновляем дерево
        assert abs(balancing_tree.skew()) <= 1  # Левое поддерево стало меньше

    def test_balancing(self, balancing_tree):
        node = balancing_tree.subtree_last()
        for i in range(10):
            node.subtree_insert_after(BalancingNode(i))

        assert abs(balancing_tree.skew()) <= 1


class TestSearchNode:

    @fixture
    def search_tree(self):
        """
        Фикстура для создания бинарного дерева поиска.
        """
        root = SearchNode(10)

        # Строим дерево
        node1 = SearchNode(5)
        node2 = SearchNode(15)
        root.subtree_insert(node1)   # Вставляем узел 5
        root.subtree_insert(node2)   # Вставляем узел 15

        node3 = SearchNode(3)
        node4 = SearchNode(7)
        node1.subtree_insert(node3)  # Вставляем узел 3
        node1.subtree_insert(node4)  # Вставляем узел 7

        node5 = SearchNode(12)
        node6 = SearchNode(18)
        node2.subtree_insert(node5)  # Вставляем узел 12
        node2.subtree_insert(node6)  # Вставляем узел 18

        return root

    def test_subtree_find(self, search_tree):
        assert search_tree.subtree_find(5).data == 5
        assert search_tree.subtree_find(12).data == 12
        assert search_tree.subtree_find(20) is None  # Узла с таким значением нет

    def test_subtree_find_next(self, search_tree):
        assert search_tree.subtree_find_next(5).data == 7
        assert search_tree.subtree_find_next(10).data == 12
        assert search_tree.subtree_find_next(18) is None  # Следующего узла нет

    def test_subtree_find_prev(self, search_tree):
        assert search_tree.subtree_find_prev(7).data == 5
        assert search_tree.subtree_find_prev(10).data == 7
        assert search_tree.subtree_find_prev(3) is None  # Предыдущего узла нет

    def test_subtree_insert(self, search_tree):
        new_node = SearchNode(8)
        search_tree.subtree_insert(new_node)

        values = [node.data for node in search_tree.inorder_traversal()]
        assert values == [3, 5, 7, 8, 10, 12, 15, 18]

    def test_subtree_insert_duplicate(self, search_tree):
        new_node = SearchNode(5)
        search_tree.subtree_insert(new_node)

        # Проверим, что дерево не добавляет дубликат узла с таким же значением
        values = [node.data for node in search_tree.inorder_traversal()]
        assert values == [3, 5, 7, 10, 12, 15, 18]


class TestSegmentNode:

    @fixture
    def segment_tree(self):
        """
        Фикстура для создания сегментного дерева с использованием только методов subtree_insert_before и subtree_insert_after.
        """
        root = SegmentNode(10)

        # Строим дерево
        node1 = SegmentNode(5)
        node2 = SegmentNode(15)

        # Вставляем узлы 5 и 15 в дерево
        root.subtree_insert_before(node1)  # Вставляем узел 5 до корня
        root.subtree_insert_after(node2)   # Вставляем узел 15 после корня

        node3 = SegmentNode(3)
        node4 = SegmentNode(7)

        # Вставляем узлы 3 и 7 в поддерево левого узла (5)
        node1.subtree_insert_before(node3)  # Вставляем узел 3 до узла 5
        node1.subtree_insert_after(node4)   # Вставляем узел 7 после узла 5

        node5 = SegmentNode(12)
        node6 = SegmentNode(18)

        # Вставляем узлы 12 и 18 в поддерево правого узла (15)
        node2.subtree_insert_before(node5)  # Вставляем узел 12 до узла 15
        node2.subtree_insert_after(node6)   # Вставляем узел 18 после узла 15

        # Обновляем размеры дерева
        root.subtree_update()

        return root


    def test_subtree_at(self, segment_tree):
        """
        Тест на нахождение i-го узла по индексу.
        """
        print(segment_tree.subtree_at(0))

        assert segment_tree.subtree_at(0).data == 3
        assert segment_tree.subtree_at(1).data == 5
        assert segment_tree.subtree_at(2).data == 7
        assert segment_tree.subtree_at(3).data == 10
        assert segment_tree.subtree_at(4).data == 12
        assert segment_tree.subtree_at(5).data == 15
        assert segment_tree.subtree_at(6).data == 18

    def test_subtree_at_out_of_bounds(self, segment_tree):
        """
        Тест на обращение к индексу, который выходит за границы дерева.
        """
        with raises(AssertionError):
            segment_tree.subtree_at(-1)  # Индекс меньше 0
        with raises(AttributeError):
            segment_tree.subtree_at(7)   # Индекс выходит за границы дерева


class TestAVLNode:
    @fixture
    def avl_tree(self):
        """
        Фикстура для создания бинарного дерева поиска.
        """
        root = AVLNode(10)

        # Строим дерево
        node1 = AVLNode(5)
        node2 = AVLNode(15)
        root.subtree_insert(node1)   # Вставляем узел 5
        root.subtree_insert(node2)   # Вставляем узел 15

        node3 = AVLNode(3)
        node4 = AVLNode(7)
        node1.subtree_insert(node3)  # Вставляем узел 3
        node1.subtree_insert(node4)  # Вставляем узел 7

        node5 = AVLNode(12)
        node6 = AVLNode(18)
        node2.subtree_insert(node5)  # Вставляем узел 12
        node2.subtree_insert(node6)  # Вставляем узел 18

        return root

    def test_subtree_find(self, avl_tree):
        assert avl_tree.subtree_find(5).data == 5
        assert avl_tree.subtree_find(12).data == 12
        assert avl_tree.subtree_find(20) is None  # Узла с таким значением нет

    def test_subtree_insert_duplicate(self, avl_tree):
        new_node = AVLNode(5)
        avl_tree.subtree_insert(new_node)

        # Проверим, что дерево не добавляет дубликат узла с таким же значением
        values = [node.data for node in avl_tree.inorder_traversal()]
        assert values == [3, 5, 7, 10, 12, 15, 18]

    def test_subtree_insert(self, avl_tree):
        new_node = AVLNode(8)
        avl_tree.subtree_insert(new_node)

        values = [node.data for node in avl_tree.inorder_traversal()]
        assert values == [3, 5, 7, 8, 10, 12, 15, 18]

    def test_balancing(self, avl_tree):
        node = avl_tree.subtree_last()
        for i in range(10):
            node.subtree_insert(AVLNode(i + 100))

        assert abs(avl_tree.skew()) <= 1