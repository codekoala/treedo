# -*- coding: utf-8 -*-

from lxml import etree
from datetime import datetime
from uuid import uuid4
import gettext
import os

gettext.install('treedo')
USER_HOME = os.path.expanduser('~')
DEFAULT_PATH = os.path.join(USER_HOME, 'treedo.xml')
DATE_FORMAT = '%x %X'

P_URGENT = 1
P_IMPORTANT = 2
P_NORMAL = 3
P_LOW = 4
P_TRIVIAL = 5
DEFAULT_PRIORITY = P_NORMAL

PRIORITIES = {
    P_URGENT: _("1 - Urgent"),
    P_IMPORTANT: _("2 - Important"),
    P_NORMAL: _("3 - Normal"),
    P_LOW: _("4 - Low"),
    P_TRIVIAL: _("5 - Trivial"),
}

XML_TASK_TREE = 'TaskList'

class Task(object):

    STANDARD = ('summary', 'notes', 'due')

    def __init__(self, summary=None, is_complete=False, priority=3, notes="",
                 due_date=None, children=None, uuid=None, parent=None):

        if uuid is None or uuid.strip() == '':
            uuid = str(uuid4())

        self.uuid = uuid

        self.summary = summary or ''
        self.is_complete = is_complete or False
        self._priority = priority or DEFAULT_PRIORITY
        self.notes = notes or ''
        self.due_date = due_date
        self.parent = parent

        if children is None:
            children = []
        self.children = children

    @staticmethod
    def from_xml(node, parent=None):

        def get_value(name):
            element = node.find(name)
            if element is not None:
                value = element.text
            else:
                value = None
            return value

        due = get_value('DueDate')
        if due is not None:
            due = datetime.strptime(due, DATE_FORMAT)

        try:
            complete = bool(int(node.get('is_complete')))
        except TypeError:
            complete = False

        try:
            priority = int(node.get('priority'))
        except TypeError:
            priority = DEFAULT_PRIORITY

        task = Task(
                    parent=parent,
                    uuid=node.get('uuid'),
                    summary=get_value('Summary'),
                    notes=get_value('Notes'),
                    is_complete=complete,
                    priority=priority,
                    due_date=due,
                )

        children = node.find(XML_TASK_TREE)
        if children is not None:
            task.children = [Task.from_xml(child, task) for child in children.getchildren()]
        else:
            task.children = []

        return task

    def to_xml(self, parent):

        if self.due_date:
            due = self.due_date.strftime(DATE_FORMAT)
        else:
            due = ''
        complete = str(int(self.is_complete))

        xml_node = etree.SubElement(parent, Task.__name__,
                                    uuid=self.uuid,
                                    is_complete=complete,
                                    priority=str(self._priority))

        summary = etree.SubElement(xml_node, 'Summary')
        summary.text = self.summary

        notes = etree.SubElement(xml_node, 'Notes')
        notes.text = self.notes

        due_date = etree.SubElement(xml_node, 'DueDate')
        due_date.text = due

        return xml_node

    def get_priority(self):
        return PRIORITIES[self._priority]

    def set_priority(self, priority_str):
        """Sets the integer version for the priority using a string"""

        self._priority = dict((p[1], p[0]) for p in PRIORITIES.items())[priority_str]

    priority = property(get_priority, set_priority)

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
            xml_node = task.to_xml(parent)
            task_list = etree.SubElement(xml_node, XML_TASK_TREE)
        else:
            xml_node = parent
            task_list = parent

        for child in node.GetChildren():
            self.to_xml(child, task_list)

        return xml_node

    def persist(self, root):
        """Translate the HyperTreeList into our serialization format"""

        parent = etree.Element(XML_TASK_TREE)
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
                        xml_declaration=True,
                        pretty_print=True)

DATA = DataStore(DEFAULT_PATH)

