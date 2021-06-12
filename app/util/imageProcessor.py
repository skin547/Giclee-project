import cv2
import numpy as np
import math

class ImageProcessor():
    def resize( self, source, width, height ):
        source = cv2.resize( source, (width, height), interpolation = cv2.INTER_AREA )
        return source
        
    def fitIn( self, source, destination ):
        d_width, d_height, _ = destination.shape
        source = cv2.resize( source, (d_width, d_height), interpolation = cv2.INTER_AREA)
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

    def mixed_clone( self, source, destination ):
        width, height, channel = destination.shape
        mask = 255 * np.ones( destination.shape, destination.dtype )
        center = ( int(height/2), int(width/2) )
        clone = cv2.seamlessClone( source, destination, mask, center, cv2.MIXED_CLONE)
        return clone

    def normal_clone( self, source, destination ):
        width, height, channel = destination.shape
        mask = 255 * np.ones( destination.shape, destination.dtype )
        center = ( int(height/2), int(width/2) )
        clone = cv2.seamlessClone( source, destination, mask, center, cv2.NORMAL_CLONE)
        return clone

    def filter( self, source ):
        img = source.astype(np.float32) / 255
        kernel = cv2.getGaborKernel((21, 21), 5, 1, 10, 1, 0, cv2.CV_32F)
        kernel /= math.sqrt((kernel * kernel).sum())
        filtered = cv2.filter2D(img, -1, kernel)
        # cv2.imshow("filtered",filtered)
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

    mixed_clone = imageProcessor.mixed_clone( paper, image ) # note : paper are source and image are dest
    cv2.imshow("mixed_clone", mixed_clone)
    normal_clone = imageProcessor.normal_clone( image, paper ) # note : paper are source and image are dest
    cv2.imshow("normal_clone", normal_clone)
    cv2.waitKey()
    cv2.destroyAllWindows()
