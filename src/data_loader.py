import pandas as pd
import os

def load_airport_data(data_dir="data"):
    airports_path = os.path.join(data_dir, "airports.csv")
    countries_path = os.path.join(data_dir, "countries.csv")
    regions_path = os.path.join(data_dir, "regions.csv")

    airports = pd.read_csv(airports_path)
    print(f"✅ Loaded {len(airports)} airports")

    countries = pd.read_csv(countries_path)[["code", "name"]]
    countries.columns = ["iso_country", "country_name"]
    airports = airports.merge(countries, on="iso_country", how="left")

    if os.path.exists(regions_path):
        regions = pd.read_csv(regions_path)[["code", "name"]]
        regions.columns = ["iso_region", "region_name"]
        airports = airports.merge(regions, on="iso_region", how="left")

    airports = airports[airports["iata_code"].notnull()].copy()
    airports = airports[airports["iata_code"] != ""]
    print(f"✅ Filtered {len(airports)} airports with valid IATA codes")

    return airports

if __name__ == "__main__":
    df = load_airport_data()
    print(df.head())
