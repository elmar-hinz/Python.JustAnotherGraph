from jag import Graph
from jag.signalslot import SignalSlot


class DepthFirstSearch(SignalSlot):
    """This class executes a depth first search on a given graph.
    
    The class can be used in two ways:
    
    1. By subclassing and implementing methods *entry*, *leaf*, *exit* that 
    are called during the visit of the nodes. 
    2. By registering methods to slots that are triggered during the visit of 
    the nodes by the signals *entry*, *leaf* or *exit*. 
    """

    # noinspection PyClassHasNoInit
    class CycleInDAG(Exception):
        pass

    def __init__(self, graph: Graph) -> None:
        """Create a DepthFirstSearch object.
        
        :param graph: The graph to parse. 
        """
        super().__init__()
        self._graph = graph

    def parse(self, root):
        """Run the depth first search from the given root node.

        Walks recursively through the tree. Calls the methods _entry, _leaf, 
        _exit. 
        
        Each of this methods by default sends a signal of the same name. This 
        signals trigger the notification of methods that may be registered 
        into slots by the names of the signals. See: _SignalSlot.

        Raises CycleInDAG error in case of a cycle.

        :param root: ID of current node.
        :signal entry: On entering the node.
        :signal leaf: If the node is a leaf.
        :signal exit: On leaving the node.
        """
        self._dfs(root, set())

    def _dfs(self, node, seen: set):
        if node in seen:
            msg = 'Unexpected cycle detected at node {}.'.format(node)
            raise self.CycleInDAG(msg)
        self._entry(node)
        seen.add(node)
        if len(self._graph.successors(node)) == 0:
            self._leaf(node)
        else:
            for child in self._graph.successors(node):
                self._dfs(child, seen)
        self._exit(node)

    def _entry(self, node):
        self.signal('entry', node)

    def _leaf(self, node):
        self.signal('leaf', node)

    def _exit(self, node):
        self.signal('exit', node)
