import networkx as nx

def build_graph_from_topology(topology):
    G = nx.DiGraph()
    for node in topology:
        site = node.get("site")
        G.add_node(site, **node)
    # Add edges from dependencies
    for node in topology:
        src = node.get("site")
        for dep in node.get("dependencies", []):
            if G.has_node(dep):
                G.add_edge(src, dep)
    return G

def downstream_nodes(G, start_node):
    # return nodes reachable from start_node following edges
    if start_node not in G:
        return []
    return list(nx.descendants(G, start_node))
