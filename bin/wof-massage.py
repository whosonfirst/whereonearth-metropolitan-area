#!/usr/bin/env python

"""
Massage standard whereonearth- feature collection documents in to Who's On First style documents
"""

import sys
import os
import json
import csv
import shapely.geometry

source = "data"

out = open("meta.csv", "w")
writer = csv.DictWriter(out, fieldnames=("id", "path"))
writer.writeheader()

for (root, dirs, files) in os.walk(source):

    for f in files:
        path = os.path.join(root, f)
        path = os.path.abspath(path)

        if path.endswith("~"):
            continue

        fh = open(path, "r")
        data = json.load(fh)
        fh.close()

        data = data['features'][0]
        id = data['id']

        shp = shapely.geometry.asShape(data['geometry'])
        bbox = list(shp.bounds)

        data['bbox'] = bbox
        data['type'] = 'Feature'

        data['properties']['name'] = data['id']

        fh = open(path, "w")
        json.dump(data, fh, indent=2)
        fh.close()

        if not path.endswith(".geojson"):
            ignore, ext = os.path.splitext(path)
            new = path.replace(ext, ".geojson")
            os.rename(path, new)
            path = new

        rel_path = path.replace("/usr/local/mapzen/whereonearth-metropolitan-area/data/", "")
        print rel_path

        writer.writerow({'id':id, 'path': rel_path})
