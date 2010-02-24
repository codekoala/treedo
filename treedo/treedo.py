#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.calendar
from wx.lib.masked import TimeCtrl
from wx.lib.agw import hypertreelist as HTL
from datetime import datetime, time
from lib import Task, DATA

__author__ = 'Josh VanderLinden'
__appname__ = 'TreeDo'
__version__ = '0.1'

ID_ADD_TASK = 1000
ID_ADD_SUBTASK = 1010
ID_COLLAPSE = 1020
ID_EXPAND = 1030

class TaskList(HTL.HyperTreeList):
    """
    This is the widget that houses the tasks
    """
    def __init__(self, parent):
        style = wx.SUNKEN_BORDER | wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HIDE_ROOT | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_ROW_LINES | wx.TR_EDIT_LABELS #| wx.TR_COLUMN_LINES | HTL.TR_AUTO_CHECK_PARENT
        HTL.HyperTreeList.__init__(self, parent, -1, style=style)

        self.AddColumn('%')
        self.AddColumn('Task')
        self.AddColumn('Due')
        self.SetMainColumn(1)

        self.root = self.AddRoot('Tasks')
        self.GetMainWindow().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit)
        self.Bind(HTL.EVT_TREE_ITEM_CHECKED, self.OnItemToggled)

    def EvaluateCompleteness(self, item=None):
        """Determines how complete various task trees are"""

        pass

    def OnEndEdit(self, evt):
        print 'Save task?', evt.GetLabel(), evt.GetItem()
        task = evt.GetItem().GetData()
        if task:
            task.summary = evt.GetLabel()

    def OnLeftDClick(self, evt):
        pt = evt.GetPosition()
        item, flags, column = self.HitTest(pt)
        if item and (flags & wx.TREE_HITTEST_ONITEMLABEL):
            self.EditLabel(item)

        evt.Skip()

    def OnItemToggled(self, evt):
        item = evt.GetItem()
        task = item.GetData()
        if task:
            task.is_complete = item.IsChecked()

        self.EvaluateCompleteness()

    def SetTasks(self, tasks):
        for task in tasks:
            self.AddTask(task)
        self.ExpandAll()

    def AddTask(self, task, parent=None):
        if parent == None:
            parent = self.root

        task.parent = parent
        item = self.AppendItem(parent, task.summary, ct_type=1)

        self.SetItemText(item, '0%', 0)
        item.Check(task.is_complete)
        if task.due_date:
            self.SetItemText(item, task.due_date.strftime('%Y-%m-%d %H:%M'), 2)

        for child in task.children:
            self.AddTask(child, item)

        item.SetData(task)

