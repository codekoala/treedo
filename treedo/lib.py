# -*- coding: utf-8 -*-

from lxml import etree
from datetime import datetime
import os

USER_HOME = os.path.expanduser('~')
DEFAULT_PATH = os.path.join(USER_HOME, 'treedo.xml')
DATE_FORMAT = '%x %X'

class Task(object):
    __slots__ = ('parent', 'summary', 'notes', 'is_complete', 'priority',
                 'due_date', 'children', 'item', 'node')

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

    @staticmethod
    def from_xml(task, parent=None):
        try:
            due = datetime.strptime(task.get('due_date'), DATE_FORMAT)
        except TypeError:
            due = None

        item = Task(
                    parent=parent,
                    summary=task.get('summary'),
                    notes=task.text,
                    is_complete=bool(int(task.get('is_complete'))),
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
        self.init_data()

    def init_data(self):

        try:
            self.data = etree.parse(self.filename)
        except IOError:
            self.data = etree.ElementTree()

    def to_xml(self, node, parent):

        task = node.GetData()

        if task:
            due_date = task.due_date and task.due_date.strftime(DATE_FORMAT) or ''
            complete = str(int(task.is_complete))
            print 'Persisting task: %s (%s)' % (task.summary, complete)

            xml_node = etree.SubElement(parent,
                                'Task',
                                summary=task.summary,
                                due=due_date,
                                priority=task.priority,
                                is_complete=complete)

            xml_node.text = task.notes
        else:
            print 'Persisting tree'
            xml_node = parent

        for child in node.GetChildren():
            self.to_xml(child, xml_node)

        return xml_node

    def persist(self, root):
        """Translate the HyperTreeList into our serialization format"""

        parent = etree.Element('TaskList')
        self.data._setroot(parent)
        serialized = self.to_xml(root, parent)
        self.persist_list()

    def get_list(self):
        self.init_data()
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

