from distutils.core import setup
from treedo import __version__, __author__
import os
import sys

APP_TITLE = 'TreeDo'
extra = {}

if 'py2app' in sys.argv and sys.platform == 'darwin':
    from upx import Py2App

    options = dict(
        iconfile='treedo/res/treedo.icns',
        compressed=1,
        optimize=1,
        plist=dict(
            CFBundleName=APP_TITLE,
            CFBundleShortVersionString=__version__,
            CFBundleGetInfoString='%s %s' % (APP_TITLE, __version__),
            CFBundleExecutable=APP_TITLE,
            CFBundleIdentifier='com.codekoala.treedo',
        ),
        packages=[
            'lxml',
        ],
        frameworks=[
            '/usr/lib/libxml2.2.7.3.dylib',
        ],
        includes=[
            'gzip',
        ],
    )
    extra = dict(
        app=['treedo/treedo.py'],
        options=dict(py2app=options),
        setup_requires=[
            'py2app',
            'lxml',
        ],
        cmdclass={
            'py2app': Py2App,
        }
    )

setup(
    name='treedo',
    version=__version__,
    description='A Python and XML-based todo list.',
    long_description=open('README', 'r').read(),
    keywords='todo, python, xml, lxml',
    author=__author__,
    author_email='codekoala at gmail com',
    license='BSD',
    package_dir={'treedo': 'treedo'},
    packages=['treedo'],
    platforms=['Windows', 'Linux', 'OSX'],
    scripts=[
        'treedo/scripts/treedo',
    ],
    data_files=[
        ('.', (
            'README',
            'LICENSE',
        )),
        ('res', (
            'treedo/res/add_subtask.png',
            'treedo/res/add.png',
            'treedo/res/collapse.png',
            'treedo/res/expand.png',
            'treedo/res/save.jpg',
        )),
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Topic :: Utilities",
    ],
    **extra
)

