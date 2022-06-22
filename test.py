import asyncio

import httpx


async def test():
    with open(r'/1/search_poligon.geojson', 'rb') as json_file:
        # files = {'upload-file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel')}
        files = {'upload_file': (None, json_file, 'application/json')}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="http://127.0.0.1:8000/ndvi",
                files=files
            )

            assert response.status_code == 200
            assert response.raw == 'myimage.tiff'


asyncio.run(test())
