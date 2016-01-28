# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer

manage_addPasswordLengthValidatorForm = PageTemplateFile( 
    "www/plvAdd", 
    globals(),
    __name__='manage_addPasswordLengthValidatorForm'
)


def addPasswordLengthValidator(dispatcher, id, title='', pwlength=5,
                               REQUEST=None, schema=None, **kw):
    """
    Create an instance of a password validation plugin.
    """
    o = PasswordLengthValidatorPlugin(id, title, pwlength)
    dispatcher._setObject(o.getId(), o)

    if REQUEST is not None:
        return REQUEST['RESPONSE'].redirect(
            "%s/manage_workspace?"
            "manage_tabs_message=Password+Length+Validator+plugin+added" 
            % dispatcher.absolute_url()
        )


@implementer(IValidationPlugin)
class PasswordLengthValidatorPlugin(BasePlugin):
    """Simple Password Validator to ensure password is 5 chars long.
    """

    meta_type = 'Password Length Validator Plugin'

    security = ClassSecurityInfo()

    _properties = (
        dict(id='prefix', type='string', mode='w', label='Optional Prefix'),
        dict(id='pwlength', type='int', mode='w', 
             label='Minimum password length'),
        )

    def __init__(self, id, title='', pwlength=5):
        """Create a password length policy
        """
        self.id = id
        self.title = title
        self.pwlength = pwlength

    @security.private
    def validateUserInfo(self, user, set_id, set_info):
        """ See IValidationPlugin. Used to validate password property
        """
        if not set_info:
            return []

        password = set_info.get('password', None)
        if password is None:
            return []

        if len(password) < self.pwlength:
            msg = 'Your password must contain at least %i characters.' % (
                   self.pwlength)
            return [
                {
                    'id': 'password',
                    'error': msg
                }
            ]
        else:
            return []

InitializeClass(PasswordLengthValidatorPlugin)
