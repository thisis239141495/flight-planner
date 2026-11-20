"""Command line entry point for the global flight route planner.

    python main.py --from PEK --to BNA
    python main.py --from LHR --to SYD --metric hops --k 3
    python main.py --summary
    python main.py --serve
"""

from __future__ import annotations

import argparse
import sys

import networkx as nx

from src.data_loader import load_airport_data
from src.graph_builder import build_airport_graph
from src.path_finder import find_routes, network_summary
from src.route_loader import add_edges_to_graph, load_routes_data


def build_network(verbose: bool = True) -> nx.Graph:
    """Load the data files and return the airport network."""
    if verbose:
        print("Loading airports...")
    airports = load_airport_data()
    G = build_airport_graph(airports)
    if verbose:
        print(f"   {G.number_of_nodes()} airports with an IATA code")
        print("Loading routes...")
    G = add_edges_to_graph(G, load_routes_data())
    if verbose:
        print(f"   network: {G.number_of_nodes()} airports, {G.number_of_edges()} routes")
    return G


def print_routes(routes: list[dict]) -> None:
    for i, route in enumerate(routes, start=1):
        head = " -> ".join(route["path"])
        print(f"\n{i}. {head}")
        print(f"   {route['segments']} segment(s), {route['total_km']:,.0f} km")
        for leg in route["legs"]:
            print(f"     {leg['from']} -> {leg['to']}  {leg['km']:>8,.0f} km")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from", dest="origin", help="origin IATA code, e.g. PEK")
    parser.add_argument("--to", dest="destination", help="destination IATA code, e.g. BNA")
    parser.add_argument("--metric", default="distance", choices=["distance", "hops"],
                        help="what to minimise (default: distance)")
    parser.add_argument("--k", type=int, default=1, help="how many itineraries to return")
    parser.add_argument("--summary", action="store_true",
                        help="print descriptive statistics about the network")
    parser.add_argument("--serve", action="store_true", help="run the web interface")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)

    if args.serve:
        from src.server import serve
        serve(build_network(), port=args.port)
        return 0

    G = build_network()

    if args.summary:
        print()
        for key, value in network_summary(G).items():
            print(f"{key:>20}: {value}")
        return 0

    if not args.origin or not args.destination:
        parser.error("give both --from and --to, or use --summary / --serve")

    try:
        routes = find_routes(G, args.origin, args.destination,
                             metric=args.metric, k=args.k)
    except KeyError as exc:
        print(f"\nerror: {exc}", file=sys.stderr)
        return 1
    except nx.NetworkXNoPath:
        print(f"\nNo route connects {args.origin.upper()} and "
              f"{args.destination.upper()} in this network.", file=sys.stderr)
        return 1

    print_routes(routes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
