"""Naval Fate.

Usage:
  sct_dbtool sanity <db_path>
  sct_dbtool setup
  sct_dbtool (-h | --help)
  sct_dbtool --version

Options:
  -h --help            Show this screen
  --version            Show version
"""
from typing import Dict

import sct_dbtool
from sct_dbtool import api
from sct_dbtool import sanity
from sct_dbtool import setup

from docopt import docopt


def run_sanity(arguments: Dict):
    config = setup.read_setup()
    api_client = api.APIClient.from_config(config)
    sanity.sanity_check(api_client, arguments)


def run_main():
    version = 'sct_dbtool v.{}'.format(sct_dbtool.__version__)
    arguments = docopt(__doc__, version=version)

    if arguments['sanity']:
        run_sanity(arguments)
        return

    if arguments['setup']:
        setup.setup(arguments)
        return


if __name__ == '__main__':
    run_main()
