# app/utils/csv_helpers.py

import csv

def load_csv_data(file_path: str):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def get_unique_brands(data):
    brands = {row["BRAND_NAME"] for row in data}
    return list(brands)
