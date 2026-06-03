def build_airport_graph(airports_df):
    import networkx as nx
    import pandas as pd

    G = nx.Graph()

    for _, row in airports_df.iterrows():
        iata = row["iata_code"]
        if not iata or pd.isna(iata):
            continue

        G.add_node(iata, 
                   name=row["name"],
                   municipality=row.get("municipality", ""),
                   country=row.get("country_name", ""),
                   lat=row["latitude_deg"],
                   lon=row["longitude_deg"])

    print(f"✅ Graph created with {G.number_of_nodes()} airport nodes.")
    return G
