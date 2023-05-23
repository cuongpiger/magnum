"""
CLASSES:
- PolicyFixture(fixtures.Fixture):
    + _setUp(self)
    + set_rules(self, rules)
"""

import fixtures
import magnum.conf

from oslo_policy import _parser
from magnum.common import policy as magnum_policy

CONF = magnum.conf.CONF


class PolicyFixture(fixtures.Fixture):

    def _setUp(self):
        CONF(args=[], project='magnum')
        magnum_policy._ENFORCER = None
        self.addCleanup(magnum_policy.init().clear)

    def set_rules(self, rules):
        policy = magnum_policy._ENFORCER
        policy.set_rules({k: _parser.parse_rule(v) for k, v in rules.items()})
