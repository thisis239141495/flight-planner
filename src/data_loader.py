"""Load the OurAirports reference tables and keep the commercially useful rows."""

from __future__ import annotations

import os

import pandas as pd


def load_airport_data(data_dir: str = "data") -> pd.DataFrame:
    airports = pd.read_csv(os.path.join(data_dir, "airports.csv"))

    countries = pd.read_csv(os.path.join(data_dir, "countries.csv"))[["code", "name"]]
    countries.columns = ["iso_country", "country_name"]
    airports = airports.merge(countries, on="iso_country", how="left")

    regions_path = os.path.join(data_dir, "regions.csv")
    if os.path.exists(regions_path):
        regions = pd.read_csv(regions_path)[["code", "name"]]
        regions.columns = ["iso_region", "region_name"]
        airports = airports.merge(regions, on="iso_region", how="left")

    # Only airports with an IATA code appear in the route table.
    airports = airports[airports["iata_code"].notnull()]
    airports = airports[airports["iata_code"] != ""]
    airports = airports.dropna(subset=["latitude_deg", "longitude_deg"])
    return airports.copy()
