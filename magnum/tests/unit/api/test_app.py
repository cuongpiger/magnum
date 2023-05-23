"""
CLASSES:
- TestAppConfig(base.BaseTestCase):
    + test_get_pecan_config(self)
"""

from pecan.configuration import Config

from magnum.api import app as api_app
from magnum.api import config as api_config
from magnum.api import hooks
from magnum.tests import base


class TestAppConfig(base.BaseTestCase):

    def test_get_pecan_config(self):
        config: Config = api_app.get_pecan_config()
        config_d: dict = dict(config.app)

        self.assertEqual(api_config.app['modules'], config_d['modules'])
        self.assertEqual(api_config.app['root'], config_d['root'])
        self.assertIsInstance(config_d['hooks'][0], hooks.ContextHook)
