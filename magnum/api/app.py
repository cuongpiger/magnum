"""
FUNCTIONS:
- build_wsgi_app(argv=None)
- load_app()
- app_factory(global_config, **local_conf)
- setup_app(config=None)
- get_pecan_config() -> pecan.configuration.Config
"""

import os
import sys
import pecan
import magnum.conf
from oslo_config import cfg
from oslo_log import log
from paste import deploy, urlmap
from typing import Optional
from magnum.common import profiler
from magnum.api import config as api_config
from magnum.api import middleware
from magnum.common import config as common_config
from magnum.common import service

CONF: cfg.ConfigOpts = magnum.conf.CONF
LOG = log.getLogger(__name__)


def get_pecan_config() -> pecan.configuration.Config:
    """
    [cuongdm]
    Set up the Pecan configuration including the pecan configuration file
    """
    filename = api_config.__file__.replace('.pyc', '.py')
    LOG.debug("Using Pecan config file %s" % filename)
    config: pecan.configuration.Config = pecan.configuration.conf_from_file(filename)
    return config


def setup_app(config=None):
    if not config:
        config = get_pecan_config()

    app_conf = dict(config.app)
    common_config.set_config_defaults()

    app = pecan.make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        wrap_app=middleware.ParsableErrorMiddleware,
        guess_content_type_from_ext=False,
        **app_conf
    )

    return app


def load_app() -> urlmap.URLMap:
    """[cuongdm]
    Read the api-paste.ini file and return the WSGI app

    return: WSGI application
    """
    cfg_file: Optional[str] = None
    cfg_path: str = CONF.api.api_paste_config  # get the api-paste.ini file from magnum.conf
    if not os.path.isabs(cfg_path):
        cfg_file = CONF.find_file(cfg_path)
    elif os.path.exists(cfg_path):
        cfg_file = cfg_path

    if not cfg_file:
        raise cfg.ConfigFilesNotFoundError([CONF.api.api_paste_config])

    LOG.info("The WSGI config file is at %s", cfg_file)
    wsgi_app: urlmap.URLMap = deploy.loadapp("config:" + cfg_file)
    return wsgi_app


def app_factory(global_config, **local_conf):
    app = setup_app()
    return app


def build_wsgi_app(argv=None) -> urlmap.URLMap:
    """[cuongdm]
    Build the WSGI app and return it.
    """
    service.prepare_service(sys.argv)  # set up logging and config variables
    wsgi_app = load_app()
    profiler.setup('magnum-api', CONF.host)  # set up OSprofiler plugins
    return wsgi_app
