import argparse
from PIL import Image
import os
import sys


def get_arguments():
    parser = argparse.ArgumentParser(
        epilog='REMEMBER! Too big size or scale may'
               'cause your computer freeze!')
    parser.add_argument(
        '-f', '--filepath', type=open,
        help='path to original img file')
    parser.add_argument(
        '-w', '--width', type=int,
        help='With of result img. Optional. May be the only one.')
    parser.add_argument(
        '-ht', '--height', type=int,
        help='Height of result img. Optional. May be the only one.')
    parser.add_argument(
        '-s', '--scale', type=float,
        help='Scale of result img. Optional. Must be only one!')
    parser.add_argument(
        '-o', '--output',
        help='Path to store result img. Optional.')
    return parser.parse_args()


def check_argument_type_and_value(
        argument,
        argument_name,
        dictionary
):
    if argument:
        dictionary[argument_name] = argument
    elif not argument:
        return None
    elif not argument.isnumeric():
        raise RuntimeError()


def check_size_arguments(args, size_params):
    try:
        check_argument_type_and_value(
            args.width, 'width', size_params)
        check_argument_type_and_value(
            args.height, 'height', size_params)
        check_argument_type_and_value(
            args.scale, 'scale', size_params)
        return None
    except RuntimeError:
        return 'Size arguments must be only numeric!'


def process_args(size_params):
    args = get_arguments()
    if not os.path.isfile(args.filepath):
        return 'Presented file is not exists'
    message = check_size_arguments(args, size_params)
    if message:
        return message
    if any(
            key in ['width', 'height'] for key in size_params.keys()
    ) and 'scale' in size_params.keys():
        return 'Need only scale or width or/and height'
    if args.output and not os.path.isdir(args.output):
        return 'Path to store output file is not correct!'
    return args


def open_img(filepath):
    source_img = Image.open(filepath)
    return source_img


def print_alert(message):
    print(message)


def compute_result_size(source_size, size_params):
    if 'scale' in size_params:
        return (int(source_size['width'] * size_params['scale']),
                int(source_size['height'] * size_params['scale']),)
    if 'width' in size_params and 'height' in size_params:
        print_alert('Scale of source img will not be saved')
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
    output_size_dict['width'], output_size_dict['height'] = output_size_tuple


def resize_img(source_img, source_size, size_params, output_size_dict):
    output_size_tuple = compute_result_size(source_size, size_params)
    generate_output_size_dict(output_size_tuple, output_size_dict)
    resized_img = source_img.resize(output_size_tuple)
    return resized_img


def get_size_from_source_img(source_img):
    size = {}
    size['width'], size['height'] = source_img.size
    return size


def create_output_params_dict(args, output_size_dict):
    output_params_dict = {}
    source_img_dirs, source_img_name = os.path.split(args.filepath)
    source_img_name_part, source_img_ext_part = source_img_name.split('.')
    output_img_name = '{}__{}x{}.{}'.format(
        source_img_name_part,
        output_size_dict['width'],
        output_size_dict['height'],
        source_img_ext_part)
    if not getattr(args, 'output'):
        output_params_dict['output_path'] = os.path.join(
            source_img_dirs, output_img_name)
        output_params_dict['message'] = 'img saved at {} as {}'.format(
            source_img_dirs, output_img_name)
    else:
        output_params_dict['output_path'] = os.path.join(
            args.output, output_img_name)
        output_params_dict['message'] = 'img saved at {} as {}'.format(
            args.output, output_img_name)
    return output_params_dict


def save_img(args, resized_img, output_size_dict):
    output_params_dict = create_output_params_dict(args, output_size_dict)
    resized_img.save(output_params_dict['output_path'])
    return output_params_dict['message']


def process_img(args, size_params):
    output_size_dict = {}
    source_img = open_img(args.filepath)
    source_size = get_size_from_source_img(source_img)
    resized_img = resize_img(source_img,
                             source_size,
                             size_params,
                             output_size_dict)
    source_img.close()
    message = save_img(args, resized_img, output_size_dict)
    return message


if __name__ == '__main__':
    size_params = {}
    args = process_args(size_params)
    if type(args) == str:
        sys.exit(args)
    message = process_img(args, size_params)
    print_alert(message)
