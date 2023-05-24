"""
CLASSES:
* Validator
    - Methods:
        + get_coe_validator(cls, coe: str) -> Union['K8sValidator', 'SwarmValidator', Exception]

"""

import pecan
import decorator
import magnum.conf

from keystoneauth1 import exceptions as ka_exception
from typing import Set, Union, List, Tuple

from magnum import objects
from magnum.i18n import _
from magnum.common import clients
from magnum.common import exception
from magnum.drivers.common import driver
from magnum.api import utils as api_utils

CONF = magnum.conf.CONF

cluster_update_allowed_properties: Set[str] = {'node_count', 'health_status', 'health_status_reason'}
federation_update_allowed_properties: Set[str] = {'member_ids', 'properties'}


def ct_not_found_to_bad_request():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exception.ClusterTemplateNotFound as e:
            # Change error code because 404 (NotFound) is inappropriate
            # response for a POST request to create a Cluster
            e.code = 400  # BadRequest
            raise

    return wrapper


def enforce_cluster_type_supported():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        cluster = args[1]
        cluster_template = objects.ClusterTemplate.get(
            pecan.request.context, cluster.cluster_template_id)
        cluster_type = (cluster_template.server_type,
                        cluster_template.cluster_distro,
                        cluster_template.coe)
        driver.Driver.get_driver(*cluster_type)
        return func(*args, **kwargs)

    return wrapper


def enforce_driver_supported():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        cluster_template = args[1]
        cluster_distro = cluster_template.cluster_distro
        if not cluster_distro:
            try:
                cli = clients.OpenStackClients(pecan.request.context)
                image_id = cluster_template.image_id
                image = api_utils.get_openstack_resource(cli.glance().images,
                                                         image_id,
                                                         'images')
                cluster_distro = image.get('os_distro')
            except Exception:
                pass
        cluster_type = (cluster_template.server_type,
                        cluster_distro,
                        cluster_template.coe)
        driver.Driver.get_driver(*cluster_type)
        return func(*args, **kwargs)

    return wrapper


def enforce_cluster_volume_storage_size():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        cluster = args[1]
        cluster_template = objects.ClusterTemplate.get(
            pecan.request.context, cluster.cluster_template_id)
        _enforce_volume_storage_size(
            cluster_template.as_dict(), cluster.as_dict())
        return func(*args, **kwargs)

    return wrapper


def enforce_valid_project_id_on_create():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        quota = args[1]
        _validate_project_id(quota.project_id)
        return func(*args, **kwargs)

    return wrapper


def _validate_project_id(project_id):
    try:
        context = pecan.request.context
        osc = clients.OpenStackClients(context)
        osc.keystone().domain_admin_client.projects.get(project_id)
    except ka_exception.http.NotFound:
        raise exception.ProjectNotFound(name='project_id',
                                        id=project_id)


def enforce_network_driver_types_create():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        cluster_template = args[1]
        _enforce_network_driver_types(cluster_template)
        return func(*args, **kwargs)

    return wrapper


def enforce_network_driver_types_update():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        cluster_template_ident = args[1]
        patch = args[2]
        cluster_template = api_utils.get_resource('ClusterTemplate',
                                                  cluster_template_ident)
        try:
            cluster_template_dict = api_utils.apply_jsonpatch(
                cluster_template.as_dict(), patch)
        except api_utils.JSONPATCH_EXCEPTIONS as e:
            raise exception.PatchError(patch=patch, reason=e)
        cluster_template = objects.ClusterTemplate(pecan.request.context,
                                                   **cluster_template_dict)
        _enforce_network_driver_types(cluster_template)
        return func(*args, **kwargs)

    return wrapper


def _enforce_network_driver_types(cluster_template):
    validator = Validator.get_coe_validator(cluster_template.coe)
    if not cluster_template.network_driver:
        cluster_template.network_driver = validator.default_network_driver
    validator.validate_network_driver(cluster_template.network_driver)


def enforce_server_type():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        cluster_template = args[1]
        _enforce_server_type(cluster_template)
        return func(*args, **kwargs)

    return wrapper


def _enforce_server_type(cluster_template):
    validator = Validator.get_coe_validator(cluster_template.coe)
    validator.validate_server_type(cluster_template.server_type)


def enforce_volume_driver_types_create():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        cluster_template = args[1]
        _enforce_volume_driver_types(cluster_template.as_dict())
        return func(*args, **kwargs)

    return wrapper


def enforce_volume_storage_size_create():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        cluster_template = args[1]
        _enforce_volume_storage_size(cluster_template.as_dict(), {})
        return func(*args, **kwargs)

    return wrapper