class TaskInfoDialog(wx.Dialog):

    def __init__(self, *args, **kwds):
        kwds['style'] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self, -1)
        self.txtSummary = wx.TextCtrl(self.panel, -1, "")
        self.lblNotes = wx.StaticText(self.panel, -1, _('Notes:'), style=wx.ALIGN_RIGHT)
        self.txtNotes = wx.TextCtrl(self.panel, -1, "", style=wx.TE_MULTILINE|wx.TE_RICH|wx.TE_WORDWRAP)
        self.lblPriority = wx.StaticText(self.panel, -1, _('Priority:'), style=wx.ALIGN_RIGHT)
        self.cmbPriority = wx.ComboBox(self.panel, -1, choices=[_("1 - Urgent"), _("2 - Important"), _("3 - Normal"), _("4 - Low"), _("5 - Trivial")], style=wx.CB_DROPDOWN)
        self.chkIsComplete = wx.CheckBox(self.panel, -1, _('Is Complete'))
        self.lblDateDue = wx.StaticText(self.panel, -1, _('Due:'), style=wx.ALIGN_RIGHT)
        self.chkIsDue = wx.CheckBox(self.panel, -1, _('Has due date'))
        self.calDueDate = wx.calendar.CalendarCtrl(self.panel, -1)
        self.txtTime = TimeCtrl(self.panel, id=-1,
                                 value=datetime.now().strftime('%X'),
                                 style=wx.TE_PROCESS_TAB,
                                 validator=wx.DefaultValidator,
                                 format='24HHMMSS',
                                 fmt24hr=True,
                                 displaySeconds=True,
                                )

        self.__set_properties()
        self.__do_layout()

        self.chkIsDue.Bind(wx.EVT_CHECKBOX, self.ToggleDueDate)
        self.txtSummary.SetFocus()

    def __set_properties(self):
        self.SetTitle(_('Task Information'))
        self.cmbPriority.SetSelection(2)
        self.calDueDate.Enable(False)
        self.txtTime.Enable(False)

    def __do_layout(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.FlexGridSizer(5, 2, 5, 5)
        lblSubject = wx.StaticText(self.panel, -1, _('Summary:'))
        sizer.Add(lblSubject, 0, wx.EXPAND, 0)
        sizer.Add(self.txtSummary, 0, wx.ALL|wx.EXPAND, 0)
        sizer.Add(self.lblNotes, 0, wx.EXPAND, 0)
        sizer.Add(self.txtNotes, 0, wx.EXPAND, 0)
        sizer.Add(self.lblPriority, 0, wx.EXPAND, 0)
        sizer.Add(self.cmbPriority, 0, wx.EXPAND, 0)
        sizer.Add((20, 20), 0, 0, 0)
        sizer.Add(self.chkIsComplete, 0, 0, 0)
        sizer.Add(self.lblDateDue, 0, wx.ALIGN_RIGHT, 0)
        sizer.Add(self.chkIsDue, 0, 0, 0)
        sizer.Add((20, 20), 0, 0, 0)
        sizer.Add(self.calDueDate, 0, 0, 0)
        sizer.Add((20, 20), 0, 0, 0)
        sizer.Add(self.txtTime, 0, 0, 0)
        self.panel.SetSizer(sizer)
        sizer.AddGrowableRow(1)
        sizer.AddGrowableCol(1)
        mainSizer.Add(self.panel, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.AddF(self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL),
                       wx.SizerFlags(0).Expand().Border(wx.BOTTOM|wx.RIGHT, 5))
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
        self.Centre()

        size = (270, 420)
        self.SetMinSize(size)
        self.SetSize(size)

    def ToggleDueDate(self, evt):
        en = self.chkIsDue.IsChecked()
        self.calDueDate.Enable(en)
        self.txtTime.Enable(en)

    def GetTask(self):
        if self.chkIsDue.IsChecked():
            due = self.calDueDate.PyGetDate()
            tm = self.txtTime.GetValue()

            try:
                tm = datetime.strptime(tm, '%H:%M:%S').time()
            except:
                tm = datetime.strptime(tm, '%H:%M').time()

            due = datetime.combine(due, tm)
        else:
            due = None

        task = Task(
                   summary=self.txtSummary.GetValue(),
                   is_complete=self.chkIsComplete.IsChecked(),
                   priority=self.cmbPriority.GetValue(),
                   due_date=due,
                   notes=self.txtNotes.GetValue()
               )

        return task

    def SetTask(self, task):
        self.txtSummary.SetValue(task.summary)
        self.txtNotes.SetValue(task.notes)
        self.cmbPriority.SetStringSelection(task.priority)
        self.chkIsComplete.SetChecked(task.is_complete)
        self.calDueDate.PySetDate(task.due_date)
        self.txtTime.SetValue(task.due_date.strftime('%X'))

class TreeDoFrame(wx.Frame):
    """
    This is the main TreeDo window, where your tasks are laid out before you.
    """

    def __init__(self):
        wx.Frame.__init__(self, None, -1, title=_('TreeDo'), size=(300, 500))
        self.SetMinSize((300, 300))
        self.CenterOnParent()

        self.toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        self.toolbar.SetToolBitmapSize((24, 24))

        save_img =  wx.Bitmap('res/save.jpg', wx.BITMAP_TYPE_JPEG)
        add_img =  wx.Bitmap('res/add.png', wx.BITMAP_TYPE_PNG)
        add_sub_img =  wx.Bitmap('res/add_subtask.png', wx.BITMAP_TYPE_PNG)
        collapse_img =  wx.Bitmap('res/collapse.png', wx.BITMAP_TYPE_PNG)
        expand_img =  wx.Bitmap('res/expand.png', wx.BITMAP_TYPE_PNG)
        self.toolbar.AddSimpleTool(wx.ID_SAVE, save_img, _('Save Task List'), _('Save the task list to the hard drive'))
        self.toolbar.AddSimpleTool(ID_ADD_TASK, add_img, _('Add Task'), _('Create a new task'))
        self.toolbar.AddSimpleTool(ID_ADD_SUBTASK, add_sub_img, _('Add Sub-Task'), _('Create a new subtask'))
        self.toolbar.AddSimpleTool(ID_COLLAPSE, collapse_img, _('Collapse'), _('Collapse all tasks'))
        self.toolbar.AddSimpleTool(ID_EXPAND, expand_img, _('Expand'), _('Expand all tasks'))
        self.Bind(wx.EVT_TOOL, self.OnToolClick)
        self.toolbar.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.tree = TaskList(self)
        sizer.Add(self.tree, 1, wx.EXPAND)

        self.Bind(wx.EVT_SIZE, self.UpdateColumnWidths)

        self.tree.SetTasks(DATA.get_list())

    def UpdateColumnWidths(self, evt=None):
        width, height = self.GetSize()

        self.tree.SetColumnWidth(0, 40)
        self.tree.SetColumnWidth(1, width - 150)
        self.tree.SetColumnWidth(2, 100)

        evt.Skip()

    def OnToolClick(self, evt):
        if evt.GetId() in (ID_ADD_TASK, ID_ADD_SUBTASK):
            taskDlg = TaskInfoDialog(self, -1, _('Task Info'))
            if taskDlg.ShowModal() == wx.ID_OK:
                task = taskDlg.GetTask()
                parent = None
                if evt.GetId() == ID_ADD_SUBTASK:
                    parent = self.tree.GetSelection()
                self.tree.AddTask(task, parent)
        elif evt.GetId() == ID_COLLAPSE:
            self.tree.Collapse()
        elif evt.GetId() == ID_EXPAND:
            self.tree.ExpandAll()
        elif evt.GetId() == wx.ID_SAVE:
            self.Persist()

    def Persist(self):
        """Persists the task list to the filesystem"""

        DATA.persist(self.tree.root)

if __name__ == '__main__':
    import gettext
    gettext.install('treedo')

    treedo = wx.PySimpleApp()
    frame = TreeDoFrame()
    treedo.SetTopWindow(frame)
    frame.Show(True)
    treedo.MainLoop()
