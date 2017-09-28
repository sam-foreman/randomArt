## based closely on the cs5png module from Harvey Mudd College

import png
import os

def saveRGB( boxed_pixels, filename="out.png" ):
    """ need docstrings! """
    #print('Starting to save', filename, '...')
    f = open(filename, 'wb')      # binary mode is important
    W, H = getWH( boxed_pixels )
    w = png.Writer( W, H )
    #print "boxed_pixels are", boxed_pixels
    pixels = unbox( boxed_pixels )
    #print "pixels are", pixels
    w.write(f, pixels)
    f.flush()
    os.fsync(f.fileno())
    f.close()
    print(filename, "saved.")

def unbox( boxed_pixels ):
    """ assumes the pixels came from box
        and unboxes them!
    """
    flat_pixels = []
    for boxed_row in boxed_pixels:
        flat_row = []
        for pixel in boxed_row:
            flat_row.extend( pixel )
        flat_pixels.append( flat_row )
    return flat_pixels

def box( L ):
    """ boxes the flat pixels in row L
        assumes three channels!
    """
    newL = []
    STRIDE = 4  # since we're using RGBA!
    for i in range(len(L)//STRIDE):
        newL.append( L[STRIDE*i:STRIDE*i+3] ) # since we're providing RGB
    return newL


def getRGB( filename="in.png" ):
    """ need docstrings! """
    #print("Opening the", filename, " file (each dot is a row)", end=' ')
    reader = png.Reader(filename)
    #data = reader.read()
    data = reader.asRGBA()
    width = data[0]
    height = data[1]
    pixels = data[2]  # this is an iterator...
    PIXEL_LIST = []
    while True:
        try:
            a = next(pixels)
     #       print(".", end=' ')
            PIXEL_LIST.append( box( a.tolist() ) )
        except StopIteration:
     #       print("\nFile read.")
            break

    return PIXEL_LIST

def getWH( PX ):
    """ need docstrings! """
    H = len(PX)
    W = len(PX[0])
    return W, H

def binary_image( s, cols, rows ):
    """ need docstrings! """
    PX = []
    for row in range(rows):
        ROW = []
        for col in range(cols):
            c = int(s[row*cols + col])*255
            px = [ c, c, c ]
            ROW.append( px )
        PX.append( ROW )
    saveRGB( PX, 'binary.png' )
    #return PX

def load_image(filename):
    """ creates an Image object from a PNG file"""
    pixels = getRGB(filename)
    img = Image(len(pixels), len(pixels[0]))
    img.image_data = pixels
    return img

class Image:
    def __init__(self, height, width):
        """ constructor for an initially empty Image """
        self.width = width
        self.height = height
        default = (0,255,0)   #(255,255,255)
        self.image_data = \
            [ [ default for col in range(width) ] \
                        for row in range(height)]
        
    def save(self, filename='test.png'):
        """ save the object's data to a file """
        saveRGB(self.image_data, filename)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_pixel(self, row, col):
        return self.image_data[row][col]

    def set_pixel(self, row, col, pixel):
        """ set a single pixel in a PNGImage """
        # check if rgb is a three-tuple
        if type(pixel) == type( [0,0,0] ) and \
           len(pixel) == 3:
            pass # ok
        else:
            print("in set_pixel, the color", pixel, end=' ')
            print("was not in a recognized format.")

        # check if we're in bounds
        if 0 <= col < self.width and \
           0 <= row < self.height:
            self.image_data[row][col] = pixel
        else:
            print("in set_pixel, row, col", row, col, end=' ')
            print("was not in bounds.")
            return

        return
