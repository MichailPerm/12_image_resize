import argparse
from PIL import Image
import os
import sys


WIDTH_INDEX = 0
HEIGHT_INDEX = 1


def add_arguments():
    parser = argparse.ArgumentParser(
        epilog='REMEMBER! Too big size or scale may'
               'cause your computer freeze!')
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


def check_size_argument_presence_and_value(argument,
                                           argument_name,
                                           dictionary,
                                           arg_type='int'):
    if argument and argument.isnumeric():
        if arg_type == 'int':
            dictionary[argument_name] = int(argument)
        elif arg_type == 'float':
            dictionary[argument_name] = float(argument)
    elif not argument:
        return None
    elif not argument.isnumeric():
        raise RuntimeError()


def check_and_process_args(size_params):
    args = add_arguments()
    if not os.path.isfile(args.filepath):
        alarm_message = 'Presented file is not exists'
        return alarm_message
    try:
        check_size_argument_presence_and_value(args.width, 'width', size_params)
        check_size_argument_presence_and_value(args.height, 'height', size_params)
        check_size_argument_presence_and_value(args.scale,
                                               'scale', size_params, arg_type='float')
    except RuntimeError:
        alarm_message = 'Size arguments must be only numeric!'
        return alarm_message
    if any(key in ['width', 'height'] for key in size_params.keys()):
        if 'scale' in size_params.keys():
            alarm_message = 'Incompatible size arguments introduced. '
            alarm_message += 'Need arguments: width or height (or both), or scale only!'
            return alarm_message
    if args.output and not os.path.isdir(args.output):
        alarm_message = 'Path to store output file is not correct!'
        return alarm_message
    return args


def open_image(filepath):
    source_image = Image.open(filepath)
    return source_image


def print_alert(message):
    print(message)


def compute_result_size(source_size, size_params):
    if 'scale' in size_params:
        return (int(source_size['width'] * size_params['scale']),
                int(source_size['height'] * size_params['scale']),)
    if 'width' in size_params and 'height' in size_params:
        print_alert('Scale of source image will not be saved')
        output_size_tuple = (size_params['width'], size_params['height'], )
    if 'width' in size_params:
        height = int((
                        size_params['width'] / source_size['width']
                     ) * source_size['height'])
        output_size_tuple = (size_params['width'], height,)
    if 'height' in size_params:
        width = int((
                        size_params['height'] / source_size['height']
                    ) * source_size['width'])
        output_size_tuple = (width, size_params['height'],)
    return output_size_tuple


def generate_output_size_dict(output_size_tuple, output_size_dict):
    output_size_dict['width'] = output_size_tuple[WIDTH_INDEX]
    output_size_dict['height'] = output_size_tuple[HEIGHT_INDEX]


def resize_image(source_image, source_size, size_params, output_size_dict):
    output_size_tuple = compute_result_size(source_size, size_params)
    generate_output_size_dict(output_size_tuple, output_size_dict)
    resized_image = source_image.resize(output_size_tuple)
    return resized_image


def get_size_from_source_image(source_image):
    size = {}
    size['width'] = source_image.size[WIDTH_INDEX]
    size['height'] = source_image.size[HEIGHT_INDEX]
    return size


def create_output_params_dict(args, output_size_dict):
    output_params_dict = {}
    source_image_dirs, source_image_name = os.path.split(args.filepath)
    source_image_name_part, source_image_ext_part = source_image_name.split('.')
    output_image_name = '{}__{}x{}.{}'.format(
        source_image_name_part,
        output_size_dict['width'],
        output_size_dict['height'],
        source_image_ext_part)
    if not getattr(args, 'output'):
        output_params_dict['output_path'] = source_image_dirs + '/' + output_image_name
        output_params_dict['message'] = 'Image saved at {} as {}'.format(
            source_image_dirs, output_image_name)
    else:
        output_params_dict['output_path'] = args.output + output_image_name
        output_params_dict['message'] = 'Image saved at {} as {}'.format(
            args.output, output_image_name)
    return output_params_dict


def save_image(args, resized_image, output_size_dict):
    output_params_dict = create_output_params_dict(args, output_size_dict)
    resized_image.save(output_params_dict['output_path'])
    return output_params_dict['message']


def process_image(args, size_params):
    output_size_dict = {}
    source_image = open_image(args.filepath)
    source_size = get_size_from_source_image(source_image)
    resized_image = resize_image(source_image,
                                 source_size,
                                 size_params,
                                 output_size_dict)
    source_image.close()
    message = save_image(args, resized_image, output_size_dict)
    return message


if __name__ == '__main__':
    size_params = {}
    args = check_and_process_args(size_params)
    if type(args) == str:
        sys.exit(args)

    message = process_image(args, size_params)
    print_alert(message)


