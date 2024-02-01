from pytest import fixture, mark
from datastructures import ListAdjacency, MatrixAdjacency


class TestMatrixAdjacency:

    @fixture
    def directed_graph(self):
        return MatrixAdjacency(6, True)

    @fixture
    def undirected_graph(self):
        return MatrixAdjacency(6, False)

    @mark.parametrize('from_node,to_node,weight', [
        (0, 1, 1),
        (0, 1, 2),
        (0, 0, 1),
    ])
    def test_add_edge(self, directed_graph, from_node, to_node, weight):
        directed_graph.add_edge(from_node, to_node, weight)
        assert directed_graph.matrix[from_node][to_node] == weight

    @mark.parametrize('from_node,to_node,weight', [
        (0, 1, 1),
        (0, 1, 2),
        (0, 0, 1),
    ])
    def test_undirected_add_edge(self, undirected_graph, from_node, to_node, weight):
        undirected_graph.add_edge(from_node, to_node, weight)
        assert undirected_graph.matrix[from_node][to_node] == weight
        assert undirected_graph.matrix[to_node][from_node] == weight

    def test_remove_edge(self, directed_graph):
        directed_graph.add_edge(0, 1, 1)
        assert directed_graph.remove_edge(0, 1) == 1  # Remove the edge
        assert directed_graph.remove_edge(0, 1) == 0 or \
            directed_graph.remove_edge(0, 1) == -1  # Edge doesn't exist

    def test_undirected_remove_edge(self, undirected_graph):
        undirected_graph.add_edge(0, 1, 1)
        assert undirected_graph.remove_edge(1, 0) == 1
        assert undirected_graph.remove_edge(1, 0) == 0 or \
            undirected_graph.remove_edge(1, 0) == -1  # Remove the edge
        assert undirected_graph.remove_edge(0, 1) == 0 or \
            undirected_graph.remove_edge(0, 1) == -1  # Edge doesn't exist

    def test_shortest_path(self, directed_graph):
        directed_graph.add_edge(0, 1, 1)
        directed_graph.add_edge(0, 2, 5)
        directed_graph.add_edge(1, 3, 2)
        directed_graph.add_edge(2, 3, 3)

        distance, path = directed_graph.shortest_path(0, 3)
        assert distance == 3
        assert path == [0, 1, 3]

    def test_bfs(self, directed_graph):
        directed_graph.add_edge(0, 2)
        directed_graph.add_edge(0, 1)
        directed_graph.add_edge(1, 4)
        directed_graph.add_edge(1, 3)
        directed_graph.add_edge(2, 5)

        assert list(directed_graph.breadth_first_traversal(0)) == [0, 1, 2, 3, 4, 5]
        assert list(directed_graph.breadth_first_traversal(1)) == [1, 3, 4]

    def test_dfs(self, directed_graph):
        directed_graph.add_edge(0, 1)
        directed_graph.add_edge(0, 2)
        directed_graph.add_edge(1, 3)
        directed_graph.add_edge(1, 4)
        directed_graph.add_edge(2, 5)

        assert list(directed_graph.depth_first_traversal(0)) == [0, 1, 3, 4, 2, 5] or \
            list(directed_graph.depth_first_traversal(0)) == [0, 2, 5, 1, 4, 3]
        assert list(directed_graph.depth_first_traversal(1)) == [1, 3, 4] or \
            list(directed_graph.depth_first_traversal(1)) == [1, 4, 3]


class TestListAdjacency(TestMatrixAdjacency):

    @fixture
    def directed_graph(self):
        return ListAdjacency(6, True)

    @fixture
    def undirected_graph(self):
        return ListAdjacency(6, False)

    @mark.parametrize('from_node,to_node,weight', [
        (0, 1, 1),
        (0, 1, 2),
        (0, 0, 1),
    ])
    def test_add_edge(self, directed_graph, from_node, to_node, weight):
        directed_graph.add_edge(from_node, to_node, weight)

        # Check if the edge is added correctly
        edges = directed_graph.list[from_node]
        edge_found = False
        while edges:
            if edges.v2 == to_node and edges.weight == weight:
                edge_found = True
                break
            edges = edges.next

        assert edge_found

    @mark.parametrize('from_node,to_node,weight', [
        (0, 1, 1),
        (0, 1, 2),
        (0, 0, 1),
    ])
    def test_undirected_add_edge(self, undirected_graph, from_node, to_node, weight):
        undirected_graph.add_edge(from_node, to_node, weight)

        edges1, edges2 = undirected_graph.list[from_node], undirected_graph.list[to_node]
        edge1_found, edge2_found = False, False
        while edges1:
            if edges1.v2 == to_node and edges1.weight == weight:
                edge1_found = True
                break
            edges1 = edges1.next

        while edges2:
            if edges2.v2 == from_node and edges2.weight == weight:
                edge2_found = True
                break
            edges2 = edges2.next

        assert edge1_found and edge2_found

