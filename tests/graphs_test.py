import pytest
from datastructures import ListAdjacency


class TestListAdjacency:

    @pytest.fixture
    def directed_graph(self):
        g = ListAdjacency(6, True)
        return g

    @pytest.fixture
    def undirected_graph(self):
        g = ListAdjacency(6, False)
        return g

    @pytest.mark.parametrize('from_node,to_node,weight', [
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

    def test_remove_edge(self, directed_graph):
        directed_graph.add_edge(0, 1, 1)
        assert directed_graph.remove_edge(0, 1) == 1  # Remove the edge
        assert directed_graph.remove_edge(0, 1) == -1  # Edge doesn't exist

    def test_shortest_path(self, directed_graph):
        directed_graph.add_edge(0, 1, 1)
        directed_graph.add_edge(0, 2, 5)
        directed_graph.add_edge(1, 3, 2)
        directed_graph.add_edge(2, 3, 3)

        distance, path = directed_graph.shortest_path(0, 3)
        assert distance == 3
        assert path == [0, 1, 3]
