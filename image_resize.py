import argparse
from PIL import Image
import os
import sys


def get_arguments():
    parser = argparse.ArgumentParser(
        epilog='REMEMBER! Too big size or scale may'
               'cause your computer freeze!')
    parser.add_argument(
        '-f', '--filepath',
        help='path to original img file')
    parser.add_argument(
        '-w', '--width',
        type=int,
        help='With of result img. Optional. May be the only one.')
    parser.add_argument(
        '-ht', '--height',
        type=int,
        help='Height of result img. Optional. May be the only one.')
    parser.add_argument(
        '-s', '--scale',
        type=float,
        help='Scale of result img. Optional. Must be only one!')
    parser.add_argument(
        '-o', '--output',
        help='Path to store result img. Optional.')
    return parser.parse_args()


def check_paths(args):
    if not os.path.isfile(args.filepath):
        return 'Presented file is not exists'
    if args.output and not os.path.isdir(args.output):
        return 'Path to store output file is not correct!'
    return None


def open_img(filepath):
    source_img = Image.open(filepath)
    return source_img


def compute_result_size(source_size, args):
    if args.scale:
        return tuple([int(source_size['width'] * args.scale),
                      int(source_size['height'] * args.scale)])
    if args.width and args.height:
        return tuple([args.width, args.height])
    if args.width:
        height = int((
                        args.width / source_size['width']
                     ) * source_size['height'])
        return tuple([args.width, height])
    if args.height:
        width = int((
                        args.height / source_size['height']
                    ) * source_size['width'])
        return tuple([width, args.height])


def generate_output_size_dict(output_size_tuple, output_size_dict):
    output_size_dict['width'], output_size_dict['height'] = output_size_tuple


def resize_img(source_img, source_size, args, output_size_dict):
    output_size_tuple = compute_result_size(source_size, args)
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


def process_img(args):
    output_size_dict = {}
    source_img = open_img(args.filepath)
    source_size = get_size_from_source_img(source_img)
    resized_img = resize_img(source_img,
                             source_size,
                             args,
                             output_size_dict)
    source_img.close()
    message = save_img(args, resized_img, output_size_dict)
    return message


if __name__ == '__main__':
    size_params = {}
    args = get_arguments()
    if args.width or args.height:
        if args.scale:
            sys.exit('Need only scale or width or/and height')
        print('Scale of source img will not be saved')
    result = check_paths(args)
    if result:
        sys.exit(result)
    message = process_img(args)
    print(message)
