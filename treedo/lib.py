# -*- coding: utf-8 -*-

from lxml import etree
from datetime import datetime
from uuid import uuid4
import os

USER_HOME = os.path.expanduser('~')
DEFAULT_PATH = os.path.join(USER_HOME, 'treedo.xml')
DATE_FORMAT = '%x %X'

class Task(object):

    def __init__(self, summary, is_complete=False, priority=3, notes="",
                 due_date=None, children=None, uuid=None, parent=None, **kwargs):

        if uuid is None or uuid.strip() == '':
            uuid = str(uuid4())

        self.uuid = uuid

        self.summary = summary
        self.is_complete = is_complete
        self.priority = priority
        self.notes = notes
        self.due_date = due_date
        self.parent = parent

        if children is None:
            children = []
        self.children = children

        # handle custom attributes
        self.custom = kwargs

    @staticmethod
    def from_xml(node, parent=None):
        try:
            due = datetime.strptime(node.get('due_date'), DATE_FORMAT)
        except TypeError:
            due = None

        standard = ('uuid', 'summary', 'is_complete', 'priority', 'due')
        custom = dict(item for item in node.items()
                      if item[0] not in standard)
        task = Task(
                    parent=parent,
                    uuid=node.get('uuid'),
                    summary=node.get('summary'),
                    notes=node.text,
                    is_complete=bool(int(node.get('is_complete'))),
                    priority=node.get('priority'),
                    due_date=due,
                    **custom
                )

        task.children = [Task.from_xml(child, task) for child in node.getchildren()]

        return task

    def to_xml(self, parent):

        if self.due_date:
            due = self.due_date.strftime(DATE_FORMAT)
        else:
            due = ''
        complete = str(int(self.is_complete))

        xml_node = etree.SubElement(parent,
                                    Task.__name__,
                                    uuid=self.uuid,
                                    summary=self.summary,
                                    due=due,
                                    priority=self.priority,
                                    is_complete=complete,
                                    **self.custom)

        xml_node.text = self.notes

        for child in self.children:
            child.to_xml(xml_node)

        return xml_node

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
            print 'Persisting node'
            xml_node = task.to_xml(parent)
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

