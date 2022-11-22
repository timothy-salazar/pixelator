#!/usr/bin/python3
""" Takes image input from pipe, converts it into blocks that
can be printed to stdout
"""
import os
import sys
import argparse
from PIL import Image
import numpy as np
from ansi_image import array_to_blocks

def resize_img(
        img: Image,
        width: float = None,
        height: float = None,
        columns: int = None,
        rows: int = None):
    """ Input:
            img: PIL.Image - the image we want to resize
            width: float - the proportion of the terminal's width we want the
                final image to fill.
            height: float - the proportion of the terminal's height we want the
                final image to fill.
            columns: int - specifies the width of the final image in pixels.
            rows: int - specifies the height of the final image in pixels.
        Output:
            returns a numpy array. This is the image, reduced by the appropriate
            amount.

    This function takes 4 arguments for specifying output size:
        width, height, columns, rows.
    At most ONE of these should be provided by the user. If none are provided,
    the image is sized to fill the terminal window.
    """

    # Test output size arguments:
    output_args = [
        ('width', width),
        ('height', height),
        ('columns', columns),
        ('rows', rows)]
    output_args = {i[0]:i[1] for i in output_args if i[1]}
    if len(output_args) > 1:
        raise ValueError(f'''
            resize_img() accepts ONE of four mutually exclusive arguments to 
            determine output image size: width, height, columns, or rows.
            Instead output_args was given {len(output_args)}: {output_args}
        ''')
    term_width, term_height = os.get_terminal_size()
    if width:
        scaling = (term_width * width) / img.width
    elif height:
        # we multiply by 2 because each character is twice as wide as it is
        # tall, so we're putting two pixels into each character 'rectangle'
        scaling = ((term_height * height) / img.height)*2
    elif columns:
        scaling = columns / img.width
    elif rows:
        scaling = (rows / img.height)*2
    else:
        # If no "output size" options are provided, we resize the image so that
        # it will fit on the screen
        scaling = min((term_width/img.width), ((term_height-1)/img.height)*2)

    # Image processing
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize((int(img.width*scaling), int(img.height*scaling)))
    return np.asarray(img)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'infile',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin.buffer)
    parser.add_argument(
        '-f',
        '--file',
        type=str,
        help='''
        A valid path to an image file that you'd like to see displayed on your
        terminal.
        '''
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-w',
        '--width',
        type=float,
        default=None,
        help='''
        The proportion of the screen width the image should take up (as a 
        decimal) 
        i.e.: if you wanted the image to take up 90 percent of the screen width
        youg would use "-w .9".
        Mutually exclusive with the '--height' argument.
        '''
    )
    group.add_argument(
        '-hg',
        '--height',
        type=float,
        default=None,
        help='''
        The proportion of the screen height the image should take up (as a 
        decimal) 
        i.e.: if you wanted the image to take up 90 percent of the screen height
        you would use "-hg .9".
        Mutually exclusive with the '--width' argument.
        '''
    )
    group.add_argument(
        '-c',
        '--columns',
        type=int,
        default=None,
        help='''
        Allows you to manually specify the width of the image in columns.
        '''
    )
    group.add_argument(
        '-r',
        '--rows',
        type=int,
        default=None,
        help='''
        Allows you to manually spedify the height of hte image in rows.
        '''
    )

    args = parser.parse_args()
    image = Image.open(args.infile)
    image = resize_img(
        image,
        width=args.width,
        height=args.height,
        columns=args.columns,
        rows=args.rows)

    sys.stdout.write(array_to_blocks(image))
    sys.exit(0)
