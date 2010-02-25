#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Josh VanderLinden'
__appname__ = 'TreeDo'
__version__ = '0.2'

def main():
    from gui import TreeDoFrame
    import gettext
    import wx
    gettext.install('treedo')

    treedo = wx.PySimpleApp()
    frame = TreeDoFrame()
    treedo.SetTopWindow(frame)
    frame.Show(True)
    treedo.MainLoop()

if __name__ == '__main__':
    main()

