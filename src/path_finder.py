"""Shortest-path search over the global airport network.

Two metrics are supported:

``hops``
    Minimise the number of flight segments. Every edge has unit cost.
``distance``
    Minimise total great-circle distance. Every edge is weighted by the
    distance between the two airports it connects.

The two disagree often enough to be interesting: the fewest-segment
itinerary is frequently far from the shortest one in kilometres.
"""

from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

import networkx as nx

EARTH_RADIUS_KM = 6371.0


def great_circle_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres between two lat/lon points."""
    phi1, phi2 = radians(lat1), radians(lat2)
    d_phi = phi2 - phi1
    d_lambda = radians(lon2 - lon1)
    h = sin(d_phi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(d_lambda / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(h))


def annotate_distances(G: nx.Graph) -> nx.Graph:
    """Attach a ``km`` attribute to every edge, in place."""
    for u, v, data in G.edges(data=True):
        if "km" in data:
            continue
        data["km"] = great_circle_km(
            G.nodes[u]["lat"], G.nodes[u]["lon"],
            G.nodes[v]["lat"], G.nodes[v]["lon"],
        )
    return G


def _edge_weight(metric: str):
    if metric == "hops":
        return None
    if metric == "distance":
        return "km"
    raise ValueError(f"unknown metric {metric!r}; expected 'hops' or 'distance'")


def describe_path(G: nx.Graph, path: list[str]) -> dict:
    """Summarise an itinerary: its airports, segment count and total km."""
    legs = []
    total_km = 0.0
    for u, v in zip(path, path[1:]):
        km = G.edges[u, v].get("km")
        if km is None:
            km = great_circle_km(
                G.nodes[u]["lat"], G.nodes[u]["lon"],
                G.nodes[v]["lat"], G.nodes[v]["lon"],
            )
        total_km += km
        legs.append({"from": u, "to": v, "km": round(km, 1)})
    return {
        "path": path,
        "airports": [
            {
                "iata": code,
                "name": G.nodes[code].get("name", ""),
                "municipality": G.nodes[code].get("municipality", ""),
                "country": G.nodes[code].get("country", ""),
                "lat": G.nodes[code]["lat"],
                "lon": G.nodes[code]["lon"],
            }
            for code in path
        ],
        "segments": len(path) - 1,
        "total_km": round(total_km, 1),
        "legs": legs,
    }


def find_routes(G: nx.Graph, origin: str, destination: str,
                metric: str = "distance", k: int = 1) -> list[dict]:
    """Return the ``k`` best itineraries from ``origin`` to ``destination``.

    Raises ``KeyError`` if either airport is absent from the network and
    ``networkx.NetworkXNoPath`` if the two are not connected.
    """
    origin, destination = origin.upper(), destination.upper()
    for code in (origin, destination):
        if code not in G:
            raise KeyError(f"{code} is not an airport in this network")
    if origin == destination:
        return [describe_path(G, [origin])]

    weight = _edge_weight(metric)
    if weight is not None:
        annotate_distances(G)

    routes = []
    for path in nx.shortest_simple_paths(G, origin, destination, weight=weight):
        routes.append(describe_path(G, path))
        if len(routes) >= k:
            break
    return routes


def network_summary(G: nx.Graph) -> dict:
    """A few descriptive numbers about the network, for the README and the UI."""
    degrees = [d for _, d in G.degree()]
    components = list(nx.connected_components(G))
    largest = max(components, key=len)
    return {
        "airports": G.number_of_nodes(),
        "routes": G.number_of_edges(),
        "mean_degree": round(sum(degrees) / len(degrees), 2) if degrees else 0.0,
        "max_degree": max(degrees) if degrees else 0,
        "components": len(components),
        "largest_component": len(largest),
    }
