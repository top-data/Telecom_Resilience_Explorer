import time
from networkx import DiGraph
from .graph_utils import downstream_nodes

def simulate_failure(G: DiGraph, topology, failure_type: str, impact: str, duration_hours: int):
    """Simulate failures. Returns (failed_nodes_list, timeline)

    Simple model:
    - Choose initial seeds based on impact (Local -> 1 random, Regional -> 2-3, National -> 4+)
    - Propagate to downstream dependencies with a time step
    """
    import random

    sites = [n for n in G.nodes]
    if impact == "Local":
        seeds = random.sample(sites, 1)
    elif impact == "Regional":
        seeds = random.sample(sites, min(3, max(2, len(sites)//4)))
    else:
        seeds = random.sample(sites, min(6, max(4, len(sites)//3)))

    failed = set()
    timeline = []
    step = max(1, duration_hours // 6)
    t = 0
    queue = list(seeds)
    for s in seeds:
        failed.add(s)
        timeline.append({"time": t, "node": s, "event": "failed", "type": failure_type})

    while queue and t < duration_hours:
        current = queue.pop(0)
        t += step
        for dn in downstream_nodes(G, current):
            if dn not in failed and random.random() < 0.6:
                failed.add(dn)
                queue.append(dn)
                timeline.append({"time": t, "node": dn, "event": "failed", "type": failure_type})
        # small delay to simulate compute (not necessary)
        time.sleep(0.01)

    return list(failed), timeline
