from distutils.core import setup
from treedo import __version__, __author__
import os

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
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
)

