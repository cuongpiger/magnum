#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os
import sys
import pecan
from typing import Optional
from oslo_config import cfg
from oslo_log import log
from paste import deploy, urlmap
from typing import Dict

import magnum.conf
from magnum.api import config as api_config
from magnum.api import middleware
from magnum.common import config as common_config
from magnum.common import service
from magnum.common.utils import print_debug

CONF = magnum.conf.CONF

LOG = log.getLogger(__name__)


def get_pecan_config() -> pecan.Config:
    """
    Load the configurations for the Pecan Application (`app` variable) from the magnum.api.config file. This application
    will be stored in the pecan.Config object.
    :return : A pecan.Config object that contains the configuration for the Pecan Application.
    """
    # Set up the pecan configuration
    filename = api_config.__file__.replace('.pyc', '.py')  # type: str # get path of the magnum/api/config.py file
    return pecan.configuration.conf_from_file(filename)  # load the configuration into the pecan.Config object


def setup_app(config=None):
    if not config:
        config = get_pecan_config()  # type: pecan.Config

    app_conf = dict(config.app)  # get the user-defined configurations from the `app` variable from the config file
    common_config.set_config_defaults()  # set up CORS middleware, policy for magnum service

    app = pecan.make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        wrap_app=middleware.ParsableErrorMiddleware,
        guess_content_type_from_ext=False,
        **app_conf
    )

    return app


def load_app() -> urlmap.URLMap:
    """
    Try to find the file `api-paste.ini` in the config-option `api_paste_config` to load the WSGI app.
    The `cfg_file` is the path of the `api-paste.ini` file.
    :return: An URLMap object is used to map to the app factory function that we specified in the `api-paste.ini` file.
    """

    cfg_file = None  # type: Optional[str]
    cfg_path = CONF.api.api_paste_config
    if not os.path.isabs(cfg_path):
        cfg_file = CONF.find_file(cfg_path)
    elif os.path.exists(cfg_path):
        cfg_file = cfg_path

    if not cfg_file:
        raise cfg.ConfigFilesNotFoundError([CONF.api.api_paste_config])
    LOG.info("Full WSGI config used: %s", cfg_file)
    return deploy.loadapp("config:" + cfg_file)


def app_factory(global_config: Dict[str, str], **local_conf: dict):
    """
    This function has been called following the order of the field `pipeline` in the `api-paste.ini` file.
    In this case, it is the last function to be called after a series of middleware functions.
    This function will call the function `setup_app()` to load the WSGI app.

    :param global_config: The key-value pairs, including of these values:
        - here: The path of the magnum directory used to run the API server.
        - __file__: The path of api-paste.ini file.
    """

    return setup_app()


def build_wsgi_app(argv=None):
    service.prepare_service(sys.argv)
    return load_app()