def enforce_volume_driver_types_update():
    @decorator.decorator
    def wrapper(func, *args, **kwargs):
        cluster_template_ident = args[1]
        patch = args[2]
        cluster_template = api_utils.get_resource('ClusterTemplate',
                                                  cluster_template_ident)
        try:
            cluster_template_dict = api_utils.apply_jsonpatch(
                cluster_template.as_dict(), patch)
        except api_utils.JSONPATCH_EXCEPTIONS as e:
            raise exception.PatchError(patch=patch, reason=e)
        _enforce_volume_driver_types(cluster_template_dict)
        return func(*args, **kwargs)

    return wrapper


def _enforce_volume_driver_types(cluster_template):
    validator = Validator.get_coe_validator(cluster_template['coe'])
    if not cluster_template.get('volume_driver'):
        return
    validator.validate_volume_driver(cluster_template['volume_driver'])


def _enforce_volume_storage_size(cluster_template, cluster):
    volume_size = cluster.get('docker_volume_size') \
                  or cluster_template.get('docker_volume_size')
    storage_driver = cluster_template.get('docker_storage_driver')

    if storage_driver == 'devicemapper':
        if not volume_size or volume_size < 3:
            raise exception.InvalidParameterValue(
                'docker volume size %s GB is not valid, '
                'expecting minimum value 3GB for %s storage '
                'driver.' % (volume_size, storage_driver))


def validate_cluster_properties(delta):
    update_disallowed_properties = delta - cluster_update_allowed_properties
    if update_disallowed_properties:
        err = (_("cannot change cluster property(ies) %s.") %
               ", ".join(update_disallowed_properties))
        raise exception.InvalidParameterValue(err=err)


def validate_federation_properties(delta):
    update_disallowed_properties = delta - federation_update_allowed_properties
    if update_disallowed_properties:
        err = (_("cannot change federation property(ies) %s.") %
               ", ".join(update_disallowed_properties))
        raise exception.InvalidParameterValue(err=err)


class Validator(object):
    """[cuongdm]
    Validator for validating cluster template.
    """

    @classmethod
    def get_coe_validator(cls, coe: str) -> Union['K8sValidator', 'SwarmValidator', Exception]:
        """[cuongdm] Get validator for `coe` type

        Parameters
        ----------
        coe : str
            COE type, such as kubernetes, swarm, swarm-mode, etc.

        Raises
        ------
        exception.InvalidParameterValue
            If COE type is not supported.
        """
        if coe == 'kubernetes':
            return K8sValidator()
        elif coe == 'swarm' or coe == 'swarm-mode':
            return SwarmValidator()
        else:
            raise exception.InvalidParameterValue(
                _('Requested COE type %s is not supported.') % coe)

    @classmethod
    def validate_network_driver(cls, network_driver: str):
        """[cuongdm]
        Validate network driver type that admins can use for this COE, including supported and allowed network drivers.

        Parameters
        ----------
        network_driver : str
            Network driver type, such as `flannel`, `calico`, etc.

        Raises
        ------
        exception.InvalidParameterValue
            If network driver is not supported or allowed.
        """

        cls._validate_network_driver_supported(network_driver)
        cls._validate_network_driver_allowed(network_driver)

    @classmethod
    def _validate_network_driver_supported(cls, network_driver: str):
        """[cuongdm]
        Confirm that driver is supported by Magnum for this COE.

        Parameters
        ----------
        network_driver : str
            Network driver type, such as `flannel`, `calico`, etc.

        Raises
        ------
        exception.InvalidParameterValue
            If network driver is not supported.
        """

        if network_driver not in cls.supported_network_drivers:  # noqa
            raise exception.InvalidParameterValue(
                _('Network driver type %(driver)s is not supported, expecting a %(supported_drivers)s network driver.')
                % {'driver': network_driver,
                   'supported_drivers': '/'.join(cls.supported_network_drivers + ['unspecified'])})  # noqa

    @classmethod
    def _validate_network_driver_allowed(cls, network_driver: str):
        """[cuongdm]
        Confirm that driver is allowed via configuration for this COE.

        Parameters
        ----------
        network_driver : str
            Network driver type, such as `flannel`, `calico`, etc.

        Raises
        ------
        exception.InvalidParameterValue
            If network driver is not allowed.
        """

        if ('all' not in cls.allowed_network_drivers and network_driver not in cls.allowed_network_drivers):  # noqa
            raise exception.InvalidParameterValue(
                _('Network driver type %(driver)s is not allowed, expecting a %(allowed_drivers)s network driver. ')
                % {'driver': network_driver,
                   'allowed_drivers': '/'.join(cls.allowed_network_drivers + ['unspecified'])})  # noqa

    @classmethod
    def validate_volume_driver(cls, volume_driver: str):
        """[cuongdm]
        Validate volume driver type that admins can support for this COE.

        Parameters
        ----------
        volume_driver : str
            Volume driver type, such as `rexray`, `cinder`, etc.

        Raises
        ------
        exception.InvalidParameterValue
            If volume driver is not supported.
        """
        cls._validate_volume_driver_supported(volume_driver)

    @classmethod
    def _validate_volume_driver_supported(cls, volume_driver: str):
        """[cuongdm]
        Confirm that volume driver is supported by Magnum for this COE.

        Parameters
        ----------
        volume_driver : str
            Volume driver type, such as `rexray`, `cinder`, etc.

        Raises
        ------
        exception.InvalidParameterValue
            If volume driver is not supported.
        """

        if volume_driver not in cls.supported_volume_driver:  # noqa
            raise exception.InvalidParameterValue(
                _('Volume driver type %(driver)s is not supported, '
                  'expecting a %(supported_volume_driver)s volume driver.') % {
                    'driver': volume_driver,
                    'supported_volume_driver': '/'.join(
                        cls.supported_volume_driver + ['unspecified'])})  # noqa

    @classmethod
    def validate_server_type(cls, server_type: str):
        """[cuongdm]
        Validate server type that admins can support for this COE.

        Parameters
        ----------
        server_type : str
            Server type, such as `vm` for virtual machine, `bm` for bare metal.

        Raises
        ------
        exception.InvalidParameterValue
            If server type is not supported.
        """
        cls._validate_server_type(server_type)

    @classmethod
    def _validate_server_type(cls, server_type: str):
        """[cuongdm]
        Confirm that server type is supported by Magnum for this COE.

        Parameters
        ----------
        server_type : str
            Server type, such as `vm` for virtual machine, `bm` for bare metal.

        Raises
        ------
        exception.InvalidParameterValue
            If server type is not supported.
        """
        if server_type not in cls.supported_server_types:  # noqa
            raise exception.InvalidParameterValue(
                _('Server type %(server_type)s is not supported, ''expecting a %(supported_server_types)s server type.')
                % {'server_type': server_type, 'supported_server_types': '/'.join(
                    cls.supported_server_types + ['unspecified'])})  # noqa


