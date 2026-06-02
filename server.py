from flask import Flask, request, jsonify
import json
from collections import defaultdict

app = Flask(__name__)

def create_polygon_feature(coords, original_type):
    if coords[0] != coords[-1]:
        coords = coords + [coords[0]]
    return {
        "type": "Feature",
        "properties": {"type": original_type},
        "geometry": {"type": "Polygon", "coordinates": [coords]}
    }

def create_boundary_feature(all_polygons_coords):
    if not all_polygons_coords:
        return None
    all_points = []
    for poly in all_polygons_coords:
        all_points.extend(poly)
    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    bbox = [
        [min_x, min_y], [max_x, min_y],
        [max_x, max_y], [min_x, max_y], [min_x, min_y]
    ]
    return {
        "type": "Feature",
        "properties": {"class": "boundaries"},
        "geometry": {"type": "Polygon", "coordinates": [bbox]}
    }

def build_output(islands):
    features = []
    all_polygons_coords = []
    for typ, polygons in islands.items():
        for poly_coords in polygons:
            features.append(create_polygon_feature(poly_coords, typ))
            all_polygons_coords.append(poly_coords)
    boundary = create_boundary_feature(all_polygons_coords)
    if boundary:
        features.append(boundary)
    return {"type": "FeatureCollection", "features": features}

def process_geojson(feature_collection):

    data = feature_collection

    lines_by_type = defaultdict(list)
    for item in data["features"]:
        if item["geometry"]["type"] == "LineString":
            lines_by_type[item["properties"]["type"]].append(item["geometry"]["coordinates"])

    islands = defaultdict(list)

    for type_of_lines, lines in lines_by_type.items():
        processed = set()
        for i, line in enumerate(lines):
            if i in processed:
                continue

            begin = tuple(line[0])
            end = tuple(line[-1])

            if begin == end:
                path = [coord for coord in line]
                islands[type_of_lines].append(path)
                processed.add(i)
                continue

            path = [coord for coord in line]
            processed.add(i)
            used_lines = {i}
            current_end = end
            finished = False

            while not finished:
                found = False
                for idx, edge in enumerate(lines):
                    if idx in used_lines:
                        continue
                    b = tuple(edge[0])
                    e = tuple(edge[-1])
                    if b == current_end:
                        path.extend(edge[1:])
                        if begin == e:
                            finished = True
                        used_lines.add(idx)
                        current_end = e
                        found = True
                        break
                    elif e == current_end:
                        path.extend(reversed(edge[:-1]))
                        if begin == b:
                            finished = True
                        used_lines.add(idx)
                        current_end = b
                        found = True
                        break
                if not found:
                    break

            if finished:
                processed.update(used_lines)
                islands[type_of_lines].append(path)

    output = build_output(islands)
    return output

@app.route('/process', methods=['POST'])
def process():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()
    try:
        result = process_geojson(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)