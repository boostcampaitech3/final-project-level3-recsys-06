import io

from segmentation import get_segmentator, get_segments
from starlette.responses import Response

from fastapi import FastAPI, File
from data import db_connect

# model = get_segmentator()
cursor = db_connect()

app = FastAPI(
    title="DeepLabV3 image segmentation",
    description="""Obtain semantic segmentation maps of the image in input via DeepLabV3 implemented in PyTorch.
                           Visit this URL at port 8501 for the streamlit interface.""",
    version="0.1.0",
)


# @app.post("/segmentation")
# def get_segmentation_map(file: bytes = File(...)):
#     """Get segmentation maps from image file"""
#     segmented_image = get_segments(model, file)
#     bytes_io = io.BytesIO()
#     segmented_image.save(bytes_io, format="PNG")
#     return Response(bytes_io.getvalue(), media_type="image/png")

@app.post("/{Token_ID}")
def get_item_info(Token_ID: str):
    cursor.execute(f"Select * from nftdb.TRADE where Token_ID = {Token_ID}")
    test = cursor.fetchall()
    return test

@app.get("/{Token_ID}")
def get_item_info(Token_ID: str):
    cursor.execute(f"Select * from nftdb.TRADE where Token_ID = {Token_ID}")
    test = cursor.fetchall()
    return test