import argparse
from PIL import Image
import os
import sys

# TODO сделать ограничение на допустимые размеры (масштаб)
# TODO сформировать имя нового рисунка и путь его сохранения


def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', help='path to original image file')
    parser.add_argument('-w', '--width', help='With of result image. Optional. May be the only one.')
    parser.add_argument('-ht', '--height', help='Height of result image. Optional. May be the only one.')
    parser.add_argument('-s', '--scale', help='Scale of result image. Optional. Works only if width and height NOT presented.')
    parser.add_argument('-o', '--output', help='Path to store result image. Optional. If not, file will be saved beside original')
    return parser.parse_args()


def check_argument_presence_and_value(argument, argument_name, dictionary, type='int'):
    if argument and argument.isnumeric():
        if type == 'int':
            dictionary[argument_name] = int(argument)
        elif type == 'float':
            dictionary[argument_name] = float(argument)
    elif not argument:
        return
    elif not argument.isnumeric():
        raise TypeError


def process_args(size_params):
    args = add_arguments()
    if not os.path.isfile(args.filepath):
        raise IOError
    check_argument_presence_and_value(args.width, 'width', size_params)
    check_argument_presence_and_value(args.height, 'height', size_params)
    check_argument_presence_and_value(args.scale, 'scale', size_params, type='float')
    if any(key in ['width', 'height'] for key in size_params.keys()) and 'scale' in size_params.keys():
        raise AttributeError
    return args


def open_image(filepath):
    source_image = Image.open(filepath)
    return source_image


def compute_result_size(source_size, size_params):
    if 'scale' in size_params:
        return (int(source_size['width'] * size_params['scale']), int(source_size['height'] * size_params['scale']),)
    if 'width' in size_params and 'height' in size_params:
        print("Scale of source image will not be saved")
        return (size_params['width'], size_params['height'],)
    if 'width' in size_params:
        height = int((size_params['width'] / source_size['width']) * source_size['height'])
        return (size_params['width'], height,)
    if 'height' in size_params:
        width = int((size_params['height'] / source_size['height']) * source_size['width'])
        return (width, size_params['height'],)


def resize_image(source_image, source_size, size_params):
    result_size = compute_result_size(source_size, size_params)
    resized_image = source_image.resize(result_size)
    return resized_image


def get_size_from_thumbnails(source_image):
    width_index = 0
    height_index = 1
    size = {}
    size['width'] = source_image.size[width_index]
    size['height'] = source_image.size[height_index]
    return size


if __name__ == '__main__':
    size_params = {}
    try:
        args = process_args(size_params)
    except IOError:
        sys.exit('Presented file is not exists')
    except AttributeError:
        sys.exit('Incompatible size arguments introduced. Need arguments: width or height (or both), or scale only!')
    except TypeError:
        sys.exit('Size arguments must be only numeric!')
    try:
        source_image = open_image(args.filepath)
        source_size = get_size_from_thumbnails(source_image)
        resize_image(source_image, source_size, size_params)
        # resized_image = resize_image(source_image, source_size, size_params)
        source_image.close()
    except IOError:
        sys.exit('Unable to open file {}!'.format(args.filepath))

