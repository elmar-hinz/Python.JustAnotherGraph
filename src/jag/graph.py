# noinspection PyShadowingBuiltins
class Graph:
    """A monolithic implementation of a graph.
    
    While `challenges.Graph` implements edges and nodes as real objects, this
    class is a monolithic implementation of a graph to achieve a better 
    performance.
    
    """

    class Error(Exception):
        pass

    # noinspection PyClassHasNoInit
    class NodeInconsistency(Error):
        pass

    # noinspection PyClassHasNoInit
    class EdgeInconsistency(Error):
        pass

    # noinspection PyClassHasNoInit
    class NodeMissing(Error):
        pass

    # noinspection PyClassHasNoInit
    class EdgeMissing(Error):
        pass

    # noinspection PyClassHasNoInit
    class NodeTagMissing(Error):
        pass

    # noinspection PyClassHasNoInit
    class EdgeTagMissing(Error):
        pass

    # noinspection PyClassHasNoInit
    class CycleInDAG(Error):
        pass

    def __init__(self):
        """Initialise an empty graph. """

        """Flags of nodes."""
        self._nodes = {}
        """Tail to heads."""
        self._tails = {}
        """Head to tails."""
        self._heads = {}
        """Flags of edges."""
        self._edges = {}

    def node_exists(self, id):
        """Check if the given node exists.
        
        Raises NodeInconsistency for inconsistencies of the internal node model.
        
        :param id: Id of the node.
        :return: True if node exists else false.
        """
        if id in self._nodes:
            if id not in self._tails:
                raise self.NodeInconsistency('ID {} in _nodes but not in '
                                             '_tails.'.format(id))
            if id not in self._heads:
                raise self.NodeInconsistency('ID {} in _nodes but not in '
                                             '_heads.'.format(id))
            return True
        else:
            if id in self._tails:
                raise self.NodeInconsistency('ID {} not in _nodes but in '
                                             '_tails.'.format(id))
            if id in self._heads:
                raise self.NodeInconsistency('ID {} not in _nodes but in '
                                             '_heads.'.format(id))
            return False

    def edge_exists(self, tail, head):
        """Check if the given edge exists. 
        
        Raises EdgeInconsistency for inconsistencies of the internal edge model.
        
        :param tail: Node id of tail.
        :param head: Node id of head. 
        :return: True if edge exists else false.
        """
        if (tail, head) in self._edges:
            if not self.node_exists(tail):
                raise self.EdgeInconsistency('Edge ({}, {}) in _edges but '
                                             'tail {} does not '
                                             'exist.'.format(tail, head, tail))
            if not self.node_exists(head):
                raise self.EdgeInconsistency('Edge ({}, {}) in _edges but '
                                             'head {} does not '
                                             'exist.'.format(tail, head, head))
            return True
        else:
            return False

    def node_tag_exists(self, id, name):
        """Check if tag exists in node.
        
        Raises NodeMissing if the node does not exist.
        
        :param id: Node ID. 
        :param name: Tag name.
        :return: Tags existence as boolean.
        """
        if not self.node_exists(id):
            raise self.NodeMissing('No node {}.'.format(id))
        return name in self._nodes[id]

    def edge_tag_exists(self, tail, head, name):
        """Check if tag exists in edge.
        
        Raises EdgeMissing if the edge does not exist.
        
        :param tail: ID of tail node.
        :param head: ID of head node.
        :param name: Tag name.
        :return: Tags existence as boolean.
        """
        if not self.edge_exists(tail, head):
            raise self.EdgeMissing('No edge ({}, {}).'.format(tail, head))
        return name in self._edges[(tail, head)]

    def create_node(self, id):
        """Register a node of the graph.
        
        If the node is not already part of an edge, it will become a 
        standalone node. If it is part of an edge the method has no effect. 
        Typically you will prefer the method *create_edge* to populate the 
        graph. 
        
        :param id: The id of the node.
        :return: False if the node already exists, else True.
        """
        if not self.node_exists(id):
            self._tails[id] = set()
            self._heads[id] = set()
            self._nodes[id] = dict()
            self.node_exists(id)  # Check consistency after creation.
            return True
        else:
            return False

    def create_edge(self, tail, head):
        """Add an edge.

        Create nodes as necessary.

        :param tail: ID of tail. 
        :param head: ID of head.
        :return: False if the node already exists, else True.
        """
        self.create_node(tail)
        self.create_node(head)
        id = (tail, head)
        if not self.edge_exists(tail, head):
            self._edges[id] = dict()
            self._heads[head].add(tail)
            self._tails[tail].add(head)
            self.edge_exists(tail, head)  # Check consistency after creation.
            return True
        else:
            return False

    def tag_node(self, id, name, value=True):
        """Set a tag of a node with a freely selectable value.
        
        If the tag already exists it will be overwritten.
        Raises NodeMissing if the given node does not exist.
        
        :param id: Node to tag.
        :param name: The name of the tag.
        :param value: The value to set the tag to, defaults to True.
        """
        if not self.node_exists(id):
            raise self.NodeMissing('No node {}.'.format(id))
        self._nodes[id][name] = value

    def untag_node(self, id, name):
        """Remove a tag from a node.
        
        :param id: Node to untag. 
        :param name: Name of the tag. 
        """
        if not self.node_exists(id):
            raise self.NodeMissing('No node {}.'.format(id))
        # TODO document and test return
        if name in self._nodes[id]:
            del (self._nodes[id][name])
            return True
        else:
            return False

    def node_tag(self, id, name):
        """Get the value of a node tag.
        
        Raises NodeMissing if the given node does not exist.
        Raises NodeTagMissing if the given tag does not exist.
        
        :param id: ID of node. 
        :param name: Name of tag. 
        :return: Value of tag. 
        """
        if not self.node_exists(id):
            raise self.NodeMissing('No node {}.'.format(id))
        if name not in self._nodes[id]:
            raise self.NodeTagMissing('No tag {} in node {}.'.format(name, id))
        return self._nodes[id][name]

    def tag_edge(self, tail, head, name, value=True):
        """Set a tag of a edge with a freely selectable value.
        
        If the tag already exists it will be overwritten.
        Raises NodeMissing if the given edge does not exist.
        
        :param tail: Tail of the edge to tag.
        :param head: Head of the edge to tag.
        :param name: The name of the tag.
        :param value: The value to set the tag to, default to True.
        """
        if not self.edge_exists(tail, head):
            raise self.EdgeMissing('No edge ({}, {}).'.format(tail, head))
        self._edges[(tail, head)][name] = value

    def untag_edge(self, tail, head, name):
        """Remove a tag from an edge.
        
        :param tail: ID of tail.
        :param head: ID of head.
        :param name: Name of the tag. 
        """
        if not self.edge_exists(tail, head):
            raise self.EdgeMissing('No edge ({}, {}).'.format(tail, head))
        # TODO see untag_node
        del (self._edges[(tail, head)][name])

    def edge_tag(self, tail, head, name):
        """Get the value of an edge tag.
        
        Raises EdgeMissing if the given edge does not exist.
        Raises EdgeTagMissing if the given tag does not exist.
        
        :param tail: Tail of edge.
        :param head: Head of edge. 
        :param name: Name of tag. 
        :return: Value of tag. 
        """
        if not self.edge_exists(tail, head):
            raise self.EdgeMissing('No edge ({}, {}).'.format(tail, head))
        if name not in self._edges[(tail, head)]:
            raise self.EdgeTagMissing(
                'No tag {} in edge ({}, {}).'.format(name, tail, head))
        return self._edges[(tail, head)][name]

    @property
    def nodes(self):
        """Get a list of all nodes."""
        return list(self._nodes.keys())

    @property
    def edges(self):
        """Get a list of all edges."""
        return list(self._edges.keys())

    def predecessors(self, id):
        """Return incoming nodes of ID.
        
        :param id: ID of node.
        :return: Set of ID's.
        """
        return self._heads[id]

    def successors(self, id):
        """Return outgoing nodes of ID.
        
        :param id: ID of node.
        :return: Set of ID's.
        """
        return self._tails[id]

    def incoming(self, id):
        """Return incoming edges of ID.
        
        :param id: ID of node.
        :return: Set of ID pairs (tail, head).
        """
        edges = set()
        for node in self._heads[id]:
            edges.add((node, id))
        return edges

    def outgoing(self, id):
        """Return outgoing edges of ID.
        
        :param id: ID of node.
        :return: Set of ID pairs (tail, head).
        """
        edges = set()
        for node in self._tails[id]:
            edges.add((id, node))
        return edges

    def count_of_nodes(self):
        """Return the count of all nodes.
        
        :return: Count of nodes. 
        """
        return len(self._nodes)

    def count_of_edges(self):
        """Return the count of all edges.
        
        :return: Count of nodes. 
        """
        return len(self._edges)

