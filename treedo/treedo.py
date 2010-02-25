#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Josh VanderLinden'
__version__ = '0.2'

def main():
    from gui import TreeDoFrame
    import gettext
    import os
    import wx
    gettext.install('treedo')

    # change to the project's directory, so we can use our images
    dirname = os.path.abspath(os.path.dirname(__file__))
    os.chdir(dirname)

    treedo = wx.PySimpleApp()
    frame = TreeDoFrame()
    treedo.SetTopWindow(frame)
    frame.Show(True)
    treedo.MainLoop()

if __name__ == '__main__':
    main()

