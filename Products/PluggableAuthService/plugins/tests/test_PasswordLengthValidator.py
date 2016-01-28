##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this
# distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import unittest
from Products.PluggableAuthService.tests import conformance


class PasswordLengthValidatorTests(
    unittest.TestCase,
    conformance.IValidationPlugin_conformance,
):

    def _getTargetClass(self):

        from Products.PluggableAuthService.plugins.PasswordLengthValidator \
            import PasswordLengthValidatorPlugin

        return PasswordLengthValidatorPlugin

    def _makeOne(self, id='test', *args, **kw):

        return self._getTargetClass()(id=id, *args, **kw)

    def test_defaults(self):
        """ Test default values
        """
        validator = self._makeOne()
        self.assertEquals(validator.getId(), 'test')
        self.assertEquals(validator.title, '')
        self.assertEquals(validator.pwlength, 5)

        minimum_length = {'password': '12345'}
        self.failIf(validator.validateUserInfo(None, None, minimum_length))

        too_short = {'password': '123'}
        error_info = validator.validateUserInfo(None, None, too_short)[0]
        self.assertEquals(error_info.get('id', None), 'password')

    def test_increased_pw_length(self):
        """ Test instantiation with values provided
        """
        validator = self._makeOne(id='vld', title='Validator', pwlength=10)
        self.assertEquals(validator.getId(), 'vld')
        self.assertEquals(validator.title, 'Validator')
        self.assertEquals(validator.pwlength, 10)

        minimum_length = {'password': '1234567890'}
        self.failIf(validator.validateUserInfo(None, None, minimum_length))

        too_short = {'password': '12345'}
        error_info = validator.validateUserInfo(None, None, too_short)[0]
        self.assertEquals(error_info.get('id', None), 'password')

if __name__ == "__main__":
    unittest.main()


def test_suite():
    tests = (
        unittest.makeSuite(PasswordLengthValidatorTests),
    )

    return unittest.TestSuite(tests)
