from gevent import monkey

monkey.patch_all()  # noqa

import argparse
import logging

from flaskiva import server

__all__ = [
    'main',
]


def get_arg_parser():
    """
    Get shell argument parser.
    """
    parser = argparse.ArgumentParser(
        description='Entrypoint for pies.'
    )

    parser.add_argument('config', help='config file')
    parser = server.get_arg_parser()

    return parser


def main():
    """
    Pies main entry point.
    """
    parser = get_arg_parser()

    args = parser.parse_args()
    app_config = server.load_config(args)

    app = server.create_app(
        args,
        'pies.web',
        static_folder=None,
        config=app_config
    )

    logging.getLogger("requests").setLevel(logging.WARNING)

    server.run(args, app)


if __name__ == '__main__':
    main()
