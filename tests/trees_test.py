from pytest import fixture
from datastructures import \
    Trie, BinaryTree, BinaryTreeNode, BSTNode, BST


class TestTrie:
    words = [
        "preclude",
        "predict",
        "prefix",
        "preface",
        "prehistoric",
        "disagree",
        "disapprove",
        "disrupt",
        "disappear",
        "disarray",
        "apple",
        "abricot"
    ]

    @fixture
    def empty_trie(self):
        return Trie()

    @fixture
    def filled_trie(self, empty_trie):
        empty_trie.insert(*self.words)
        return empty_trie

    def test_get_words(self, filled_trie):
        for word in filled_trie.get_words_with_prefix("dis"):
            assert word in ["disagree",
                            "disapprove",
                            "disrupt",
                            "disappear",
                            "disarray"]
        assert len(filled_trie.get_words_with_prefix("dis")) == 5
        assert len(filled_trie.get_words_with_prefix("pre")) == 5
        assert filled_trie.get_words_with_prefix("pre") != filled_trie.get_words_with_prefix("dis")

    def test_insert(self, empty_trie):
        empty_trie.insert(*self.words)
        for word in empty_trie:
            assert word in self.words

    def test_search(self, filled_trie):
        for word in filled_trie:
            assert word in self.words
        assert "pineapple" not in filled_trie
        assert "disappears" not in filled_trie


class TestBinaryTree:

    class TestBinaryTreeNode:

        @fixture
        def root_node(self):
            return BinaryTreeNode(5)

        @fixture
        def child_node(self):
            return BinaryTreeNode(3)

        def test_insert_before_root(self, root_node, child_node):
            root_node.subtree_insert_before(child_node)
            assert root_node.left == child_node
            assert child_node.parent == root_node

        def test_insert_after_root(self, root_node, child_node):
            node = BinaryTreeNode(7)
            root_node.subtree_insert_after(node)
            assert root_node.right == node
            assert node.parent == root_node

        @fixture
        def node_with_children(self):
            root = BinaryTreeNode(5)
            left = BinaryTreeNode(3)
            right = BinaryTreeNode(7)
            root.subtree_insert_before(left)
            root.subtree_insert_after(right)
            return root, left, right

        def test_insert_before_node_with_children(self, node_with_children):
            root, left, right = node_with_children
            node = BinaryTreeNode(2)
            left.subtree_insert_before(node)
            assert left.left == node
            assert node.parent == left

        def test_insert_after_node_with_children(self, node_with_children):
            root, left, right = node_with_children
            node = BinaryTreeNode(8)
            right.subtree_insert_after(node)
            assert right.right == node
            assert node.parent == right

        def test_insert_at_end_of_tree(self, node_with_children):
            root, left, right = node_with_children
            node = BinaryTreeNode(10)
            right.subtree_insert_after(node)
            assert right.right == node
            assert node.parent == right

        def test_traversal(self, node_with_children):
            root, left, right = node_with_children
            inorder = list(root.inorder_traversal())
            assert [node.data for node in inorder] == [3, 5, 7]

        def test_delete_node_with_one_child(self, node_with_children):
            root, left, right = node_with_children
            left.subtree_delete()
            assert root.left is None
            assert left.parent is None

        def test_delete_node_with_two_children(self, node_with_children):
            root, left, right = node_with_children
            root.subtree_delete()
            assert root.left is None
            assert root.right is not None

        def test_update_node_value(self, root_node):
            root_node.data = 10
            assert root_node.data == 10

        def test_preorder_traversal(self, node_with_children):
            root, left, right = node_with_children
            preorder = list(root.preorder_traversal())
            assert [node.data for node in preorder] == [5, 3, 7]

        def test_postorder_traversal(self, node_with_children):
            root, left, right = node_with_children
            postorder = list(root.postorder_traversal())
            assert [node.data for node in postorder] == [3, 7, 5]

    @fixture
    def empty_tree(self):
        return BinaryTree()

    @fixture
    def populated_tree(self):
        tree = BinaryTree()
        tree.root = BinaryTreeNode(4)
        tree.root.subtree_insert_before(BinaryTreeNode(2))
        tree.root.subtree_insert_after(BinaryTreeNode(6))
        tree.root.left.subtree_insert_before(BinaryTreeNode(1))
        tree.root.left.subtree_insert_after(BinaryTreeNode(3))
        tree.root.right.subtree_insert_before(BinaryTreeNode(5))
        tree.size = 6
        return tree

    def test_empty_tree(self, empty_tree):
        assert len(empty_tree) == 0

    def test_insert_root(self, empty_tree):
        node = BinaryTreeNode(5)
        empty_tree.root = node
        empty_tree.size += 1
        assert empty_tree.root == node
        assert len(empty_tree) == 1

    def test_tree_traversal(self, populated_tree):
        inorder = list(populated_tree.root.inorder_traversal())
        assert [node.data for node in inorder] == [1, 2, 3, 4, 5, 6]

    def test_tree_insert(self, empty_tree):
        nodes = [BinaryTreeNode(i) for i in range(1, 6)]
        empty_tree.root = nodes[2]
        empty_tree.size += 1
        empty_tree.root.subtree_insert_before(nodes[1])
        empty_tree.size += 1
        empty_tree.root.subtree_insert_after(nodes[3])
        empty_tree.size += 1
        nodes[1].subtree_insert_before(nodes[0])
        empty_tree.size += 1
        nodes[3].subtree_insert_after(nodes[4])
        empty_tree.size += 1
        inorder = list(empty_tree.root.inorder_traversal())
        assert [node.data for node in inorder] == [1, 2, 3, 4, 5]
        assert len(empty_tree) == 5

    def test_delete_node(self, populated_tree):
        tree = populated_tree
        tree.root.subtree_delete()
        inorder = list(tree.root.inorder_traversal())
        assert [node.data for node in inorder] == [1, 2, 3, 5, 6]

    def test_tree_balance_after_operations(self, empty_tree):
        nodes = [BinaryTreeNode(i) for i in range(1, 5)]
        empty_tree.root = nodes[1]
        empty_tree.size += 1
        empty_tree.root.subtree_insert_before(nodes[0])
        empty_tree.size += 1
        empty_tree.root.subtree_insert_after(nodes[2])
        empty_tree.size += 1
        nodes[2].subtree_insert_after(nodes[3])
        empty_tree.size += 1

        assert empty_tree.root.skew() == 1

        nodes[3].subtree_delete()
        empty_tree.size -= 1

        assert empty_tree.root.skew() == 0


