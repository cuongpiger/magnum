# Copyright 2014 - Rackspace Hosting
#
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

"""Common RPC service and API tools for Magnum."""

import oslo_messaging as messaging
from oslo_service import service

from magnum.common import profiler
from magnum.common import rpc
import magnum.conf
from magnum.common.utils import print_debug
from magnum.objects import base as objects_base
from magnum.service import periodic
from magnum.servicegroup import magnum_service_periodic as servicegroup
from oslo_log import log as logging

CONF = magnum.conf.CONF
LOG = logging.getLogger(__name__)


class Service(service.Service):

    def __init__(self, topic: str, server: str, handlers: list, binary: str):
        """[cuongdm]
        Constructor of the RPC service.

        Parameters
        ----------
        topic : str
            The topic of the Message Queue service that you want to subscribe to.
        server : str
            A rondom string that is used to identify the RPC service.
        handlers : list
            A list of handlers that are used to handle the RPC service.
        binary : str
            The service name of the RPC service, this parameter is used by OSprofiler.
        """
        super(Service, self).__init__()
        # TODO(asalkeld) add support for version='x.y'
        target: messaging.Target = messaging.Target(topic=topic, server=server)
        self._server = rpc.get_server(target, handlers, serializer=objects_base.MagnumObjectSerializer())

        self.binary = binary
        profiler.setup(binary, CONF.host)
        LOG.debug('Created RPC server for service %(service)s on host %(host)s.',
                  {'service': self.binary, 'host': CONF.host})

    def start(self):
        self._server.start()

    def create_periodic_tasks(self):
        if CONF.periodic_enable:
            periodic.setup(CONF, self.tg)
        servicegroup.setup(CONF, self.binary, self.tg)

    def stop(self):
        if self._server:
            self._server.stop()
            self._server.wait()
        super(Service, self).stop()

    @classmethod
    def create(cls, topic: str, server: str, handlers: list, binary: str) -> 'Service':
        """[cuongdm]
        This method is used to create the RPC service.

        Parameters
        ----------
        topic : str
            The topic of the RPC service that you want to subscribe to.
        server : str
            A rondom string that is used to identify the RPC service.
        handlers : list
            A list of handlers that are used to handle the RPC service.
        binary : str
            The service name of the RPC service, this parameter is used by OSprofiler.

        Returns
        -------
        Service
            The RPC :class:`Service` object.
        """

        service_obj = cls(topic, server, handlers, binary)
        return service_obj


class API(object):
    def __init__(self, context=None, topic=None, server=None,
                 timeout=None):
        self._context = context
        if topic is None:
            topic = ''
        target = messaging.Target(topic=topic, server=server)
        self._client = rpc.get_client(
            target,
            serializer=objects_base.MagnumObjectSerializer(),
            timeout=timeout
        )

    def _call(self, method, *args, **kwargs):
        return self._client.call(self._context, method, *args, **kwargs)

    def _cast(self, method, *args, **kwargs):
        self._client.cast(self._context, method, *args, **kwargs)

    def echo(self, message):
        self._cast('echo', message=message)