class K8sValidator(Validator):
    """[cuongdm]
    Validator for validating Kubernetes cluster template.

    Attributes
    ----------
    supported_network_drivers : List[str]
        List of supported network drivers.
    supported_server_types : List[str]
        List of supported server types, such as `vm` for virtual machine, `bm` for bare metal.
    supported_volume_driver : List[str]
        List of supported volume drivers.
    allowed_network_drivers : Tuple[str]
        List of allowed network drivers that admins can configure in magnum.conf.
    default_network_driver : str
        Default network driver that admins can configure in magnum.conf. It is used when clients do not specify.
    """

    supported_network_drivers: List[str] = ['flannel', 'calico']
    supported_server_types: List[str] = ['vm', 'bm']
    supported_volume_driver: List[str] = ['cinder']
    allowed_network_drivers: Tuple[str] = (
        CONF.cluster_template.kubernetes_allowed_network_drivers)
    default_network_driver: str = (
        CONF.cluster_template.kubernetes_default_network_driver)


class SwarmValidator(Validator):
    """[cuongdm]
    Validator for validating Swarm cluster template.

    Attributes
    ----------
    supported_network_drivers : List[str]
        List of supported network drivers.
    supported_server_types : List[str]
        List of supported server types, such as `vm` for virtual machine, `bm` for bare metal.
    supported_volume_driver : List[str]
        List of supported volume drivers. For Swarm, it is `rexray`.
    allowed_network_drivers : Tuple[str]
        List of allowed network drivers that admins can configure in magnum.conf.
    default_network_driver : str
        Default network driver that admins can configure in magnum.conf. It is used when clients do not specify.
    """

    supported_network_drivers: List[str] = ['docker', 'flannel']
    supported_server_types: List[str] = ['vm', 'bm']
    supported_volume_driver: List[str] = ['rexray']
    allowed_network_drivers: Tuple[str] = (
        CONF.cluster_template.swarm_allowed_network_drivers)
    default_network_driver: str = (
        CONF.cluster_template.swarm_default_network_driver)


class MesosValidator(Validator):
    """[cuongdm]
    Validator for validating Mesos cluster template.

    Attributes
    ----------
    supported_network_drivers : List[str]
        List of supported network drivers.
    supported_server_types : List[str]
        List of supported server types, such as `vm` for virtual machine, `bm` for bare metal.
    supported_volume_driver : List[str]
        List of supported volume drivers. For Mesos, it is `rexray`.
    allowed_network_drivers : Tuple[str]
        List of allowed network drivers that admins can configure in magnum.conf.
    default_network_driver : str
        Default network driver that admins can configure in magnum.conf. It is used when clients do not specify.
    """

    supported_network_drivers: List[str] = ['docker']
    supported_server_types: List[str] = ['vm', 'bm']
    supported_volume_driver: List[str] = ['rexray']
    allowed_network_drivers: Tuple[str] = (
        CONF.cluster_template.mesos_allowed_network_drivers)
    default_network_driver: str = (
        CONF.cluster_template.mesos_default_network_driver)
