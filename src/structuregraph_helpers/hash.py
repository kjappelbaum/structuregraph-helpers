"""Create hash strings for structure graphs."""
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash
import networkx as nx


def generate_hash(g: nx.Graph, node_decorated: bool, edge_decorated: bool, iterations: int) -> str:
    return weisfeiler_lehman_graph_hash(g, iterations=6)


def undecorated_graph_hash():
    ...


def decorated_graph_hash():
    ...


def undecorated_scaffold_hash():
    ...


def decorated_scaffold_hash():
    ...
