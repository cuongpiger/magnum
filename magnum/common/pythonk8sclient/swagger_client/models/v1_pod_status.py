# coding: utf-8

"""
Copyright 2015 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from pprint import pformat
from six import iteritems


class V1PodStatus(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Swagger model

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'phase': 'str',
            'conditions': 'list[V1PodCondition]',
            'message': 'str',
            'reason': 'str',
            'host_ip': 'str',
            'pod_ip': 'str',
            'start_time': 'str',
            'container_statuses': 'list[V1ContainerStatus]'
        }

        self.attribute_map = {
            'phase': 'phase',
            'conditions': 'conditions',
            'message': 'message',
            'reason': 'reason',
            'host_ip': 'hostIP',
            'pod_ip': 'podIP',
            'start_time': 'startTime',
            'container_statuses': 'containerStatuses'
        }

        self._phase = None
        self._conditions = None
        self._message = None
        self._reason = None
        self._host_ip = None
        self._pod_ip = None
        self._start_time = None
        self._container_statuses = None

    @property
    def phase(self):
        """
        Gets the phase of this V1PodStatus.
        current condition of the pod; see http://releases.k8s.io/v1.0.4/docs/pod-states.md#pod-phase

        :return: The phase of this V1PodStatus.
        :rtype: str
        """
        return self._phase

    @phase.setter
    def phase(self, phase):
        """
        Sets the phase of this V1PodStatus.
        current condition of the pod; see http://releases.k8s.io/v1.0.4/docs/pod-states.md#pod-phase

        :param phase: The phase of this V1PodStatus.
        :type: str
        """
        self._phase = phase

    @property
    def conditions(self):
        """
        Gets the conditions of this V1PodStatus.
        current service state of pod; see http://releases.k8s.io/v1.0.4/docs/pod-states.md#pod-conditions

        :return: The conditions of this V1PodStatus.
        :rtype: list[V1PodCondition]
        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        """
        Sets the conditions of this V1PodStatus.
        current service state of pod; see http://releases.k8s.io/v1.0.4/docs/pod-states.md#pod-conditions

        :param conditions: The conditions of this V1PodStatus.
        :type: list[V1PodCondition]
        """
        self._conditions = conditions

    @property
    def message(self):
        """
        Gets the message of this V1PodStatus.
        human readable message indicating details about why the pod is in this condition

        :return: The message of this V1PodStatus.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this V1PodStatus.
        human readable message indicating details about why the pod is in this condition

        :param message: The message of this V1PodStatus.
        :type: str
        """
        self._message = message

    @property
    def reason(self):
        """
        Gets the reason of this V1PodStatus.
        (brief-CamelCase) reason indicating details about why the pod is in this condition

        :return: The reason of this V1PodStatus.
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """
        Sets the reason of this V1PodStatus.
        (brief-CamelCase) reason indicating details about why the pod is in this condition

        :param reason: The reason of this V1PodStatus.
        :type: str
        """
        self._reason = reason

    @property
    def host_ip(self):
        """
        Gets the host_ip of this V1PodStatus.
        IP address of the host to which the pod is assigned; empty if not yet scheduled

        :return: The host_ip of this V1PodStatus.
        :rtype: str
        """
        return self._host_ip

    @host_ip.setter
    def host_ip(self, host_ip):
        """
        Sets the host_ip of this V1PodStatus.
        IP address of the host to which the pod is assigned; empty if not yet scheduled

        :param host_ip: The host_ip of this V1PodStatus.
        :type: str
        """
        self._host_ip = host_ip

    @property
    def pod_ip(self):
        """
        Gets the pod_ip of this V1PodStatus.
        IP address allocated to the pod; routable at least within the cluster; empty if not yet allocated

        :return: The pod_ip of this V1PodStatus.
        :rtype: str
        """
        return self._pod_ip

    @pod_ip.setter
    def pod_ip(self, pod_ip):
        """
        Sets the pod_ip of this V1PodStatus.
        IP address allocated to the pod; routable at least within the cluster; empty if not yet allocated

        :param pod_ip: The pod_ip of this V1PodStatus.
        :type: str
        """
        self._pod_ip = pod_ip

    @property
    def start_time(self):
        """
        Gets the start_time of this V1PodStatus.
        RFC 3339 date and time at which the object was acknowledged by the Kubelet.  This is before the Kubelet pulled the container image(s) for the pod.

        :return: The start_time of this V1PodStatus.
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Sets the start_time of this V1PodStatus.
        RFC 3339 date and time at which the object was acknowledged by the Kubelet.  This is before the Kubelet pulled the container image(s) for the pod.

        :param start_time: The start_time of this V1PodStatus.
        :type: str
        """
        self._start_time = start_time

    @property
    def container_statuses(self):
        """
        Gets the container_statuses of this V1PodStatus.
        list of container statuses; see http://releases.k8s.io/v1.0.4/docs/pod-states.md#container-statuses

        :return: The container_statuses of this V1PodStatus.
        :rtype: list[V1ContainerStatus]
        """
        return self._container_statuses

    @container_statuses.setter
    def container_statuses(self, container_statuses):
        """
        Sets the container_statuses of this V1PodStatus.
        list of container statuses; see http://releases.k8s.io/v1.0.4/docs/pod-states.md#container-statuses

        :param container_statuses: The container_statuses of this V1PodStatus.
        :type: list[V1ContainerStatus]
        """
        self._container_statuses = container_statuses

    def to_dict(self):
        """
        Return model properties dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Return model properties str
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()