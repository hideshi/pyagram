from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'pyagram',
    version = '1.0.5',
    description = 'Pyagram: Python Finite State Machine Diagram Generator',
    license = 'MIT License',
    author = 'Hideshi Ogoshi',
    author_email = 'hideshi.ogoshi@gmail.com',
    url = 'https://github.com/hideshi',
    bugtrack_url = 'https://github.com/hideshi/pyagram/issues',
    long_description = read('README.md'),
    packages = ['pyagram'],
    install_requires = [
        'pyparsing',
    ],
    entry_points = {
        'console_scripts': ['pyagram = pyagram.pyagram:main']
    },
    platforms = ['MacOS', 'Linux'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Topic :: Documentation',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Documentation',
    ],
)
