# parse.py
from argparse import ArgumentParser
from __main__ import __doc__ as description


def _parse_args(add_args=None):
    """
    Parse args using `argparse` in order to fullfil requirements.
    """

    parser = ArgumentParser(description=description)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true",
                       help="Increase output verbosity")
    group.add_argument("-q", "--quiet", action="store_true",
                       help="Decrease output verbosity")
    parser.add_argument("-H", "--host", type=str, default="localhost",
                        help="service IP address")
    parser.add_argument("-p", "--port", type=int,
                        default=4321, help="service port")

    if add_args is not None:
        add_args(parser)
    return parser.parse_args()


def _add_name_arg(parser):
    parser.add_argument("-n", "--name", type=str,
                        required=True, help="file name")


def _args_upload(parser):
    _add_name_arg(parser)
    parser.add_argument("-d", "--dst", type=str,
                        required=True, help="destination file path")


def parse_args_upload():
    return _parse_args(_args_upload)


def _args_download(parser):
    _add_name_arg(parser)
    parser.add_argument("-s", "--src", type=str, help="source file path")


def parse_args_download():
    return _parse_args(_args_download)


def _args_list(parser):
    # parser.add_argument() Agregar argumentos para ls?
    pass


def parse_args_list():
    return _parse_args(_args_list)
