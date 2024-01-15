import pandas as pd
import os
import geopandas as gpd
from .utils.calculation import polygon_to_point, point_error_distance

current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
gdf_database_ch_modern = os.path.join(current_directory, 'data/Modern', '2020China.geojson')
gdf_database_ch_historic = os.path.join(current_directory, 'data/Historic', 'v6_time_cnty_pts_gbk_wgs84.csv')

def calculate_point(data, geographic_crs, lang, preferences, if_certainty):
    if lang == "ch":
        for preference in preferences:
            if preference == "modern":
                print("Calculating modern location references...")
                gdf_database = gpd.read_file(gdf_database_ch_modern, driver="GeoJSON")
                data = polygon_to_point.get_point_from_address(data, geographic_crs, gdf_database, lang, if_certainty)
            if preference == "historic":
                print("Calculating historic location references...")
                df_database = pd.read_csv(gdf_database_ch_historic, encoding="utf-8-sig")
                gdf_database = gpd.GeoDataFrame(df_database, geometry=gpd.points_from_xy(df_database["X_COOR"], df_database["Y_COOR"]))
                if if_certainty == True:
                    data = point_error_distance.compute_error_distance(data, geographic_crs, gdf_database, lang)
        try:
            data = gpd.GeoDataFrame(data, geometry="geometry")
            data["X"] = data.loc[data["geometry"].notnull(), "geometry"].x
            data["Y"] = data.loc[data["geometry"].notnull(), "geometry"].y
        except:
            pass             
        
        data.drop(columns=["id"], inplace=True)
        return data