import random
import json

def split_lane_into_parts(lane, num_points):
    # split lane to smaller lanes for monthly
    total_points = len(lane)
    part_size = total_points // num_points
    parts = []

    for i in range(num_points):
        start = i * part_size

        # Last part gets remaining points
        end = (i + 1) * part_size if i < num_points - 1 else total_points
        part = lane[start:end]
        if len(part) >= 2:
            parts.append(part)
    return parts

def fragment_all_lanes(lanes, max_points=24):
    fragmented_lanes = []
    for lane in lanes:
        if len(lane) <= max_points:
            fragmented_lanes.append(lane)
            continue

        fragments = split_lane_into_parts(lane, max_points)
        fragmented_lanes.extend(fragments)
    return fragmented_lanes

with open("lanes-data.geojson") as f:
    lanes_raw = json.load(f)

# conv input to {"coordinates": [[[lon, lat], [lon, lat], ...], ...]}
original_lanes = (lanes_raw.get("features")[0])["geometry"]["coordinates"]

fragmented = fragment_all_lanes(original_lanes, max_points=24)

with open("data/fragmented_shipping_lanes.json", "w") as f:
    json.dump({"coordinates": fragmented}, f, indent=2)

print(f"Fragmented {len(original_lanes)} lanes into {len(fragmented)} sub-lanes.")
