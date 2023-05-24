# Copyright 2012 New Dream Network, LLC (DreamHost)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pecan
from pecan import rest
from wsme import types as wtypes

from magnum.api.controllers import base
from magnum.api.controllers import link
from magnum.api.controllers import v1
from magnum.api.controllers import versions
from magnum.api import expose
from typing import List


class Version(base.APIBase):
    """An API version representation."""

    id = wtypes.text
    """The ID of the version, also acts as the release number"""

    links = [link.Link]
    """A Link that point to a specific version of the API"""

    status = wtypes.text
    """The current status of the version: CURRENT, SUPPORTED, UNSUPPORTED"""

    max_version = wtypes.text
    """The max microversion supported by this version"""

    min_version = wtypes.text
    """The min microversion supported by this version"""

    @staticmethod
    def convert(id_: str, status: str, max_: str, min_: str):
        version = Version()
        version.id = id_
        version.links = [link.Link.make_link('self', pecan.request.host_url, id_, '', bookmark=True)]
        version.status = status
        version.max_version = max_
        version.min_version = min_

        return version


class Root(base.APIBase):
    name = wtypes.text
    """The name of the API"""

    description = wtypes.text
    """Some information about this API"""

    versions = [Version]
    """Links to all the versions available in this API"""

    @staticmethod
    def convert():
        root = Root()
        root.name = "OpenStack Magnum API"
        root.description = "Magnum is an OpenStack project which aims to provide container cluster management."
        root.versions = [Version.convert('v1', "CURRENT", versions.CURRENT_MAX_VER, versions.BASE_VER)]
        return root


class RootController(rest.RestController):
    """[cuongdm]
    Root controller for the Magnum API. All the requests must go through this controller.

    ...
    Attributes
    ----------
    _versions : List[str]
        All supported API versions
    _default_version : str
        The default API version
    v1 : v1.Controller
        The controller for the v1 API version because of all the requests always start with /v1
    """

    _versions: List[str] = ['v1']
    _default_version: str = 'v1'
    v1 = v1.Controller()

    @expose.expose(Root)
    def get(self):
        # NOTE: The reason why convert() it's being called for every
        #       request is because we need to get the host url from
        #       the request object to make the links.
        return Root.convert()

    @pecan.expose()
    def _route(self, args: List[str]):
        """Overrides the default routing behavior. It redirects the request to the default version of the magnum API if
        the version number is not specified in the url.

        Parameters
        ----------
        args : List[str]
            The list of arguments in the url, for example if your URL is /v1/clusters, then args = ['v1', 'clusters']
        """

        if args[0] and args[0] not in self._versions:
            args = [self._default_version] + args
        return super(RootController, self)._route(args)
