from types import SimpleNamespace

from jag import DepthFirstSearch
from jag import Graph
from unittest import TestCase
from jag.signalslot import SignalSlot


class DepthFirstSearchTest(TestCase):
    def setUp(self):
        self.graph = Graph()
        self.dfs = DepthFirstSearch(self.graph)
        self.method_arguments = None
        self.number_of_method_calls = 0

        def method(*args):
            self.method_arguments = args
            self.number_of_method_calls += 1

        self.method = method

    def test___init__(self):
        self.assertIsInstance(self.dfs._graph, Graph)
        self.assertIsInstance(self.dfs, SignalSlot)

    def test_parse_calls__dfs(self):
        self.graph.create_edge(10, 20)
        self.dfs._dfs = self.method
        self.dfs.parse(10)
        self.assertEqual(1, self.number_of_method_calls)
        self.assertEqual((10, set()), self.method_arguments)

    def test__dfs_raises_CycleInDAG(self):
        self.graph.create_edge(10, 20)
        self.graph.create_edge(10, 30)
        self.graph.create_edge(20, 30)
        with self.assertRaises(self.dfs.CycleInDAG):
            self.dfs._dfs(10, set())
            # TODO check message

    def test__dfs(self):
        ns = SimpleNamespace()
        ns.entries = []
        ns.leafs = []
        ns.exits = []

        def entry(node):
            ns.entries.append(node)

        def leaf(node):
            ns.leafs.append(node)

        # noinspection PyShadowingBuiltins
        def exit(node):
            ns.exits.append(node)

        self.dfs.slot('entry', entry)
        self.dfs.slot('leaf', leaf)
        self.dfs.slot('exit', exit)
        for edge in ((0, 1), (0, 2), (0, 3), (2, 4), (2, 5)):
            self.graph.create_edge(*edge)
        self.dfs.parse(0)
        expect = [0, 1, 2, 4, 5, 3]
        self.assertEqual(expect, ns.entries)
        expect = [1, 4, 5, 2, 3, 0]
        self.assertEqual(expect, ns.exits)
        expect = [1, 4, 5, 3]
        self.assertEqual(expect, ns.leafs)

    def test__entry(self):
        self.dfs.slot('entry', self.method)
        self.dfs._entry(10)
        self.assertEqual(10, self.method_arguments[0])

    def test__leaf(self):
        self.dfs.slot('leaf', self.method)
        self.dfs._leaf(10)
        self.assertEqual(10, self.method_arguments[0])

    def test__exit(self):
        self.dfs.slot('exit', self.method)
        self.dfs._exit(10)
        self.assertEqual(10, self.method_arguments[0])
