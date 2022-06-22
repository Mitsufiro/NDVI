from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from ndvi import load_satellite
import json
app = FastAPI()


@app.post("/ndvi")
def generate_ndvi_image(
        upload_file: UploadFile = File(...),
):
    file = upload_file.file.read()
    # process_geojson
    image_path = load_satellite(json.loads(file))

    return FileResponse(image_path)
