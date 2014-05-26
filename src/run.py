"""
run.py

Runs the parser.

"""

import argparse
import errno

import fnmatch
import os
from vogue import Parser


def mkdirp(path):
    """
    Creates a directory if it doesn't exist. If the path exists, makes sure
    that it isn't a directory.
    """
    assert path

    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.isdir(path):
        raise OSError(errno.EEXIST, "File exists and is not a directory.")
    else:
        pass

    assert os.path.exists(path)


def exit_if_exists(path, msg_prefix):
    """
    Prints an error message and quits, if the path exists.
    """
    msg = "Error: %s %s already exists.\nTo force output, use -f."

    if os.path.exists(path):
        print msg % (msg_prefix, os.path.abspath(path))
        exit(1)


def parse_args():
    """
    Creates the command-line argument parser and parses the arguments.
    """
    parser = argparse.ArgumentParser(
        description='vogue -- automatically externalize styles in HTML files.',
        epilog='Note: vogue does not currently handle psuedo-elements or '
               'pseudo-classes within style tags.')

    parser.add_argument('-c', '--css_path', default='css/extracted.css',
                        help='CSS output filename and path (relative to output_dir). '
                             'Default is "css/extracted.css".')
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help='Write files even if output dir exists. May overwrite existing files in output dir.')
    parser.add_argument('-i', '--input_dir', default='.',
                        help='Specifies the input directory. Default is ".".')
    parser.add_argument('-o', '--output_dir', default='output',
                        help='Specifies the output directory. Default is "./output".')
    parser.add_argument('-p', '--prefix', default='st_',
                        help='Sets the prefix for CSS class names. Must be a '
                             "valid CSS class identifier (omit the leading dot). "
                             'Default is "st_".')

    args = vars(parser.parse_args())
    args['css_path'] = os.path.join(args['output_dir'], args['css_path'])

    return args


def validate_args(args):
    """
    Validates the command-line arguments. Invalid arguments may cause the program
    to exit.
    """
    if not os.path.exists(args['input_dir']):
        print "Input path not found: %s" % args['input_dir']
        exit(1)

    # output_dir and css_path can only exist if --force is used
    if not args['force']:
        exit_if_exists(args['output_dir'], "Output path")
        exit_if_exists(args['css_path'], "CSS output file")

    # create output path or if --force check it exists

    # TODO avoid creating output if stylesheet was empty
    # or create temp files but don't copy
    mkdirp(args['output_dir'])


def process_files(fnames, in_dir, out_dir, prefix, css_path):
    """
    Reads each HTML file in the list and writes updated files to the output
    dir. Writes the CSS output.
    """
    parser = Parser(prefix)

    for fname in fnames:
        in_path = os.path.join(in_dir, fname)
        out_path = os.path.join(out_dir, fname)

        with open(in_path, 'rb') as fin, open(out_path, 'wb') as fout:
            parser.feed(fin.read())
            output = ''.join(parser.out)
            fout.write(output)

    if parser.sty:
        write_css(parser, prefix, css_path)


def write_css(parser, prefix, css_path):
    """
    Writes CSS to a file.
    """
    path, fname = os.path.split(css_path)
    mkdirp(path)
    with open(css_path, 'wb') as sheet:
        sheet.write(parser.stylesheet())


# -----------------------------------------------------------------------------


if __name__ == '__main__':
    args = parse_args()
    validate_args(args)


    fnames = fnmatch.filter(os.listdir(args['input_dir']), '*.html')
    process_files(fnames, args['input_dir'], args['output_dir'], args['prefix'], args['css_path'])