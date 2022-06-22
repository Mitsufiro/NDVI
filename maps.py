import os
import numpy as np
from osgeo import gdal
import glob
import matplotlib.pyplot as plt
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import pandas
import rasterio as rio
from unzip import unzipping, clear_zipfiles
from coordinates import search_polygon
import json


def downloading_of_file(geojson_file):   #скачивание архива
    user = 'ginfrost'
    password = '901290129012chux'
    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
    with open('input.geojson', 'r') as f:
        json_data = json.load(f)
        if json_data['type'] == 'FeatureCollection':
            footprint = geojson_to_wkt(read_geojson(search_polygon('input.geojson')))
        else:
            footprint = geojson_to_wkt(geojson_file)
        products = api.query(footprint,
                             date=('NOW-2DAYS', 'NOW'),
                             platformname='Sentinel-2',
                             producttype='S2MSI2A', limit=1)

    products_df = api.to_dataframe(products)
    products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
    products_df_sorted = products_df_sorted.head(5)
    api.download_all(products_df.index, directory_path='zipfiles') #указание места скачивания

# downloading_of_file('search_poligon.geojson')
# file_name = os.listdir('zipfiles')[0]  # ловим имя скачанного файла для дальнейшей обработки
# clear_zipfiles()  # очистка папки zipfiles от архивов
