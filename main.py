# from src.data_loader import load_airport_data
# from src.graph_builder import build_airport_graph

# if __name__ == "__main__":
#     airports_df = load_airport_data()
#     G = build_airport_graph(airports_df)

#     print("✈️ Sample airport nodes:")
#     sample_nodes = list(G.nodes(data=True))[:5]
#     for node, attr in sample_nodes:
#         print(node, attr)


# from src.data_loader import load_airport_data
# from src.graph_builder import build_airport_graph
# from src.route_loader import load_and_add_routes


# if __name__ == "__main__":
#     airports_df = load_airport_data()
#     print("✅ Loaded airport data")

#     G = build_airport_graph(airports_df)
    
#     print(f"📊 Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

#     sample_nodes = list(G.nodes(data=True))[:5]
#     print("✈️ Sample airport nodes (with attributes):")
#     for node, attrs in sample_nodes:
#         print(f"🛫 {node}: {attrs}")
#     routes_file = "data/routes.csv"  
#     load_and_add_routes(G, routes_file)

#     print(f"📊 Final graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")


from src.data_loader import load_airport_data
from src.graph_builder import build_airport_graph
from src.route_loader import load_routes_data, add_edges_to_graph

if __name__ == "__main__":
    airports_df = load_airport_data()
    print("✅ Loaded airport data")

    G = build_airport_graph(airports_df)
    print("✅ Graph built!")

    routes_df = load_routes_data()
    G = add_edges_to_graph(G, routes_df)

    print(f"📊 Final graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    sample_nodes = list(G.nodes(data=True))[:5]
    print("✈️ Sample airport nodes:")
    for node, attrs in sample_nodes:
        print(f"🛫 {node}: {attrs}")
