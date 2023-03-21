# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_utils import importutils
from oslo_config import cfg
from types import ModuleType
from typing import Optional

# Try to import Python osprofiler library, return None if this library is not installed on service host.
profiler_opts = importutils.try_import('osprofiler.opts')  # type: Optional[ModuleType]


def register_opts(conf: cfg.ConfigOpts):
    """
    Depends on the user defined config-options inside conf variable, this function will set up osprofiler to satisfy the
    requirements of the service.
    """
    if profiler_opts:  # if osprofiler is installed
        profiler_opts.set_defaults(conf)


def list_opts():
    return {
        profiler_opts._profiler_opt_group: profiler_opts._PROFILER_OPTS
    }
