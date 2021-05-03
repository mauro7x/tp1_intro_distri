from argparse import ArgumentParser
from __main__ import __doc__ as description


def parse_args():
    """
    Parse args using `argparse` in order to fullfil requirements.
    """

    parser = ArgumentParser(description=description)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true",
                       help="Increase output verbosity")
    group.add_argument("-q", "--quiet", action="store_true",
                       help="Decrease output verbosity")
    parser.add_argument("-H", "--host", type=str, required=True,
                        help="service IP address")
    parser.add_argument("-p", "--port", type=str,
                        required=True, help="service port")

    return parser.parse_args()
