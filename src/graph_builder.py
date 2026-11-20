"""Build the airport graph: one node per airport with an IATA code."""

from __future__ import annotations

import networkx as nx
import pandas as pd


def build_airport_graph(airports_df: pd.DataFrame) -> nx.Graph:
    G = nx.Graph()
    for row in airports_df.itertuples(index=False):
        iata = getattr(row, "iata_code", None)
        if not iata or pd.isna(iata):
            continue
        G.add_node(
            iata,
            name=getattr(row, "name", ""),
            municipality=getattr(row, "municipality", "") or "",
            country=getattr(row, "country_name", "") or "",
            lat=float(row.latitude_deg),
            lon=float(row.longitude_deg),
        )
    return G
