import random
import json

def split_lane_into_parts(lane, num_parts):
    # split lane to smaller lanes for monthly
    total_points = len(lane)
    part_size = total_points // num_parts
    parts = []

    for i in range(num_parts):
        start = i * part_size
        # Last part gets all remaining points
        end = (i + 1) * part_size if i < num_parts - 1 else total_points
        part = lane[start:end]
        if len(part) >= 2:
            parts.append(part)
    return parts

def fragment_all_lanes(lanes):
    fragmented_lanes = []
    for lane in lanes:
        if len(lane) < 4:
            fragmented_lanes.append(lane)
            continue

        num_parts = random.choice([2, 3])
        fragments = split_lane_into_parts(lane, num_parts)
        fragmented_lanes.extend(fragments)
    return fragmented_lanes

with open("lanes-data.geojson") as f:
    lanes_raw = json.load(f)

# conv input to {"coordinates": [[[lon, lat], [lon, lat], ...], ...]}
original_lanes = (lanes_raw.get("features")[0])["geometry"]["coordinates"]

fragmented = fragment_all_lanes(original_lanes)

with open("data/fragmented_shipping_lanes.json", "w") as f:
    json.dump({"coordinates": fragmented}, f, indent=2)

print(f"Fragmented {len(original_lanes)} lanes into {len(fragmented)} sub-lanes.")
