import wx
from wx.lib.agw import hypertreelist as HTL

class TaskList(HTL.HyperTreeList):
    def __init__(self, parent):
        style = wx.SUNKEN_BORDER | wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HIDE_ROOT | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_ROW_LINES #| wx.TR_COLUMN_LINES | HTL.TR_AUTO_CHECK_PARENT
        HTL.HyperTreeList.__init__(self, parent, -1, style=style)

        self.AddColumn('%')
        self.AddColumn('Task')
        self.AddColumn('Due')
        self.SetMainColumn(1)
        self.SetColumnWidth(0, 30)
        self.SetColumnWidth(1, 200)
        self.SetColumnWidth(2, 90)

        self.root = self.AddRoot('Tasks')

        child1 = self.AppendItem(self.root, 'Testing', ct_type=1)
        child2 = self.AppendItem(self.root, 'Testing', ct_type=1)
        child3 = self.AppendItem(child2, 'Testing', ct_type=1)

        self.SetItemText(child1, '0%', 0)
        self.SetItemText(child1, 'frrt', 2)

class Sample(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.SetMinSize((640, 480))
        self.SetTitle('HyperTreeList Demo')
        self.CenterOnParent()

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.tree = TaskList(self)
        sizer.Add(self.tree, 1, wx.EXPAND)
        self.Show(True)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frm = Sample(None)
    app.MainLoop()
