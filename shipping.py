import json
from datetime import datetime
import os

def get_deterministic_lane(fragmented_lanes, year, month):
    # deterministically find lane
    total_lanes = len(fragmented_lanes)

    # based on the year and month
    lane_index = (year + month) % total_lanes
    return fragmented_lanes[lane_index]

def load_fragmented_lanes(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data.get("coordinates", [])

def save_selected_lane(file_path, selected_lane):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump({"coordinates": selected_lane}, f, indent=2)

def main():
    fragmented_lanes = load_fragmented_lanes("fragmented-utils/data/fragmented_shipping_lanes.json")

    # for sample testing
    now = datetime.now()
    year = now.year
    month = now.month

    selected_lane = get_deterministic_lane(fragmented_lanes, year, month)

    save_selected_lane("data/monthly_shipping_lane.json", selected_lane)

    print(f"Selected lane for {year}-{month:02d} with {len(selected_lane)} points.")

if __name__ == "__main__":
    main()