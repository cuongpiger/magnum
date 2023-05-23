"""
CLASSES:
- ConfFixture(ConfFixture(fixtures.Fixture):
    + _setUp(self)
"""

import fixtures
import magnum.conf
from magnum.common import config

CONF = magnum.conf.CONF


class ConfFixture(fixtures.Fixture):
    """Fixture to manage global conf settings."""

    def _setUp(self):
        CONF.set_default('host', 'fake-mini')
        CONF.set_default('connection', "sqlite://", group='database')
        CONF.set_default('sqlite_synchronous', False, group='database')
        config.parse_args([], default_config_files=[])
        self.addCleanup(CONF.reset)
