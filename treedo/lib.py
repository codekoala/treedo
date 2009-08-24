# -*- coding: utf-8 -*-

from lxml import etree
from datetime import datetime
import os

USER_HOME = os.path.expanduser('~')
DEFAULT_PATH = os.path.join(USER_HOME, 'treedo.xml')
DATE_FORMAT = '%x %X'

class Task(object):
    __slots__ = ('parent', 'summary', 'notes', 'is_complete', 'priority', 'due_date', 'children')

    def __init__(self, *args, **kwargs):
        # initialize all attributes
        for slt in self.__slots__:
            setattr(self, slt, None)

        # set attributes based on argument positions
        for i, val in enumerate(args):
            setattr(self, self.__slots__[i], val)

        # set attributes based on keyword
        for key, val in kwargs.items():
            setattr(self, key, val)

        if not isinstance(self.children, list):
            self.children = []

    @classmethod
    def from_xml(Task, task, parent=None):
        try:
            due = datetime.strptime(task.get('due_date'), DATE_FORMAT)
        except TypeError:
            due = None

        item = Task(
                    parent=parent,
                    summary=task.get('summary'),
                    notes=task.text,
                    is_complete=bool(task.get('is_complete')),
                    priority=task.get('priority'),
                    due_date=due,
                )

        item.children = [Task.from_xml(child, item) for child in task.getchildren()]

        return item

class DataStore(object):
    data = None
    filename = None

    def __init__(self, path=DEFAULT_PATH):
        self.filename = path
        self.get_list()

    def add_task(self, task, parent=None):
        if parent == None:
            parent = self.data.getroot()

        if parent == None:
            parent = etree.Element('TaskList')
            self.data._setroot(parent)

        due_date = task.due_date and task.due_date.strftime(DATE_FORMAT) or ''

        item = etree.SubElement(parent,
                            'Task',
                            summary=task.summary,
                            due=due_date,
                            priority=task.priority,
                            is_complete=str(task.is_complete))
        item.text = task.notes
        self.persist_list()

    def get_list(self):
        if not self.data:
            try:
                self.data = etree.parse(self.filename)
            except IOError:
                self.data = etree.ElementTree()

        tasks = []
        if self.data.getroot() is not None:
            for task in self.data.getroot():
                item = Task.from_xml(task)
                tasks.append(item)

        return tasks

    def persist_list(self, filename=None):
        if not filename:
            filename = self.filename
        self.data.write(self.filename,
                        encoding='utf-8',
                        xml_declaration=True)

DATA = DataStore(DEFAULT_PATH)
