import pandas as pd
import networkx as nx

# def load_routes_data(filepath="data/routes.dat"):
#     cols = [
#         "airline", "airline_id", "source_airport", "source_airport_id",
#         "destination_airport", "destination_airport_id", "codeshare",
#         "stops", "equipment"
#     ]
#     routes = pd.read_csv(filepath, header=None, names=cols)
    
#     routes = routes.dropna(subset=["source_airport", "destination_airport"])
#     return routes
def load_routes_data(filepath="data/routes.csv"):
    cols = [
        "airline", "airline_id",
        "source_airport", "source_airport_id",
        "destination_airport", "destination_airport_id",
        "codeshare", "stops", "equipment"
    ]
    routes = pd.read_csv(filepath, header=None, names=cols)
    routes = routes.dropna(subset=["source_airport", "destination_airport"])
    print("🛬 Sample routes:")
    print(routes.head(10))
    return routes


def add_edges_to_graph(G: nx.Graph, routes_df: pd.DataFrame):
    added_edges = 0
    missing_nodes = 0
    for _, row in routes_df.iterrows():
        src = row["source_airport"]
        dst = row["destination_airport"]

        if src in G and dst in G and src != dst:
            G.add_edge(src, dst)
            added_edges += 1
        else:
            missing_nodes += 1

    print(f"✅ Added {added_edges} edges (routes) to the graph.")
    print(f"⚠️ Skipped {missing_nodes} routes due to missing nodes.")

    if src not in G:
     print(f"⚠️ Source {src} not in graph.")
    if dst not in G:
     print(f"⚠️ Destination {dst} not in graph.")

    return G
