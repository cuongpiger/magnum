"""
FUNCTIONS:
- prepare_service(argv=None)

VARIABLE:
- CONF: cfg.ConfigOpts = magnum.conf.CONF
"""

import magnum.conf
from oslo_log import log as logging
from magnum.common import config
from typing import Optional

CONF = magnum.conf.CONF


def prepare_service(argv: Optional[list] = None):
    """[cuongdm]
    Read configuration file and prepare logging.

    :param argv: list of arguments from command line
    """

    if argv is None:
        argv = []

    logging.register_options(CONF)  # format the log
    config.parse_args(argv)  # read the magnum.conf file and parse to CONF
    config.set_config_defaults()
    logging.setup(CONF, 'magnum')
