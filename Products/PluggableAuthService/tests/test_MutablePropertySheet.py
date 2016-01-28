# -*- coding: utf-8 -*-
from .conformance import IMutablePropertySheet_conformance
import os.path
import unittest

path = os.path.dirname(__file__)
path = os.path.join(path, 'image.gif')
img_file = open(path, 'r')


class MutablePropertySheetTest(
    unittest.TestCase,
    IMutablePropertySheet_conformance
):

    def _getTargetClass(self):

        from Products.PluggableAuthService.MutablePropertySheet \
            import MutablePropertySheet

        return MutablePropertySheet

    def test_mutablity(self):
        """Create a sheet
        """
        from Products.PluggableAuthService.MutablePropertySheet import MutablePropertySheet  # noqa
        sheet = MutablePropertySheet('testsheet', foo=1, bar="2")
        self.assertEqual(sheet.getProperty('foo'), 1)
        self.assertEqual(sheet.getProperty('bar'), "2")

        sheet.setProperty('foo', 4)
        self.assertEqual(sheet.getProperty('foo'), 4)

        sheet.setProperty('bar', "abc")
        self.assertEqual(sheet.getProperty('bar'), "abc")

        sheet.setProperties({'foo': 10, 'bar': 'xyz'})
        self.assertEqual(sheet.getProperty('foo'), 10)
        self.assertEqual(sheet.getProperty('bar'), "xyz")
