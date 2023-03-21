# Copyright 2013 - Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_log import log as logging
from typing import List, Optional

from magnum.common import config
import magnum.conf

CONF = magnum.conf.CONF


def prepare_service(argv: Optional[List[str]] = None):
    """
    Prepare a service for launch. Includes parsing the config file to CONF variable, setting up logging, and preparing
    for the messaging and notification subsystems.
    :param argv: List of command line arguments when launching the program.
    """
    if argv is None:
        argv = []

    logging.register_options(CONF)  # call this method with `CONF` before parsing any application CLI options
    config.parse_args(argv)
    config.set_config_defaults()

    logging.setup(CONF, 'magnum')
