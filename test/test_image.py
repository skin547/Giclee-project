import os.path as path
import cv2
import numpy as np

from app.util.imageProcessor import ImageProcessor

def test_resize():
    imageProcessor = ImageProcessor()

    abs_path = path.dirname(__file__)
    file_path = path.abspath( path.join( abs_path, f"../static/image/materialC.jpg" ) )
    image = cv2.imread( file_path )
    height, width = (200, 300 )
    image = imageProcessor.resize( image, width, height )
    assert (image.shape[0], image.shape[1]) == (200, 300 )

def test_resizeTo():
    imageProcessor = ImageProcessor()
    abs_path = path.dirname(__file__)
    imageA_file_path = path.abspath( path.join( abs_path, f"../static/image/materialB.jpeg" ) )
    imageB_file_path = path.abspath( path.join( abs_path, f"../static/image/materialC.jpg" ) )
    imageA = cv2.imread( imageA_file_path )
    imageB = cv2.imread( imageB_file_path)

    imageA = imageProcessor.resizeTo( imageA, imageB )
    assert (imageA.shape[0], imageA.shape[1]) == (imageB.shape[0], imageB.shape[1] )

def test_mixedClone():
    imageProcessor = ImageProcessor()
    convert_to = "canvas"

    abs_path = path.dirname(__file__)
    image_file_path = path.abspath( path.join( abs_path, f"../static/image/materialC.jpg" ) )
    image = cv2.imread(image_file_path)

    paper_file_path = path.abspath( path.join( abs_path, f"../static/paper/{convert_to}.jpeg" ) )
    paper = cv2.imread( paper_file_path )

    height, width, _ = image.shape

    if( image.shape[0] > 1080 or image.shape[1] > 1920):
        image = imageProcessor.scaleAdjust( image, 1920, 1080 )

    paper = imageProcessor.makeBorder( paper, image )
    paper = imageProcessor.resize( paper, width, height )

    print( paper.shape, image.shape )
    mixed_clone = imageProcessor.mixedClone( paper, image )
    print( mixed_clone.shape )
    

