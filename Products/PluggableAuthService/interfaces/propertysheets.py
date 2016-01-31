# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2001 Zope Foundation and Contributors
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
""" Interfaces:  IPropertySheet

$Id$
"""

from zope.interface import Interface


class IPropertySheet(Interface):

    """ Interface for queryable property sheets.

    o Objects implementing this interface can play in read-only fashion
      in OFS.PropertySheets' framework.
    """

    def getId():
        """ Identify the sheet within a collection.
        """

    def hasProperty(id):
        """ Does the sheet have a property corresponding to 'id'?
        """

    def getProperty(id, default=None):
        """ Return the value of the property corresponding to 'id'.

        o If no such property exists within the sheet, return 'default'.
        """

    def getPropertyType(id):
        """ Return the string identifying the type of property, 'id'.

        o If no such property exists within the sheet, return None.
        """

    def propertyInfo(id):
        """ Return a mapping describing property, 'id'.

        o Keys must include:

          'id'  -- the unique identifier of the property.

          'type' -- the string identifying the property type.

          'meta' -- a mapping containing additional info about the property.
        """

    def propertyMap():
        """ Return a tuple of 'propertyInfo' mappings, one per property.
        """

    def propertyIds():
        """ Return a sequence of the IDs of the sheet's properties.
        """

    def propertyValues():
        """ Return a sequence of the values of the sheet's properties.
        """

    def propertyItems():
        """ Return a sequence of ( id, value ) tuples, one per property.
        """


class IMutablePropertySheet(IPropertySheet):
    """ Interface for mutable property sheets.

    o Objects implementing this interface are able to read and write properties
    """
    def canWriteProperty(id):
        """ Check if a property can be modified.
        """

    def setProperty(id, value):
        """ Sets a property with a given id to the new value
        """

    def setProperties(mapping):
        """ Sets for each key in the mapping the property to the given
            corresponding value.
        """


class IMutablePropertySchemaFactory(Interface):
    """factory for mutable property sheet schemas.
    """

    def schema(user):
        """returns a schema
        """

    def defaultvalues(user):
        """returns default values for schema
        """
