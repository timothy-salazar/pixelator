""" This contains functions for 
"""
import sys
import pathlib
import os
from PIL import Image
import numpy as np


def get_project_dir():
    """ Input:
            None
        Output:
            project_dir: pathlib.Path - the path of the project directory
    """
    this_file_path = pathlib.Path(__file__)
    project_dir = this_file_path.parents[0]
    return project_dir

def resize_img_to_fit_term(img: Image):
    """ Input:
            img: PIL.Image - the image we want to fit our terminal window
        Output:
            img: PIL.Image - the same image, but resized to fit our terminal
                when displayed as ANSI formatted text 
    """
    term_width, term_height = os.get_terminal_size()
    scaling = min((term_width/img.width), ((term_height-1)/img.height)*2)
    return img.resize((int(img.width*scaling), int(img.height*scaling)))

def path_to_array(path: str, reduce_factor: int = None) -> Image:
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
    with open(path, 'rb') as f:
        img = Image.open(f)
        # the ANSI formatting we're using assumes RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        if not reduce_factor:
            # reduce_factor = get_term_reduce_factor(img)
            img = resize_img_to_fit_term(img)
        else:
            img = img.reduce(reduce_factor)
        img = np.asarray(img)
    return img

def image_to_blocks(path: str, reduce_factor: int = None) -> str:
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
    return array_to_blocks(img)

def array_to_blocks(img: np.array) -> str:
    """ Input:
            img: np.array - a numpy array
        Output:
            Returns a string representing a bunch of colored "UPPER HALF BLOCK"
            unicode characters.

    this takes an array representing our image and returns a string
    representation we can print.
    The way we get around the fact that the space taken up by a character on the
    terminal is a rectangle is:
        - read two lines of pixels
        - add an "UPPER HALF BLOCK" unicode character with the color of the
          first pixel
        - set the background to the color of the second character
    """
    s = ''
    for y in range(int(img.shape[0]//2)):
        for x in range(img.shape[1]):
            unicode_block = img[y*2:y*2+2, x]
            rt, gt, bt = unicode_block[0]
            rb, gb, bb = unicode_block[1]
            s += f'\033[38;2;{rt};{gt};{bt};48;2;{rb};{gb};{bb}m\u2580\033[0m'
        s += '\n'
    return s

def main():
    """ This is just for demo purposes
    """
    if len(sys.argv) == 1:
        path = os.path.join(get_project_dir(), 'images', 'dog.jpg')
    else:
        path = sys.argv[1]
    if len(sys.argv) == 3:
        reduce_factor = int(sys.argv[2])
    else:
        reduce_factor = None
    print(image_to_blocks(path, reduce_factor), end='')

if __name__ == "__main__":
    main()