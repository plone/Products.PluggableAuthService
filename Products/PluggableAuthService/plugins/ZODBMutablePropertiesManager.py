# -*- coding: utf-8 -*-
"""
Mutable Property Manager
"""
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from BTrees.OOBTree import OOBTree
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IMutablePropertiesPlugin  # noqa
from Products.PluggableAuthService.interfaces.propertysheets import IMutablePropertySchemaFactory  # noqa
from Products.PluggableAuthService.MutablePropertySheet import MutablePropertySheet  # noqa
from Products.PluggableAuthService.MutablePropertySheet import validateValue
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.UserPropertySheet import _guessSchema
from zope.interface import implementer
import copy

manage_addZODBMutablePropertiesManagerForm = PageTemplateFile(
    "www/MutablePropertyProviderForm",
    globals()
)


def manage_addZODBMutablePropertiesManager(
    self,
    id,
    title='',
    RESPONSE=None,
    schema=None,
    **kw
):
    """
    Create an instance of a mutable property manager.
    """
    ob = ZODBMutablePropertiesManager(id, title, schema, **kw)
    self._setObject(ob.getId(), ob)

    if RESPONSE is not None:
        RESPONSE.redirect('manage_workspace')


@implementer(IMutablePropertiesPlugin)
class ZODBMutablePropertiesManager(BasePlugin):
    """Storage for mutable properties in the ZODB for users/groups.

    API sounds like it's only for users, but groups work as well.
    """

    meta_type = 'ZODB Mutable Properties Manager'

    security = ClassSecurityInfo()

    def __init__(self, id, title='', schema=None, **kw):
        """Create in-ZODB mutable property provider.

        Provide a schema either as a list of (name,type,value) tuples
        in the 'schema' parameter or as a series of keyword parameters
        'name=value'. Types will be guessed in this case.

        The 'value' is meant as the default value, and will be used
        unless the user provides data.

        If no schema is provided by constructor, the properties of the
        portal_memberdata object will be used.

        Types available: string, text, boolean, int, long, float, lines, date
        """
        self.id = id
        self.title = title
        self._storage = OOBTree()

        # calculate schema and default values
        defaultvalues = {}
        if not schema and not kw:
            schema = ()
        elif not schema and kw:
            schema = _guessSchema(kw)
            defaultvalues = kw
        else:
            valuetuples = [(name, value) for name, type, value in schema]
            schema = [(name, type) for name, type, value in schema]
            for name, value in valuetuples:
                defaultvalues[name] = value
        self._schema = tuple(schema)
        self._defaultvalues = defaultvalues

    def _getSchema(self, isgroup=None):
        schema = self._schema
        if schema:
            return schema
        factory = IMutablePropertySchemaFactory(self, None)
        if factory is None:
            # if no schema is provided, use portal_memberdata properties
            return ()
        return factory.schema(self)

    def _getDefaultValues(self, isgroup=None):
        """Returns a dictionary mapping of property names to default values.
        Defaults to portal_*data tool if necessary.
        """
        defaultvalues = self._defaultvalues or {}
        if not self._schema:
            factory = IMutablePropertySchemaFactory(self, None)
            if factory is not None:
                return factory.defaultvalues(self)
        return defaultvalues

    @security.private
    def getPropertiesForUser(self, user, request=None):
        """Get property values for a user or group.
        Returns a dictionary of values or a PropertySheet.

        This implementation will always return a MutablePropertySheet.
        """
        data = copy.deepcopy(self._getDefaultValues())
        data.update(self._storage.get(user.getId(), {}))
        schema = self._getSchema()
        return MutablePropertySheet(
            self.id,
            schema=schema,
            **data
        )

    @security.private
    def setPropertiesForUser(self, user, propertysheet):
        """Set the properties of a user or group based on the contents of a
        property sheet.
        """
        properties = dict(propertysheet.propertyItems())
        for name, property_type in self._getSchema() or ():
            if (
                name in properties and not
                validateValue(property_type, properties[name])
            ):
                raise ValueError(
                    'Invalid value: {0} does not conform to {1}'.format(
                        (name, property_type)
                    )
                )

        allowed_prop_keys = [pn for pn, pt in self._getSchema() or ()]
        if allowed_prop_keys:
            prop_names = set(properties.keys()) - set(allowed_prop_keys)
            if prop_names:
                raise ValueError('Unknown Properties: %r' % prop_names)

        userid = user.getId()
        userprops = self._storage.get(userid)
        properties.update({
            'isGroup': getattr(user, 'isGroup', lambda: None)()
        })
        if userprops is not None:
            userprops.update(properties)
            # notify persistence machinery of change
            self._storage[userid] = self._storage[userid]
        else:
            self._storage.insert(user.getId(), properties)

    @security.private
    def deleteUser(self, user_id):
        """Delete all user properties
        """
        # Do nothing if an unknown user_id is given
        try:
            del self._storage[user_id]
        except KeyError:
            pass


InitializeClass(ZODBMutablePropertiesManager)
