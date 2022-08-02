"""Create hash strings for structure graphs.

Note that two LQGs of the same net (crystallographic net)
cannot have non-isomorphic unlabeled quotient graphs.
Hence, computing a hash of the Weisfeiler-Lehman canonical form
of the UQG will yield always lead to too many duplicates, not too few.
"""
import networkx as nx
from pymatgen.analysis.graphs import StructureGraph

from ._hasher import weisfeiler_lehman_graph_hash
from .create import construct_clean_graph
from .delete import get_structure_graph_with_broken_bridges, get_structure_graph_without_leaf_nodes


def generate_hash(g: nx.Graph, node_decorated: bool, edge_decorated: bool, iterations: int) -> str:
    """Run the Weisfeiler-Lehman algorithm on the graph.

    Args:
        g (nx.Graph): Graph to hash
        node_decorated (bool): If True, decorate the nodes with the species.
        edge_decorated (bool): If True, decorate the edges with the image tuples
        iterations (int): Number of iterations to run the algorithm.

    Returns:
        str: Hash string for the graph.
    """
    edge_attr = None
    node_attr = None
    if node_decorated:
        node_attr = "specie"
    if edge_decorated:
        edge_attr = "voltage"
    return weisfeiler_lehman_graph_hash(
        g, iterations=iterations, edge_attr=edge_attr, node_attr=node_attr
    )


def undecorated_graph_hash(structure_graph: StructureGraph, lqg: bool = True) -> str:
    """Create a undecorated hash string for a StructureGraph.

    Undecorated means that the hash is  based on the structure graph,
    but ignoring the atomic species.

    Args:
        structure_graph (StructureGraph): pymatgen StructureGraph
        lqg (bool): If True, computed the hash on the labeled quotient graph.
            Otherwise, computed the hash on the undirected quotient graph.

    Returns:
        str: Hash string for the StructureGraph.
    """
    if lqg:
        g = construct_clean_graph(structure_graph, multigraph=True, directed=True)
    else:
        g = construct_clean_graph(structure_graph)

    edge_decorated = True if lqg else False
    node_decorated = False
    return generate_hash(g, node_decorated, edge_decorated, iterations=6)


def decorated_graph_hash(structure_graph: StructureGraph, lqg: bool = True) -> str:
    """Create a decorated hash string for a StructureGraph.

    Decorated means that the hash is based on the structure graph,
    and the atomic species.

    Args:
        structure_graph (StructureGraph): pymatgen StructureGraph
        lqg (bool): If True, computed the hash on the labeled quotient graph.
            Otherwise, computed the hash on the undirected quotient graph.

    Returns:
        str: Hash string for the StructureGraph.
    """
    if lqg:
        g = construct_clean_graph(structure_graph, multigraph=True, directed=True)
    else:
        g = construct_clean_graph(structure_graph)
    edge_decorated = True if lqg else False
    node_decorated = True
    return generate_hash(g, node_decorated, edge_decorated, iterations=6)


def undecorated_no_leaf_hash(structure_graph: StructureGraph, lqg: bool = True) -> str:
    """Create a undecorated no-leaf hash string for a StructureGraph.

    Undecorated means that the hash is  based on the structure graph,
    but ignoring the atomic species.
    No-leaf means that leaf nodes are not included in the hash computation.

    Args:
        structure_graph (StructureGraph): pymatgen StructureGraph
        lqg (bool): If True, computed the hash on the labeled quotient graph.
            Otherwise, computed the hash on the undirected quotient graph.

    Returns:
        str: Hash string for the StructureGraph.
    """
    sg, _ = get_structure_graph_without_leaf_nodes(structure_graph)
    if lqg:
        g = construct_clean_graph(sg, multigraph=True, directed=True)
    else:
        g = construct_clean_graph(sg)
    edge_decorated = True if lqg else False
    node_decorated = False
    return generate_hash(g, node_decorated, edge_decorated, iterations=6)


def decorated_no_leaf_hash(structure_graph: StructureGraph, lqg: bool = True) -> str:
    """Create a undecorated no-leaf hash string for a StructureGraph.

    Decorated means that the hash is based on the structure graph,
    amd the atomic species.
    No-leaf means that leaf nodes are not included in the hash computation.

    Args:
        structure_graph (StructureGraph): pymatgen StructureGraph
        lqg (bool): If True, computed the hash on the labeled quotient graph.
            Otherwise, computed the hash on the undirected quotient graph.

    Returns:
        str: Hash string for the StructureGraph.
    """
    sg, _ = get_structure_graph_without_leaf_nodes(structure_graph)
    if lqg:
        g = construct_clean_graph(sg, multigraph=True, directed=True)
    else:
        g = construct_clean_graph(sg)
    edge_decorated = True if lqg else False
    node_decorated = True
    return generate_hash(g, node_decorated, edge_decorated, iterations=6)


def undecorated_scaffold_hash(structure_graph: StructureGraph, lqg: bool = True) -> str:
    """Create a undecorated scaffold hash string for a StructureGraph.

    Undecorated means that the hash is based on the structure graph,
    but ignoring the atomic species.
    Scaffold means that the subgraphs that are connected via a bridge to the main
    framenwork are not included in the hash computation.

    Args:
        structure_graph (StructureGraph): pymatgen StructureGraph
        lqg (bool): If True, computed the hash on the labeled quotient graph.
            Otherwise, computed the hash on the undirected quotient graph.

    Returns:
        str: Hash string for the StructureGraph.
    """
    sg, _ = get_structure_graph_with_broken_bridges(structure_graph)
    if lqg:
        g = construct_clean_graph(sg, multigraph=True, directed=True)
    else:
        g = construct_clean_graph(sg)
    edge_decorated = True if lqg else False
    node_decorated = False
    return generate_hash(g, node_decorated, edge_decorated, iterations=6)


def decorated_scaffold_hash(structure_graph: StructureGraph, lqg: bool = True) -> str:
    """Create a decorated scaffold hash string for a StructureGraph.

    Decorated means that the hash is based on the structure graph,
    and the atomic species.
    Scaffold means that the subgraphs that are connected via a bridge to the main
    framenwork are not included in the hash computation.

    Args:
        structure_graph (StructureGraph): pymatgen StructureGraph
        lqg (bool): If True, computed the hash on the labeled quotient graph.
            Otherwise, computed the hash on the undirected quotient graph.

    Returns:
        str: Hash string for the StructureGraph.
    """
    sg, _ = get_structure_graph_with_broken_bridges(structure_graph)
    if lqg:
        g = construct_clean_graph(sg, multigraph=True, directed=True)
    else:
        g = construct_clean_graph(sg)
    edge_decorated = True if lqg else False
    node_decorated = True
    return generate_hash(g, node_decorated, edge_decorated, iterations=6)
