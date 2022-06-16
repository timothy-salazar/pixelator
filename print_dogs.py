from PIL import Image
import numpy as np
import sys
import pathlib
import os

def get_project_dir():
    """ Input:
            None
        Output:
            project_dir: pathlib.Path - the path
                of the project directory
    """
    this_file_path = pathlib.Path(__file__)
    project_dir = this_file_path.parents[0]
    return project_dir

def path_to_array(path:str, reduce_factor:int=10) -> Image:
    """ Input:
            path: str - the path to the image file we want to open
            reduce_factor: int - the factor we want to reduce the 
                image by 
        Output:
            returns a PIL Image representing the image, downscaled by
            reduce_factor. 
            
    We're reducing the image to a very small size so that we can translate
    each pixel directly to some colored blocks. If reduce_factor isn't small
    enough, then the "lines" will wrap around and the image won't display 
    correctly
    """
    with open(path,'rb') as f:
        img = Image.open(f)
        img = img.reduce(reduce_factor)
        img = np.asarray(img) 
    # This is bad and I should feel bad for leaving it here.
    # If there is an alpha channel this just rips it out with a reckless
    # disregard for the potential consequences
    return img[:,:,:3]
        
def image_to_blocks(path:str, reduce_factor:int=30) -> str:
    """ Input:
            path: str - the path to the image file we want to open
            reduce_factor: int - the factor we want to reduce the 
                image by
        Output:
            Returns a string representing a bunch of colored "UPPER HALF BLOCK" 
            unicode characters. 
    
    This gets an image from a given path, and returns a string representation we
    can print. 
    The way we get around the fact that the space taken up by a character on the
    terminal is a rectangle is:
        - read two lines of pixels 
        - add an "UPPER HALF BLOCK" unicode character with the color of the 
          first pixel
        - set the background to the color of the second character
    """
    
    img = path_to_array(path, reduce_factor)
    s = ''
    for y in range(int(img.shape[0]//2)):
        for x in range(img.shape[1]):
            unicode_block = img[y*2:y*2+2,x]
            rt,gt,bt = unicode_block[0]
            rb,gb,bb = unicode_block[1]
            s += f'\033[38;2;{rt};{gt};{bt};48;2;{rb};{gb};{bb}m\u2580\033[0m'
        s += '\n'
    return s

def main():
    if len(sys.argv) == 1:
        path = os.path.join(get_project_dir(),'images','dog_1.png')
    else:
        path = sys.argv[1]
    if len(sys.argv) == 3:
        reduce_factor = int(sys.argv[2])
    else:
        reduce_factor = 30
    print(image_to_blocks(path, reduce_factor))

if __name__ == "__main__":
    main()