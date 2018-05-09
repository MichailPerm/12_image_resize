import argparse
from PIL import Image
import os
import sys


def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', help='path to original image file')
    parser.add_argument('-w', '--width', help='With of result image. Optional. May be the only one.')
    parser.add_argument('-ht', '--height', help='Height of result image. Optional. May be the only one.')
    parser.add_argument('-s', '--scale', help='Scale of result image. Optional. Works only if width and height NOT presented.')
    parser.add_argument('-o', '--output', help='Path to store result image. Optional. If not, file will be saved beside original')
    return parser.parse_args()


def process_args():
    args = add_arguments()
    if not os.path.isfile(args.filepath):
        raise IOError
    if ((args.width or args.height) and args.scale) == True:
        raise AttributeError
    if args.width and args.height or args.scale:
        if not (args.width.isnumeric() and args.height.isnumeric() and args.scale.isnumeric()):
            raise TypeError
        if int(args.width) <=0 or int(args.height) <= 0:
            raise ValueError
    return args


def open_image(filepath):
    with Image.open(filepath) as source_image:
        return source_image


def resize_image(args, source_image):
    if args.width and args.height:
        size = (args.width, args.height,)
    elif args.width and not args.height:

    resized_image = source_image.resize(size)
    return resized_image



if __name__ == '__main__':
    try:
        args = process_args()
    except IOError:
        sys.exit('Presented file is not exists')
    except AttributeError:
       sys.exit('Incompatible size arguments introduced. Need arguments: width or height (or both), or scale only!')
    except TypeError:
        sys.exit('Size arguments must be only numeric!')
    except ValueError:
        sys.exit('Width and height may be only greater 0!')
    try:
        source_image = open_image(args.filepath)
        resized_image = resize_image(args, source_image)
    except IOError:
        sys.exit('Unable to open file {}!'.format(args.filepath))

