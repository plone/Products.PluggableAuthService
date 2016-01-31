# -*- coding: utf-8 -*-
from Products.PluggableAuthService.tests import conformance
import unittest


class ZODBRoleManagerTests(
    unittest.TestCase,
    conformance.IMutablePropertiesPlugin_conformance,
):

    def _getTargetClass(self):
        from Products.PluggableAuthService.plugins.ZODBMutablePropertiesManager import ZODBMutablePropertiesManager  # noqa
        return ZODBMutablePropertiesManager

    def _makeOne(self, id='test', *args, **kw):
        return self._getTargetClass()(id=id, *args, **kw)

    def test_empty_schema(self):
        zmpm = self._makeOne()

        self.assertEqual(zmpm._getSchema(), tuple())
