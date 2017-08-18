# -*- coding: utf-8 -*-
"""
Small example of a traitsui app displaying an app with a dynamic
enum, where the maximum integer value is controlled by another
field.

"""
from __future__ import division, print_function

from traits.api import HasStrictTraits, Enum, Int, Property, List
from traitsui.api import Item, View, VGroup


class Demo(HasStrictTraits):

    a = Enum(values="a_list")

    a_list = Property(List, depends_on="max_a")

    max_a = Int(3)

    view = View(
        VGroup(
            Item('a'),
            Item('max_a')
        )
    )

    def _get_a_list(self):
        return range(self.max_a)


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
