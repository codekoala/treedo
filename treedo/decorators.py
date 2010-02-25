import wx

def requires_selection(func):
    """Displays an error message if the user has not selected a task.

    This decorator is only intended to work on TreeDoFrame methods."""

    def wrapped(self, *args, **kwargs):
        if self.tree.GetSelection() != self.tree.root:
            return func(self, *args, **kwargs)
        else:
            wx.MessageBox('Please select a task and try again.', 'Error')
    return wrapped

