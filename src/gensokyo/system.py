#!/usr/bin/env python3

import abc

from gensokyo import locator


class System:

    """
    Superclass for Systems

    """

    __metaclass__ = abc.ABCMeta

    @staticmethod
    def get_with(types):
        """
        :param types: component types to look for
        :type types: tuple
        :rtype: set

        """
        return locator.model.em.get_with(types)

    @staticmethod
    def get_tag(tag):
        """
        :param tag: tag to look for
        :type tag: str
        :rtype: Entity

        """
        return locator.model.tm[tag]

    @staticmethod
    def dispatch_event(event, *args):
        """
        :param event: event
        :type event: str

        """
        locator.sm.dispatch_event(event, *args)
