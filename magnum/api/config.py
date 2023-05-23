"""
VARIABLES:
- app - Pecan application configurations
"""

from magnum.api import hooks

# Pecan Application Configurations
app: dict = {
    'root': 'magnum.api.controllers.root.RootController',
    'modules': ['magnum.api'],
    'debug': False,
    'hooks': [
        hooks.ContextHook(),
        hooks.RPCHook(),
        hooks.NoExceptionTracebackHook(),
    ],
    'acl_public_routes': [
        '/',
        '/v1',
    ],
}
