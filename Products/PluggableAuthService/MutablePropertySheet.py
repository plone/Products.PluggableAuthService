# -*- coding: utf-8 -*-
"""
Add Mutable Property Sheets and Schema Mutable Property Sheets to PAS

also a property schema type registry which is extensible.

"""
from Products.PluggableAuthService.interfaces.propertysheets import IMutablePropertySheet  # noqa
from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet
from Products.PluggableAuthService.UserPropertySheet import _SequenceTypes
from zope.interface import implementer


class PropertyValueError(ValueError):
    pass


class PropertySchemaTypeMap(object):

    def __init__(self):
        self.tmap = {}
        self.tmap_order = []

    def addType(self, type_name, identifier, order=None):
        self.tmap[type_name] = identifier
        if order is not None and isinstance(order, int):
            self.tmap_order.insert(order, type_name)
        else:
            self.tmap_order.append(type_name)

    def getTypeFor(self, value):
        ptypes = [(ptype, self.tmap[ptype]) for ptype in self.tmap_order]
        for ptype, inspector in ptypes:
            if inspector(value):
                return ptype
        raise TypeError('Invalid property type: %s' % type(value))

    def validate(self, property_type, value):
        return self.tmap[property_type](value)

PropertySchema = PropertySchemaTypeMap()
PropertySchema.addType(
    'string',
    lambda x: x is None or isinstance(x, basestring)
)
PropertySchema.addType(
    'text',
    lambda x: x is None or isinstance(x, basestring)
)
PropertySchema.addType(
    'boolean',
    lambda x: 1  # anything can be boolean
)
PropertySchema.addType(
    'int',
    lambda x: x is None or isinstance(x, int)
)
PropertySchema.addType(
    'long',
    lambda x: x is None or isinstance(x, long)
)
PropertySchema.addType(
    'float',
    lambda x: x is None or isinstance(x, float)
)
PropertySchema.addType(
    'lines',
    lambda x: x is None or isinstance(x, _SequenceTypes)
)
PropertySchema.addType(
    'selection',
    lambda x: x is None or isinstance(x, basestring)
)
PropertySchema.addType(
    'multiple selection',
    lambda x: x is None or isinstance(x, _SequenceTypes)
)
PropertySchema.addType(
    'date',
    lambda x: 1
)
validateValue = PropertySchema.validate


@implementer(IMutablePropertySheet)
class MutablePropertySheet(UserPropertySheet):

    def canWriteProperty(self, pid):
        return pid in dict(self._schema)

    def validateProperty(self, id, value):
        if id not in self._properties:
            raise PropertyValueError('No such property found on this schema')

        proptype = self.getPropertyType(id)
        if not validateValue(proptype, value):
            raise PropertyValueError(
                "Invalid value ({0}) for property '{1}' of type {2}".format(
                    value,
                    id,
                    proptype
                )
            )

    def setProperty(self, id, value):
        self.validateProperty(id, value)
        self._properties[id] = value
        self._properties = self._properties

    def setProperties(self, mapping):
        prop_keys = self._properties.keys()
        prop_update = mapping.copy()
        for key, value in tuple(prop_update.items()):
            if key not in prop_keys:
                prop_update.pop(key)
                continue
            self.validateProperty(key, value)
        self._properties.update(prop_update)
