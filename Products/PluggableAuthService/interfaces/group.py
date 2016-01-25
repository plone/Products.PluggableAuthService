# -*- coding: utf-8 -*-
from zope.interface import Interface


class IGroupData(Interface):
    """ An abstract interface for accessing properties on a group object"""

    def setProperties(properties=None, **kw):
        """Allows setting of group properties en masse.
        Properties can be given either as a dict or a keyword parameters
        list"""

    def getProperty(id):
        """ Return the value of the property specified by 'id' """

    def getProperties():
        """ Return the properties of this group. Properties are as usual in
        Zope."""

    def getGroupId():
        """ Return the string id of this group, WITHOUT group prefix."""

    def getMemberId():
        """This exists only for a basic user/group API compatibility
        """

    def getGroupName():
        """ Return the name of the group."""

    def getGroupMembers():
        """ Return a list of the portal_memberdata-ish members of the group."""

    def getAllGroupMembers():
        """ Return a list of the portal_memberdata-ish members of the group
        including transitive ones (ie. users or groups of a group in that
        group)."""

    def getGroupMemberIds():
        """ Return a list of the user ids of the group."""

    def getAllGroupMemberIds():
        """ Return a list of the user ids of the group.
        including transitive ones (ie. users or groups of a group in that
        group)."""

    def addMember(id):
        """ Add the existing member with the given id to the group"""

    def removeMember(id):
        """ Remove the member with the provided id from the group """

    def getGroup():
        """ Returns the actual group implementation. Varies by group
        implementation (GRUF/Nux/et al)."""
