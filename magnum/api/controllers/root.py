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
from magnum.common.utils import print_debug


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
    def convert(id, status, max, min):
        print_debug("Version.convert called: id = %s" % id)
        version = Version()
        version.id = id
        version.links = [link.Link.make_link('self', pecan.request.host_url,
                                             id, '', bookmark=True)]
        version.status = status
        version.max_version = max
        version.min_version = min
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
        print_debug("Root.convert called")
        root = Root()
        root.name = "OpenStack Magnum API"
        root.description = ("Magnum is an OpenStack project which aims to "
                            "provide container cluster management.")
        root.versions = [Version.convert('v1', "CURRENT",
                                         versions.CURRENT_MAX_VER,
                                         versions.BASE_VER)]
        return root


class RootController(rest.RestController):
    """
    RootController is the single entrypoint of the Pecan application, which can be considered as the root URL path of
    the application. It is responsible for routing the request to the appropriate controller based on the version. In
    this scenario, the root URL path is http://localhost:8080/v1 (dev-env).
    Pecan application used the object distributed routing mechanism to process the request.
    """

    _versions = ['v1']  # all supported API versions

    _default_version = 'v1'  # the default API version

    v1 = v1.Controller()

    @expose.expose(Root)
    def get(self):
        # NOTE: The reason why convert() it's being called for every
        #       request is because we need to get the host url from
        #       the request object to make the links.
        print_debug("RootController.get called")
        self.convert = Root.convert()
        return self.convert

    @pecan.expose()
    def _route(self, args):
        """
        Overrides the default routing behavior.
        Routes a request to the appropriate controller and returns its result. Performs a bit of validation - refuses to
        route delete and put actions via a GET request.
        It redirects the request to the default version of the magnum API if the version number is not specified in the
        url.
        """
        print_debug("RootController._route called")
        if args[0] and args[0] not in self._versions:
            args = [self._default_version] + args
        return super(RootController, self)._route(args)
