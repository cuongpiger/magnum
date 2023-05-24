"""
CLASSES:
- VersionedMethod
    + __init__(self, name, start_version, end_version, func)
    + __str__(self)
"""

from typing import Callable


class VersionedMethod(object):
    """
    Versioning information for a single method

    ...
    Attributes
    ----------
    name : str
        Name of the method
    start_version : str
        Minimum acceptable version
    end_version : str
        Maximum acceptable version
    func : Callable
        Method to call
    """

    def __init__(self, name: str, start_version: str, end_version: str, func: Callable):
        """Constructor

        :param name: Name of the method
        :param start_version: Minimum acceptable version
        :param end_version: Maximum acceptable version
        :param func: Method to call
        """
        self.name: str = name
        self.start_version: str = start_version
        self.end_version: str = end_version
        self.func: Callable = func

    def __str__(self) -> str:
        return "Version Method %s: min: %s, max: %s" % (self.name, self.start_version, self.end_version)
