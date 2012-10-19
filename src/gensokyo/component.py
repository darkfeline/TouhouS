#!/usr/bin/env python3

"""
This module contains the components provided by gensokyo.

In a component/system design, components hold only data.  Systems operate on
entites which own components, and thus all logic are in systems.

"""

import abc


class Component:

    """
    Abstract Base Class for components

    Please subclass to avoid confusion

    """

    __metaclass__ = abc.ABCMeta
