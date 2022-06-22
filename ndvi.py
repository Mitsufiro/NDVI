import glob
import os
import matplotlib.pyplot as plt
import numpy as np
import rasterio as rio
from osgeo import gdal
from sentinelsat import read_geojson
from maps import downloading_of_file
from unzip import clear_zipfiles, unzipping
import json
from coordinates import search_polygon


def load_satellite(geo_json_file, debug=False):

    if len(os.listdir('unzipped/')) == 0 and len(os.listdir('zipfiles/')) == 0:
        downloading_of_file(geo_json_file)  # скачиваем данные
    if len(os.listdir('zipfiles/')) > 0:
        file_name = os.listdir('zipfiles/')[0].replace('.zip',
                                                       '')  # ловим имя скачанного файла для дальнейшей обработки
        unzipping()  # разархивирование скачанного файла
    elif len(os.listdir('unzipped/')) > 0 and len(os.listdir('zipfiles/')) == 0:
        file_name = os.listdir('unzipped/')[0].replace('.SAFE', '')

    R10 = glob.glob(f'unzipped/{file_name}.SAFE/GRANULE/L2A**/IMG_DATA/R10m')[0]

    # очистка папки zipfiles от архивов
    file_name = file_name[-15:-1]
    b4 = rio.open(glob.glob(f'{R10}/**B04_10m.jp2')[0], driver='JP2OpenJPEG')
    b8 = rio.open(glob.glob(f'{R10}/**B08_10m.jp2')[0], driver='JP2OpenJPEG')
    with rio.open(f'ground/{file_name}.tiff', 'w', driver='Gtiff', width=b4.width, height=b4.height,
                  count=2, crs=b4.crs, transform=b4.transform, dtype=b4.dtypes[0]) as rgb:
        rgb.write(b4.read(1), 1)
        rgb.write(b8.read(1), 2)
        rgb.close()

    list_tif = glob.glob(f'ground/{file_name}.tiff')
    out_path = 'results/'

    for tif in list_tif:
        in_ds = gdal.Open(tif)
        # Получить путь к файлу и имя файла без суффикса
        (filepath, fullname) = os.path.split(tif)
        (prename, suffix) = os.path.splitext(fullname)
        if in_ds is None:
            print('Could not open the file ' + tif)
        else:
            # Преобразование типа данных MODIS в отражательную способность
            red = in_ds.GetRasterBand(1).ReadAsArray() * 0.0001
            nir = in_ds.GetRasterBand(2).ReadAsArray() * 0.0001
            print(red)
            print('...........................')
            first = nir - red
            second = nir + red
            np.seterr(invalid='ignore')
            ndvi = first / second
            # Преобразование NAN в значение 0
            nan_index = np.isnan(ndvi)
            ndvi[nan_index] = 0
            ndvi = ndvi.astype(np.float32)
            # Сохраняем рассчитанный NDVI в виде файла GeoTiff
            gtiff_driver = gdal.GetDriverByName('GTiff')
            # Пакетная обработка должна учитывать, что имя файла является переменной здесь перехватывается имя файла без суффиксп соответствующее исходному файлу
            out_ds = gtiff_driver.Create(out_path + prename + '_ndvi.tiff',
                                         ndvi.shape[1], ndvi.shape[0], 1, gdal.GDT_Float32)
            # Установим проекцию координат данных NDVI на исходную проекцию координат
            out_ds.SetProjection(in_ds.GetProjection())
            out_ds.SetGeoTransform(in_ds.GetGeoTransform())
            out_band = out_ds.GetRasterBand(1)
            out_band.WriteArray(ndvi)
            out_band.FlushCache()
            if debug:
                plt.imshow(ndvi)
                # отображать изображение
                plt.axis('off')  # Не отображать оси
                # plt.show()
            plt.imsave(f'images/{file_name}.jpeg', ndvi)
    clear_zipfiles()
    return f'images/{file_name}.jpeg'


if __name__ == '__main__':
    with open('input.geojson', 'r') as f:
        json_data = json.load(f)
        if json_data['type'] == 'FeatureCollection':
            json_file = read_geojson(search_polygon('input.geojson'))
        else:
            json_file = read_geojson('input.geojson')
    load_satellite(geo_json_file=json_file, debug=True)
