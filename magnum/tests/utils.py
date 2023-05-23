"""
FUNCTIONS:
- dummy_context(user='test_username', project_id='test_tenant_id')
"""

from magnum.common import context as magnum_context


def dummy_context(user='test_username', project_id='test_tenant_id'):
    return magnum_context.RequestContext(user=user, project_id=project_id)
