import cv2
import numpy as np
import math
import base64

class ImageProcessor():
    def fromBase64( self, base64Image ):
        decoded = base64.b64decode( base64Image )
        img_array = np.frombuffer( decoded, np.uint8 ) # 轉換np序列
        image = cv2.imdecode( img_array, cv2.IMREAD_COLOR ) # 轉換Opencv格式
        return image

    def resize( self, source, width, height ):
        source = cv2.resize( source, (width, height), interpolation = cv2.INTER_AREA )
        return source

    def resizeTo( self, source, destination ):
        height, width, _ = destination.shape
        source = cv2.resize( source, (width, height), interpolation = cv2.INTER_AREA )
        return source
        
    def fitIn( self, source, destination ):
        d_width, d_height, _ = destination.shape
        source = cv2.resize( source, (d_width, d_height), interpolation = cv2.INTER_AREA)
        return source

    def scaleAdjust( self, source, new_width, new_height ):
        height, width, _ = source.shape
        if width / height >= new_width / new_height:
            source = cv2.resize(source, (new_width, int(height * new_width / width)))
        else:
            source = cv2.resize(source, (int(width * new_height / height), new_height))
        return source


    def makeBorder( self, source, destination ):
        source_y, source_x, _ = source.shape
        destination_y, destination_x, _ = destination.shape
        diff_x = destination_x - source_x
        diff_y = destination_y - source_y
        if( diff_x > 0 and diff_y > 0):
            source = cv2.copyMakeBorder( source, 0, diff_y, 0, diff_x, cv2.BORDER_REFLECT)
        elif( diff_x > 0 ):
            source = cv2.copyMakeBorder( source, 0, 0, 0, diff_x, cv2.BORDER_REFLECT)
        elif(  diff_y > 0):
            source = cv2.copyMakeBorder( source, 0, diff_y, 0, 0, cv2.BORDER_REFLECT)
        return source

    def cutCorner( self, source, destination, shift_x, shift_y ):
        s_width, s_height, _ = source.shape
        d_width, d_height, _ = destination.shape
        if( s_width > d_width ):
            x, y, _ = source.shape
            source = source[ shift_y:shift_y+y, shift_x:shift_x+d_width]
        if( s_height > d_height ):
            x, y, _ = source.shape
            source = source[ shift_y:shift_y+d_height, shift_x:shift_x+x]
        return source

    def mixedClone( self, texture, image ):
        width, height, _ = image.shape
        mask = 255 * np.ones( image.shape, image.dtype )
        center = ( int(height/2), int(width/2) )
        clone = cv2.seamlessClone( texture, image, mask, center, cv2.MIXED_CLONE)
        return clone

    def filter( self, source ):
        img = source.astype(np.float32) / 255
        kernel = cv2.getGaborKernel((21, 21), 5, 1, 10, 1, 0, cv2.CV_32F)
        kernel /= math.sqrt((kernel * kernel).sum())
        filtered = cv2.filter2D(img, -1, kernel)
        return filtered


if __name__ == '__main__':

    imageProcessor = ImageProcessor()

    image = cv2.imread("../../static/image/2498.jpg")
    paper = cv2.imread("../../static/paper/canvas.jpeg")

    # paper = filter(paper)
    width, height, channel = paper.shape

    image = imageProcessor.fitIn( image, paper )
    print(paper.shape)
    print(image.shape)

    cv2.imshow("image", image)
    cv2.imshow("paper", paper)

    mixed_clone = imageProcessor.mixedClone( paper, image ) # note : paper are source and image are dest
    cv2.imshow("mixed_clone", mixed_clone)
    normal_clone = imageProcessor.normal_clone( image, paper ) # note : paper are source and image are dest
    cv2.imshow("normal_clone", normal_clone)
    cv2.waitKey()
    cv2.destroyAllWindows()