class TestBST:

    class TestBSTNode:

        @fixture
        def root_node(self):
            return BSTNode(5)

        @fixture
        def child_node(self):
            return BSTNode(3)

        def test_subtree_find(self, root_node):
            node_7 = BSTNode(7)
            root_node.subtree_insert_after(node_7)
            found_node = root_node.subtree_find(7)
            assert found_node == node_7

        def test_subtree_find_next(self, root_node):
            node_7 = BSTNode(7)
            root_node.subtree_insert_after(node_7)
            next_node = root_node.subtree_find_next(5)
            assert next_node == node_7

        def test_subtree_find_prev(self, root_node):
            node_3 = BSTNode(3)
            root_node.subtree_insert_before(node_3)
            prev_node = root_node.subtree_find_prev(5)
            assert prev_node == node_3

        def test_subtree_insert(self, root_node, child_node):
            root_node.subtree_insert(child_node)
            assert root_node.left == child_node
            assert child_node.parent == root_node

    @fixture
    def empty_tree(self):
        return BST()

    @fixture
    def populated_tree(self):
        tree = BST()
        tree.build([5, 3, 7, 2, 4, 6, 8])
        return tree

    def test_empty_tree(self, empty_tree):
        assert len(empty_tree) == 0

    def test_insert_root(self, empty_tree):
        empty_tree.insert(5)
        assert empty_tree.root.data == 5
        assert len(empty_tree) == 1

    def test_tree_build(self, empty_tree):
        empty_tree.build([5, 3, 7, 2, 4, 6, 8])
        inorder = list(empty_tree.root.inorder_traversal())
        assert [node.data for node in inorder] == [2, 3, 4, 5, 6, 7, 8]

    def test_tree_find_min(self, populated_tree):
        assert populated_tree.find_min() == 2

    def test_tree_find_max(self, populated_tree):
        assert populated_tree.find_max() == 8

    def test_tree_find(self, populated_tree):
        assert populated_tree.find(4) == 4
        assert populated_tree.find(10) is None

    def test_tree_find_next(self, populated_tree):
        assert populated_tree.find_next(4) == 5
        assert populated_tree.find_next(8) is None

    def test_tree_find_prev(self, populated_tree):
        assert populated_tree.find_prev(4) == 3
        assert populated_tree.find_prev(2) is None

    def test_tree_insert(self, empty_tree):
        assert empty_tree.insert(5)
        assert empty_tree.insert(3)
        assert not empty_tree.insert(5)  # Duplicate
        inorder = list(empty_tree.root.inorder_traversal())
        assert [node.data for node in inorder] == [3, 5]

    def test_tree_delete(self, populated_tree):
        populated_tree.delete(3)
        inorder = list(populated_tree.root.inorder_traversal())
        assert [node.data for node in inorder] == [2, 4, 5, 6, 7, 8]

    def test_tree_delete_root(self, populated_tree):
        populated_tree.delete(5)
        inorder = list(populated_tree.root.inorder_traversal())
        assert [node.data for node in inorder] == [2, 3, 4, 6, 7, 8]

    def test_tree_balance_after_operations(self, empty_tree):
        nodes = [BSTNode(i) for i in range(1, 5)]
        empty_tree.root = nodes[1]
        empty_tree.root.subtree_insert_before(nodes[0])
        empty_tree.root.subtree_insert_after(nodes[2])
        nodes[2].subtree_insert_after(nodes[3])

        assert empty_tree.root.skew() == 1

        nodes[3].subtree_delete()
        empty_tree.size -= 1

        assert empty_tree.root.skew() == 0
