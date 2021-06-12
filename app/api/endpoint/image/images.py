from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import cv2
import numpy as np
import base64
import io

from app.util.imageProcessor import ImageProcessor

router = APIRouter()
imageProcessor = ImageProcessor()

class BlendImage(BaseModel):
    name: str
    convert_to: str
    shift_x: int
    shift_y: int
    base64image : str

@router.get("/")
def read_image():
    image = cv2.imread("/Users/frankwu/projects/giclee_c127/clone_demo/static/image/2498.jpg")
    paper = cv2.imread("/Users/frankwu/projects/giclee_c127/clone_demo/static/paper/canvas.jpeg")

    image = imageProcessor.fitIn( image, paper )

    mixed_clone = imageProcessor.mixed_clone( paper, image )

    res, image_png = cv2.imencode(".png", mixed_clone)
    return StreamingResponse( io.BytesIO( image_png.tobytes() ), media_type = "image/png" )

@router.get("/base64")
def get_base64_image():
    image = cv2.imread("/Users/frankwu/projects/giclee_c127/clone_demo/static/image/2498.jpg")
    paper = cv2.imread("/Users/frankwu/projects/giclee_c127/clone_demo/static/paper/canvas.jpeg")

    image = imageProcessor.fitIn( image, paper )

    mixed_clone = imageProcessor.mixed_clone( paper, image )

    res, image_png = cv2.imencode(".png", mixed_clone)
    
    endcoded_img = base64.b64encode( image_png )

    return {
        'filename': "mixed_clone",
        'encoded_img': endcoded_img,
    }


@router.post("/blend")
def blend_image(data: BlendImage):
    base64_decode = base64.b64decode( data.base64image )
    img_array = np.frombuffer( base64_decode, np.uint8 ) # 轉換np序列
    image = cv2.imdecode( img_array, cv2.IMREAD_COLOR )  # 轉換Opencv格式

    paper = cv2.imread(f"/Users/frankwu/projects/giclee_c127/clone_demo/static/paper/{data.convert_to}.jpeg")
    paper = imageProcessor.resize( paper, 600, 600 )
    image = imageProcessor.cutCorner( image, paper, data.shift_x, data.shift_y )

    mixed_clone = imageProcessor.mixed_clone( paper, image )

    res, image_jpg = cv2.imencode(".jpg", mixed_clone)

    if( res ):
        return StreamingResponse( io.BytesIO( image_jpg.tobytes() ), media_type = "image/png" )
    else:
        return {"error":"oops"}
