from setuptools import setup

setup(
    name = 'pyagram',
    version = '1.0.4',
    description = 'Pyagram: Python Finite State Machine Diagram Generator',
    author = 'Hideshi Ogoshi',
    author_email = 'hideshi.ogoshi@gmail.com',
    url = 'https://github.com/hideshi',
    bugtrack_url = 'https://github.com/hideshi/pyagram/issues',
    packages = ['pyagram'],
    install_requires=[
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
