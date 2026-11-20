"""Load the OpenFlights route table and add it to the airport graph.

Note on modelling: routes are recorded as directed pairs, but this project
treats the network as undirected. In scheduled commercial aviation the
overwhelming majority of segments are flown in both directions, and the
questions this project is aimed at (reachability, segment counts, distance)
are symmetric. Anything schedule-dependent would need the directed graph.
"""

from __future__ import annotations

import networkx as nx
import pandas as pd

ROUTE_COLUMNS = [
    "airline", "airline_id",
    "source_airport", "source_airport_id",
    "destination_airport", "destination_airport_id",
    "codeshare", "stops", "equipment",
]


def load_routes_data(filepath: str = "data/routes.csv") -> pd.DataFrame:
    routes = pd.read_csv(filepath, header=None, names=ROUTE_COLUMNS)
    routes = routes.dropna(subset=["source_airport", "destination_airport"])
    return routes


def add_edges_to_graph(G: nx.Graph, routes_df: pd.DataFrame) -> nx.Graph:
    """Add every route whose endpoints are both present as nodes."""
    pairs = zip(
        routes_df["source_airport"].to_numpy(),
        routes_df["destination_airport"].to_numpy(),
    )
    added = skipped = 0
    for src, dst in pairs:
        if src != dst and src in G and dst in G:
            if not G.has_edge(src, dst):
                G.add_edge(src, dst)
            added += 1
        else:
            skipped += 1
    print(f"   {added} route records matched, {skipped} skipped (unknown airport)")
    return G
