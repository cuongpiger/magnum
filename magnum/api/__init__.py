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

import paste.urlmap
from paste.deploy import loadwsgi
from typing import Dict


def root_app_factory(loader: loadwsgi.ConfigLoader, global_conf: Dict[str, str],
                     **local_conf: Dict[str, str]) -> paste.urlmap.URLMap:
    """
    This function is called after the magnum.api.app.load_app() function. It is called by the paste.deploy.loadapp(). It
    will load the other config files, and create the WSGI app. In our scenario based-on api-paste.ini, it will load api
    and healcheck apps to run parallel. Because of specifing the `pipelinee` field in file api-paste.ini, the api will
    run the cors middleware firstly.

    :param loader: The paste.deploy.ConfigLoader object, this tell us where to find the other config files, running
    directory, etc.
    :param global_conf: The key-value pairs, including of these values:
        - here: The path of the magnum directory used to run the API server.
        - __file__: The path of api-paste.ini file.
    :param local_conf: The configuration from the [composite:main] section of the paste config file. In this case, that
    will be "/" (api) and "/healthcheck" (healthcheck).
    """
    return paste.urlmap.urlmap_factory(loader, global_conf, **local_conf)
