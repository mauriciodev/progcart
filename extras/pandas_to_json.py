#!/usr/bin/env python3

import geopandas as gpd
import pandas as pd
import zipfile
import tempfile
import os
import json
import argparse
import fiona

def extract_shapefiles(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    shapefiles = [
        os.path.join(root, file)
        for root, _, files in os.walk(extract_to)
        for file in files if file.endswith(".shp")
    ]

    return shapefiles

def convert_to_generic_gdf(shapefile_path, zip_name):
    gdf = gpd.read_file(shapefile_path)

    # Convert all non-geometry attributes to JSON
    json_props = gdf.drop(columns=gdf.geometry.name).apply(
        lambda row: json.dumps(row.dropna().to_dict()), axis=1
    )

    # Add source info
    gdf_out = gpd.GeoDataFrame({
        'geometry': gdf.geometry,
        'properties': json_props,
        'filename': os.path.basename(shapefile_path),
        'zipfilename': os.path.basename(zip_name)
    }, crs=gdf.crs)

    return gdf_out

def layer_exists(gpkg_path, layer_name):
    if not os.path.exists(gpkg_path):
        return False
    return layer_name in fiona.listlayers(gpkg_path)

def main():
    parser = argparse.ArgumentParser(description="Merge multiple zipped shapefiles into a single GPKG layer.")
    parser.add_argument("output_gpkg", help="Output GeoPackage file")
    parser.add_argument("zips", nargs="+", help="Input ZIP files containing shapefiles")
    parser.add_argument("--layer", default="merged_layer", help="Name of the output layer (default: merged_layer)")

    args = parser.parse_args()

    all_features = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for zip_file in args.zips:
            print(f"Processing: {zip_file}")
            shapefiles = extract_shapefiles(zip_file, tmpdir)
            if not shapefiles:
                print(f"Warning: No shapefiles found in {zip_file}")
                continue
            for shp in shapefiles:
                gdf = convert_to_generic_gdf(shp, zip_file)
                all_features.append(gdf)

    if not all_features:
        print("No valid shapefiles were found in the provided ZIP files.")
        return

    # Concatenate all GeoDataFrames
    common_crs = all_features[0].crs
    merged_gdf = gpd.GeoDataFrame(pd.concat(
        [gdf.to_crs(common_crs) for gdf in all_features],
        ignore_index=True
    ), crs=common_crs)

    # Determine mode: append or write
    mode = "a" if layer_exists(args.output_gpkg, args.layer) else "w"

    # Write to GeoPackage
    merged_gdf.to_file(args.output_gpkg, layer=args.layer, driver="GPKG", mode=mode)

    print(f"Saved {len(merged_gdf)} features to '{args.output_gpkg}' in layer '{args.layer}' (mode={mode}).")

if __name__ == "__main__":
    main()
