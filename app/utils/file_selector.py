# app/utils/file_selector.py

import os

# Mapping device types to corresponding CSV filenames and additional metadata
device_mapping = {
    "001_clothes-dryers": {
        "filename": "001_clothes-dryers.csv",
        "description": "Clothes Dryer",
        "additional_info": "Additional metadata if needed",
        "field_mapping": {
            "MODEL_NUM": "MODEL_NUM_1",
            "BRAND": "BRAND_NAME",
            "AEC": "AEC",
            "EF": "EF",
        }
    },
    "002_clothes-washer-dryers": {
        "filename": "002_clothes-washer-dryers.csv",
        "description": "Clothes Washer Dryers",
        "additional_info": "Additional metadata if needed",
         "field_mapping": {
            "MODEL_NUM": "MODEL_NUM_1",
            "BRAND": "BRAND_NAME",
            "AEC": "MOD_J1_AEC",
            "DRYER_AEC": "DRYER_AEC",
        }
    },
    "004_cooktops": {
        "filename": "004_cooktops.csv",
        "description": "Cooktops",
        "additional_info": "Additional metadata if needed",
         "field_mapping": {
            "MODEL_NUM": "MODEL_NUM_1",
            "BRAND": "BRAND_NAME",
            "AEC": "AEC_03",
        }
    },
    "005_dishwashers": {
        "filename": "005_dishwashers.csv",
        "description": "Dishwashers",
        "additional_info": "Additional metadata if needed",
         "field_mapping": {
            "MODEL_NUM": "MODEL_NUM_1",
            "BRAND": "BRAND_NAME",
            "AEC": "TAEC_C373_04",
        }
    },
    "006_freezers": {
        "filename": "006_freezers.csv",
        "description": "Freezers",
        "additional_info": "Additional metadata if needed",
        "field_mapping": {
            "MODEL_NUM": "MODEL_NUM_1",
            "BRAND": "BRAND_NAME",
            "AEC": "AEC",
        }
    },
}


CSV_DIRECTORY = os.path.join(os.path.dirname(__file__), "../csv_files")

def select_csv_file(device_type: str) -> str:
    # Get the mapping entry based on the device type
    mapping_entry = device_mapping.get(device_type)
    
    if not mapping_entry:
        raise ValueError(f"No mapping found for device type: {device_type}")
    
    # Construct the full path to the CSV file and resolve it to an absolute path
    csv_file_path = os.path.abspath(os.path.join(CSV_DIRECTORY, mapping_entry["filename"]))
    
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file does not exist: {csv_file_path}")
    
    return csv_file_path

def get_device_metadata(device_type: str) -> dict:
    # Retrieve metadata for the given device type
    mapping_entry = device_mapping.get(device_type)
    
    if not mapping_entry:
        raise ValueError(f"No metadata found for device type: {device_type}")
    
    return mapping_entry