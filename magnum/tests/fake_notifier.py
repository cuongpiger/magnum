"""
FUNCTIONS:
- reset(self)

CLASSES:
- FakeNotifier(object):
    + __init__(self, transport, publisher_id=None, driver=None, topic=None, serializer=None, retry=None)
    + prepare(self, publisher_id=None)
    + _notify(self, ctxt, event_type, payload, priority)
"""

import collections
import functools

NOTIFICATIONS = []
FakeMessage = collections.namedtuple('Message', [
    'publisher_id', 'priority', 'event_type', 'payload', 'context'])


def reset():
    """
    [cuongdm]
    Reset the list of notifications `NOTIFICATIONS`.
    """
    del NOTIFICATIONS[:]


class FakeNotifier(object):

    def __init__(self, transport, publisher_id=None, driver=None, topic=None, serializer=None, retry=None):
        self.transport = transport
        self.publisher_id = publisher_id or 'fake.id'
        for priority in ('debug', 'info', 'warn', 'error', 'critical'):
            setattr(self, priority, functools.partial(self._notify, priority=priority.upper()))

    def prepare(self, publisher_id=None):
        if publisher_id is None:
            publisher_id = self.publisher_id
        return self.__class__(self.transport, publisher_id=publisher_id)

    def _notify(self, ctxt, event_type, payload, priority):
        msg = FakeMessage(self.publisher_id, priority, event_type, payload, ctxt)
        NOTIFICATIONS.append(msg)
