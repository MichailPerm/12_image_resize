import argparse
from PIL import Image
import os
import sys

# TODO сделать ограничение на допустимые размеры (масштаб)
# TODO сформировать имя нового рисунка и путь его сохранения

WIDTH_INDEX = 0
HEIGHT_INDEX = 1


def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--filepath',
        help='path to original image file')
    parser.add_argument(
        '-w', '--width',
        help='With of result image. Optional. May be the only one.')
    parser.add_argument(
        '-ht', '--height',
        help='Height of result image. Optional. May be the only one.')
    parser.add_argument(
        '-s', '--scale',
        help='Scale of result image. Optional. Must be only one!')
    parser.add_argument(
        '-o', '--output',
        help='Path to store result image. Optional.')
    return parser.parse_args()


def check_argument_presence_and_value(argument,
                                      argument_name,
                                      dictionary,
                                      type='int'):
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
    check_argument_presence_and_value(args.scale,
                                      'scale', size_params, type='float')
    if any(key in ['width', 'height'] for key in size_params.keys()):
        if 'scale' in size_params.keys():
            raise AttributeError
    if args.output and not os.path.isdir(args.output):
        raise RuntimeError
    return args


def open_image(filepath):
    source_image = Image.open(filepath)
    return source_image


def compute_result_size(source_size, size_params):
    if 'scale' in size_params:
        return (int(source_size['width'] * size_params['scale']),
                int(source_size['height'] * size_params['scale']),)
    if 'width' in size_params and 'height' in size_params:
        print('Scale of source image will not be saved')
        return (size_params['width'], size_params['height'],)
    if 'width' in size_params:
        height = int((size_params['width'] / source_size['width']) * source_size['height'])
        return (size_params['width'], height,)
    if 'height' in size_params:
        width = int((size_params['height'] / source_size['height']) * source_size['width'])
        return (width, size_params['height'],)


def resize_image(source_image, source_size, size_params, output_size):
    output_size_tuple = compute_result_size(source_size, size_params)
    output_size['width'] = output_size_tuple[WIDTH_INDEX]
    output_size['height'] = output_size_tuple[HEIGHT_INDEX]
    resized_image = source_image.resize(output_size_tuple)
    return resized_image


def get_size_from_thumbnails(source_image):
    size = {}
    size['width'] = source_image.size[WIDTH_INDEX]
    size['height'] = source_image.size[HEIGHT_INDEX]
    return size


def save_image(args, resized_image, output_size):
    source_image_dirs, source_image_name = os.path.split(args.filepath)
    source_image_name_parts = source_image_name.split('.')
    output_image_name = '{}__{}x{}.{}'.format(source_image_name_parts[0],
                                              output_size['width'],
                                              output_size['height'],
                                              source_image_name_parts[1])
    if not getattr(args, 'output'):
        output_path = source_image_dirs + '/' + output_image_name
        message = 'Image saved at {} as {}'.format(source_image_dirs, output_image_name)
    else:
        output_path = args.output + output_image_name
        message = 'Image saved at {} as {}'.format(args.output, output_image_name)
    resized_image.save(output_path)
    return message


if __name__ == '__main__':
    size_params = {}
    output_size = {}
    try:
        args = process_args(size_params)
    except IOError:
        sys.exit('Presented file is not exists')
    except AttributeError:
        sys.exit('Incompatible size arguments introduced. Need arguments: width or height (or both), or scale only!')
    except TypeError:
        sys.exit('Size arguments must be only numeric!')
    except RuntimeError:
        sys.exit('Path to store output file is not correct!')
    try:
        source_image = open_image(args.filepath)
        source_size = get_size_from_thumbnails(source_image)
        resized_image = resize_image(source_image, source_size, size_params, output_size)
        source_image.close()
        message = save_image(args, resized_image, output_size)
        print(message)
    except PermissionError:
        sys.exit('Something wrong with a file. Check if output path correct!')
    except IOError:
        sys.exit('Unable to open file {}!'.format(args.filepath))
