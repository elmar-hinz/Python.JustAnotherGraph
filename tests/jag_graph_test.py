from unittest import TestCase
from types import SimpleNamespace
from jag import Graph


# noinspection PyShadowingBuiltins
class GraphTest(TestCase):
    """Test units of FastGraph."""

    def setUp(self):
        self.graph = Graph()

    def test__init__(self):
        self.assertIsInstance(self.graph._nodes, dict)
        self.assertIsInstance(self.graph._tails, dict)
        self.assertIsInstance(self.graph._heads, dict)
        self.assertIsInstance(self.graph._edges, dict)

    def test_node_exists_false(self):
        result = self.graph.node_exists(3)
        self.assertFalse(result)

    def test_node_exists_true(self):
        id = 3
        self.graph._tails[id] = True
        self.graph._heads[id] = True
        self.graph._nodes[id] = True
        result = self.graph.node_exists(id)
        self.assertTrue(result)

    def test_node_exists_raises_but_not_in_tails(self):
        id = 10
        self.graph._nodes[id] = True
        self.graph._heads[id] = True
        with self.assertRaises(Graph.NodeInconsistency) as raised:
            self.graph.node_exists(id)
        result = str(raised.exception)
        expect = 'ID 10 in _nodes but not in _tails.'
        self.assertEqual(expect, result)

    def test_node_exists_raises_but_not_in_heads(self):
        id = 10
        self.graph._nodes[id] = True
        self.graph._tails[id] = True
        with self.assertRaises(Graph.NodeInconsistency) as raised:
            self.graph.node_exists(id)
        result = str(raised.exception)
        expect = 'ID 10 in _nodes but not in _heads.'
        self.assertEqual(expect, result)

    def test_node_exists_raises_but_in_tails(self):
        id = 10
        self.graph._tails[id] = True
        with self.assertRaises(Graph.NodeInconsistency) as raised:
            self.graph.node_exists(id)
        result = str(raised.exception)
        expect = 'ID 10 not in _nodes but in _tails.'
        self.assertEqual(expect, result)

    def test_node_exists_raises_but_in_heads(self):
        id = 10
        self.graph._heads[id] = True
        with self.assertRaises(Graph.NodeInconsistency) as raised:
            self.graph.node_exists(id)
        result = str(raised.exception)
        expect = 'ID 10 not in _nodes but in _heads.'
        self.assertEqual(expect, result)

    def test_edge_exists_false(self):
        result = self.graph.edge_exists(1, 2)
        self.assertFalse(result)

    def test_edge_exists_true(self):
        tail = 1
        self.graph._tails[tail] = True
        self.graph._heads[tail] = True
        self.graph._nodes[tail] = True
        head = 2
        self.graph._tails[head] = True
        self.graph._heads[head] = True
        self.graph._nodes[head] = True
        self.graph._edges[(tail, head)] = True
        result = self.graph.edge_exists(tail, head)
        self.assertTrue(result)

    def test_edge_exists_raises_tail_does_not_exist(self):
        tail, head = 10, 20
        self.graph._nodes[head] = True
        self.graph._heads[head] = True
        self.graph._tails[head] = True
        self.graph._edges[(tail, head)] = True
        with self.assertRaises(Graph.EdgeInconsistency) as raised:
            self.graph.edge_exists(tail, head)
        result = str(raised.exception)
        expect = 'Edge (10, 20) in _edges but tail 10 does not exist.'
        self.assertEqual(expect, result)

    def test_edge_exists_raises_head_does_not_exist(self):
        tail, head = 10, 20
        self.graph._nodes[tail] = True
        self.graph._heads[tail] = True
        self.graph._tails[tail] = True
        self.graph._edges[(tail, head)] = True
        with self.assertRaises(Graph.EdgeInconsistency) as raised:
            self.graph.edge_exists(tail, head)
        result = str(raised.exception)
        expect = 'Edge (10, 20) in _edges but head 20 does not exist.'
        self.assertEqual(expect, result)

    def test_node_tag_exists_true(self):
        name, id = 'aa', 10
        self.graph.create_node(10)
        self.graph._nodes[id][name] = True
        result = self.graph.node_tag_exists(id, name)
        self.assertTrue(result)

    def test_node_tag_exists_false(self):
        name, id = 'aa', 10
        self.graph.create_node(10)
        result = self.graph.node_tag_exists(id, name)
        self.assertFalse(result)

    def test_node_tag_exists_raises_no_node(self):
        with self.assertRaises(Graph.NodeMissing) as raised:
            self.graph.node_tag_exists(10, 'aa')
        result = str(raised.exception)
        expect = 'No node 10.'
        self.assertEqual(expect, result)

    def test_edge_tag_exists_true(self):
        tail, head, name = 10, 20, 'aa'
        self.graph.create_edge(tail, head)
        self.graph._edges[(tail, head)][name] = True
        result = self.graph.edge_tag_exists(tail, head, name)
        self.assertTrue(result)

    def test_edge_tag_exists_false(self):
        tail, head, name = 10, 20, 'aa'
        self.graph.create_edge(tail, head)
        result = self.graph.edge_tag_exists(tail, head, name)
        self.assertFalse(result)

    def test_edge_tag_exists_raises_no_edge(self):
        with self.assertRaises(Graph.EdgeMissing) as raised:
            self.graph.edge_tag_exists(10, 20, 'aa')
        result = str(raised.exception)
        expect = 'No edge (10, 20).'
        self.assertEqual(expect, result)

    def test_create_node_non_existent(self):
        result = self.graph.create_node(23)
        self.assertTrue(result)
        self.assertIn(23, self.graph._tails)
        self.assertIn(23, self.graph._heads)
        self.assertIn(23, self.graph._nodes)
        self.assertNotIn(23, self.graph._edges)

    def test_create_node_existent(self):
        result = self.graph.create_node(23)
        self.assertTrue(result)
        result = self.graph.create_node(23)
        self.assertFalse(result)

    def test_create_node_calls_node_exists_twice(self):
        id = 10
        ns = SimpleNamespace()
        ns.count = 0

        def node_exists(i):
            self.assertEqual(i, id)
            ns.count += 1
            return False

        self.graph.node_exists = node_exists
        self.graph.create_node(id)
        self.assertEqual(2, ns.count)

    def test_create_edge_non_existing(self):
        result = self.graph.create_edge(1, 2)
        self.assertTrue(result)
        self.assertIn((1, 2), self.graph._edges)
        self.assertTrue(self.graph.node_exists(1))
        self.assertTrue(self.graph.node_exists(2))

    def test_create_edge_existing(self):
        result = self.graph.create_edge(1, 2)
        self.assertTrue(result)
        result = self.graph.create_edge(1, 2)
        self.assertFalse(result)

    def test_create_edge_calls_edge_exists_twice(self):
        tail, head = 10, 20
        ns = SimpleNamespace()
        ns.count = 0

        def edge_exists(t, h):
            self.assertEqual((t, h), (tail, head))
            ns.count += 1
            return False

        self.graph.edge_exists = edge_exists
        self.graph.create_edge(tail, head)
        self.assertEqual(2, ns.count)

    def test_tag_node(self):
        id, name, value = 10, 'aa', 'vv'
        self.graph.create_node(id)
        self.graph.tag_node(id, name, value)
        result = self.graph._nodes[id][name]
        self.assertEqual(value, result)

    def test_tag_node_value_default(self):
        id, name, value = 10, 'aa', True
        self.graph.create_node(id)
        self.graph.tag_node(id, name)
        result = self.graph._nodes[id][name]
        self.assertEqual(value, result)

    def test_untag_node(self):
        id, name = 10, 'aa'
        self.graph.create_node(id)
        self.graph.tag_node(id, name)
        self.assertTrue(self.graph.node_tag_exists(id, name))
        self.graph.untag_node(id, name)
        self.assertFalse(self.graph.node_tag_exists(id, name))

    def test_tag_node_raises_no_node(self):
        id, name, value = 10, 'aa', 'vv'
        with self.assertRaises(Graph.NodeMissing) as raised:
            self.graph.tag_node(id, name, value)
        result = str(raised.exception)
        expect = 'No node 10.'
        self.assertEqual(expect, result)

    def test_node_tag(self):
        id, name, value = 10, 'aa', 'vv'
        self.graph.create_node(id)
        self.graph.tag_node(id, name, value)
        result = self.graph.node_tag(id, name)
        self.assertEqual(value, result)

    def test_node_tag_raises_no_node(self):
        id, name, value = 10, 'aa', 'vv'
        with self.assertRaises(Graph.NodeMissing) as raised:
            self.graph.node_tag(id, name)
        result = str(raised.exception)
        expect = 'No node 10.'
        self.assertEqual(expect, result)

    def test_node_tag_raises_no_tag_in_node(self):
        id, name, value = 10, 'aa', 'vv'
        self.graph.create_node(id)
        with self.assertRaises(Graph.NodeTagMissing) as raised:
            self.graph.node_tag(id, name)
        result = str(raised.exception)
        expect = 'No tag aa in node 10.'
        self.assertEqual(expect, result)

    def test_tag_edge(self):
        tail, head, name, value = 10, 20, 'aa', 'vv'
        self.graph.create_edge(tail, head)
        self.graph.tag_edge(tail, head, name, value)
        result = self.graph._edges[(tail, head)][name]
        self.assertEqual(value, result)

    def test_tag_edge_value_default(self):
        tail, head, name, value = 10, 20, 'aa', True
        self.graph.create_edge(tail, head)
        self.graph.tag_edge(tail, head, name)
        result = self.graph._edges[(tail, head)][name]
        self.assertEqual(value, result)

    def test_untag_edge(self):
        tail, head, name = 10, 20, 'aa'
        self.graph.create_edge(tail, head)
        self.graph.tag_edge(tail, head, name)
        self.assertTrue(self.graph.edge_tag_exists(tail, head, name))
        self.graph.untag_edge(tail, head, name)
        self.assertFalse(self.graph.edge_tag_exists(tail, head, name))

    def test_tag_edge_raises_no_edge(self):
        tail, head, name, value = 10, 20, 'aa', 'vv'
        with self.assertRaises(Graph.EdgeMissing) as raised:
            self.graph.tag_edge(tail, head, name, value)
        result = str(raised.exception)
        expect = 'No edge (10, 20).'
        self.assertEqual(expect, result)

    def test_edge_tag(self):
        tail, head, name, value = 10, 20, 'aa', 'vv'
        self.graph.create_edge(tail, head)
        self.graph.tag_edge(tail, head, name, value)
        result = self.graph.edge_tag(tail, head, name)
        self.assertEqual(value, result)

    def test_edge_tag_raises_no_edge(self):
        tail, head, name, value = 10, 20, 'aa', 'vv'
        with self.assertRaises(Graph.EdgeMissing) as raised:
            self.graph.tag_edge(tail, head, name, value)
        result = str(raised.exception)
        expect = 'No edge (10, 20).'
        self.assertEqual(expect, result)

    def test_edge_tag_raises_no_tag_in_edge(self):
        tail, head, name, value = 10, 20, 'aa', 'vv'
        self.graph.create_edge(tail, head)
        with self.assertRaises(Graph.EdgeTagMissing) as raised:
            self.graph.edge_tag(tail, head, name)
        result = str(raised.exception)
        expect = 'No tag aa in edge (10, 20).'
        self.assertEqual(expect, result)

    def test_nodes(self):
        self.graph.create_edge(10, 20)
        self.assertCountEqual([20, 10], list(self.graph.nodes))

    def test_edges(self):
        self.graph.create_edge(10, 20)
        self.graph.create_edge(30, 40)
        self.assertCountEqual([(10, 20), (30, 40)], list(self.graph.edges))

    def test_predecessors_empty(self):
        id = 3
        self.graph.create_node(id)
        result = self.graph.predecessors(id)
        expect = set()
        self.assertEqual(expect, result)

    def test_predecessors(self):
        self.graph.create_edge(1, 10)
        self.graph.create_edge(2, 10)
        result = self.graph.predecessors(10)
        expect = {2, 1}
        self.assertEqual(expect, result)

    def test_successors_empty(self):
        id = 3
        self.graph.create_node(id)
        result = self.graph.successors(id)
        expect = set()
        self.assertEqual(expect, result)

    def test_successors(self):
        self.graph.create_edge(10, 1)
        self.graph.create_edge(10, 2)
        result = self.graph.successors(10)
        expect = {2, 1}
        self.assertEqual(expect, result)

    def test_incoming_empty(self):
        id = 3
        self.graph.create_node(id)
        result = self.graph.incoming(id)
        expect = set()
        self.assertEqual(expect, result)

    def test_incoming(self):
        self.graph.create_edge(1, 10)
        self.graph.create_edge(2, 10)
        result = self.graph.incoming(10)
        expect = {(1, 10), (2, 10)}
        self.assertEqual(expect, result)

    def test_outgoing_empty(self):
        id = 3
        self.graph.create_node(id)
        result = self.graph.outgoing(id)
        expect = set()
        self.assertEqual(expect, result)

    def test_outgoing(self):
        self.graph.create_edge(10, 1)
        self.graph.create_edge(10, 2)
        result = self.graph.outgoing(10)
        expect = {(10, 1), (10, 2)}
        self.assertEqual(expect, result)

    def test_count_of_nodes(self):
        self.assertEqual(0, self.graph.count_of_nodes())
        self.graph.create_edge(1, 2)
        self.graph.create_edge(1, 3)
        self.assertEqual(3, self.graph.count_of_nodes())

    def test_count_of_edges(self):
        self.assertEqual(0, self.graph.count_of_edges())
        self.graph.create_edge(1, 2)
        self.graph.create_edge(1, 3)
        self.assertEqual(2, self.graph.count_of_edges())
