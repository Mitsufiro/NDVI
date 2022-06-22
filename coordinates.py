import json


def search_polygon(geojson):  #преобразование geojson к четырехугольному полигону если формат не удовлетворяет feature
        with open(geojson) as f:
            template = json.load(f)
            coordinates = template['features'][0]['geometry']['coordinates']
            sum_of_cords = [0, 0]  # долгота и широта
            # count_of_cords = 0
            min_x = 180
            max_x = -180
            min_y = 180
            max_y = -180

            for i in coordinates:
                for j in i:
                    for k in j:
                        if k[0] > max_x:
                            max_x = k[0]
                        elif k[0] < min_x:
                            min_x = k[0]
                        elif k[1] > max_y:
                            max_y = k[1]
                        elif k[1] < min_y:
                            min_y = k[1]
                            # sum_of_cords[0] += k[0]
                        # sum_of_cords[1] += k[1]
                        # count_of_cords += 1
            polygon = [[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y], [min_x, min_y]]
        with open('search_poligon.geojson', 'r') as f:
            json_data = json.load(f)
            json_data['geometry']['coordinates'] = [polygon]  #вставка четырехугольного полигона

        with open('search_poligon.geojson', 'w') as f: #запись нового geojson в файл
            f.write(json.dumps(json_data))
        return 'search_poligon.geojson'
# search_polygon('input.geojson')

# print(sum_of_cords)
# sum_of_cords[0] = sum_of_cords[0] / count_of_cords
# sum_of_cords[1] = sum_of_cords[1] / count_of_cords
# print(sum_of_cords)

# with open(r'C:\Projects\geo_ndvi\1\search_poligon.geojson') as gfile:
#     x = json.load(gfile)
#     gfile.writelines(x['geometry']['coordinates'].extend([avg, avg]))
#     f.writelines(x)
