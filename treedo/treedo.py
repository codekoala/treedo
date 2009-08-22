#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from lxml import etree

__author__ = 'Josh VanderLinden'
__appname__ = 'TreeDo'
__version__ = '0.1'

class TreeDoFrame(wx.Frame):
    """
    This is the main TreeDo window, where your tasks are laid out before you.
    """
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title='TreeDo', size=(300, 500))
        self.Show(True)

if __name__ == '__main__':
    root = etree.Element('TreeDo', version=__version__)
    child = etree.SubElement(root, 'Task', start='22-08-09')
    child1 = etree.SubElement(child, 'Task', start='22-08-09')
    child.text = 'wasabi'
    print etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)

    """
    app = wx.App()
    frame = TreeDoFrame()
    app.MainLoop()
    """
