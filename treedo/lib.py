# -*- coding: utf-8 -*-

from lxml import etree

class Task(object):
    __slots__ = ('parent', 'subject', 'is_complete', 'status', 'priority', 'start_date', 'due_date', 'notes')

    def __init__(self, *args, **kargs):
        for i, val in enumerate(args):
            setattr(self, self.__slots__[i], val)
        for key, val in kwargs:
            setattr(self, key, val)

class DataStore(object):
    data = None
    filename = None

    def add_task(self, parent):
        pass

    def get_list(self, filename):
        if not self.data:
            self.data = etree.parse(filename)
            self.filename = filename
        return self.data

    def persist_list(self, filename=None):
        if not filename:
            filename = self.filename
        print etree.tostring(
                self.data,
                pretty_print=True,
                encoding='utf-8',
                xml_declaration=True)
