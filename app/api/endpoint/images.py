from fastapi import APIRouter
from fastapi.responses import StreamingResponse

import cv2
import numpy as np
import base64
import io
import os.path as path

from app.util.imageProcessor import ImageProcessor
from app.model.BlendImage import BlendImage
from app.model.PreviewImage import PreviewImage

router = APIRouter()
imageProcessor = ImageProcessor()

@router.get("/")
def read_image():
    image = cv2.imread("/Users/frankwu/projects/giclee_c127/clone_demo/static/image/materialA.png")
    paper = cv2.imread("/Users/frankwu/projects/giclee_c127/clone_demo/static/paper/canvas.jpeg")

    image = imageProcessor.fitIn( image, paper )

    mixed_clone = imageProcessor.mixedClone( paper, image )

    res, image_png = cv2.imencode(".png", mixed_clone)
    if( res ):
        return StreamingResponse( io.BytesIO( image_png.tobytes() ), media_type = "image/png" )
    else:
        return { "error" : "oops, something wrong getting images" }

@router.get("/textures")
def get_textures():
    image = cv2.imread("/Users/frankwu/projects/giclee_c127/clone_demo/static/image/2498.jpg")
    paper = cv2.imread("/Users/frankwu/projects/giclee_c127/clone_demo/static/paper/canvas.jpeg")

    image = imageProcessor.fitIn( image, paper )

    mixed_clone = imageProcessor.mixedClone( paper, image )

    res, image_png = cv2.imencode(".png", mixed_clone)
    
    endcoded_img = base64.b64encode( image_png )

    return {
        'filename': "mixed_clone",
        'encoded_img': endcoded_img,
    }

@router.get("/base64")
def get_base64_image():
    image = cv2.imread("/Users/frankwu/projects/giclee_c127/clone_demo/static/image/2498.jpg")
    paper = cv2.imread("/Users/frankwu/projects/giclee_c127/clone_demo/static/paper/canvas.jpeg")

    image = imageProcessor.fitIn( image, paper )

    mixed_clone = imageProcessor.mixedClone( paper, image )

    res, image_png = cv2.imencode(".png", mixed_clone)
    
    endcoded_img = base64.b64encode( image_png )

    return {
        'filename': "mixed_clone",
        'encoded_img': endcoded_img,
    }

@router.post("/blend")
def preview_image(data: PreviewImage):
    image = imageProcessor.fromBase64( data.base64image.split(",")[1] )

    abs_path = path.dirname(__file__)
    file_path = path.abspath( path.join( abs_path, f"../../../static/paper/{data.convert_to}.jpeg" ) )
    paper = cv2.imread( file_path )

    if( image.shape[0] > 1080 or image.shape[1] > 1920):
        image = imageProcessor.scaleAdjust( image, 1920, 1080 )

    paper = imageProcessor.makeBorder( paper, image )
    paper = imageProcessor.resizeTo( paper, image )

    mixed_clone = imageProcessor.mixedClone( paper, image )

    res, image_jpg = cv2.imencode(".jpg", mixed_clone )
    if( res ):
        endcoded_img = base64.b64encode( image_jpg )
        return {
            'name': "mixed_clone",
            'base64Image': endcoded_img,
        }
    else:
        return { "error" : "oops, something wrong when cloning image" }


@router.post("/preview")
def blend_image(data: BlendImage):
    image = imageProcessor.fromBase64( data.base64image.split(",")[1] )

    abs_path = path.dirname(__file__)
    file_path = path.abspath( path.join( abs_path, f"../../../static/paper/{data.convert_to}.jpeg" ) )
    paper = cv2.imread( file_path )

    paper = imageProcessor.resize( paper, 600, 600 )
    image = imageProcessor.cutCorner( image, paper, data.shift_x, data.shift_y )

    mixed_clone = imageProcessor.mixedClone( paper, image )

    res, image_png = cv2.imencode(".png", mixed_clone)

    if( res ):
        endcoded_img = base64.b64encode( image_png )
        return {
            'name': "mixed_clone",
            'base64Image': endcoded_img,
        }
    else:
        return { "error" : "oops, something wrong when cloning image" }
