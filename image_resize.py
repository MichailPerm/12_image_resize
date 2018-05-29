import argparse
from PIL import Image
import os


def get_parser():
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
    return parser


def validate_args(argument_parser):
    args = argument_parser.parse_args()
    if not args.filepath:
        argument_parser.error('Path to image was not presented!')
    if not args.width and not args.height and not args.scale:
        argument_parser.error('Arguments to resize were not presented!')
    if not os.path.isfile(args.filepath):
        argument_parser.error('Presented file is not exists')
    if (args.width or args.height) and args.scale:
        argument_parser.error('Need only scale or width or/and height')
    if args.output and not os.path.isdir(args.output):
        argument_parser.error('Path to store output file is not correct!')
    return args


def open_img(filepath):
    source_img = Image.open(filepath)
    return source_img


def compute_result_size(
        source_width,
        source_height,
        width=None,
        height=None,
        scale=None
):
    if scale:
        return int(source_width * scale), int(source_height * scale)
    if width and height:
        return width, height
    if width:
        height = int((width / source_width) * source_height)
        return width, height
    if height:
        width = int((height / source_height) * source_width)
        return width, height


def generate_output_size_dict(output_size_tuple, output_size_dict):
    output_size_dict['width'], output_size_dict['height'] = output_size_tuple


def resize_img(source_img, output_size_tuple):
    return source_img.resize(output_size_tuple)


def calculate_output_path(args, output_size_tuple):
    source_img_dir, source_img_name = os.path.split(args.filepath)
    source_img_name_part, source_img_ext_part = os.path.splitext(
        source_img_name
    )
    output_img_name = '{}__{}x{}{}'.format(
        source_img_name_part,
        output_size_tuple[0],
        output_size_tuple[1],
        source_img_ext_part)
    if not args.output:
        output_path = os.path.join(
            source_img_dir, output_img_name)
    else:
        output_path = os.path.join(
            args.output, output_img_name)
    return output_path


def is_preserve_aspect_ratio(
        source_width,
        source_height,
        args_width,
        args_height
    ):
    return int(source_width/args_width) == int(source_height/args_height)


if __name__ == '__main__':
    size_params = {}
    argument_parser = get_parser()
    valid_args = validate_args(argument_parser)
    source_img = open_img(valid_args.filepath)
    source_width, source_height = source_img.size
    if valid_args.width and valid_args.height and not is_preserve_aspect_ratio(
        source_width,
        source_height,
        valid_args.width,
        valid_args.height
    ):
        print('Scale of source img will not be saved')
    output_size_tuple = compute_result_size(
        source_width,
        source_height,
        valid_args.width,
        valid_args.height,
        valid_args.scale)
    resized_img = resize_img(source_img, output_size_tuple)
    output_path = calculate_output_path(valid_args, output_size_tuple)
    resized_img.save(output_path)
    print('New file saved as {}'.format(output_path))
