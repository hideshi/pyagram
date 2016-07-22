from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'pyagram',
    version = '1.1.2',
    description = 'Pyagram: Python Finite State Machine Diagram Generator',
    license = 'MIT License',
    author = 'Hideshi Ogoshi',
    author_email = 'hideshi.ogoshi@gmail.com',
    url = 'https://github.com/hideshi',
    bugtrack_url = 'https://github.com/hideshi/pyagram/issues',
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
    long_description = '''
Pyagram
=======

Python Finite State Machine Diagram Generator  

This is a command line tool, which generates finite state machine diagram for web and mobile application development from a source file through graphviz.  

The finite state machine diagram is a kind of diagram, which describes screen transitions and flows of the processes.  

The source file is written in a specific format, which enables us to write a code easier than using only graphviz, since Pyagram generates graphviz code as an intermediate file.  

Since graphviz provides 3 kinds of image formats, such as gif, png and svg, Pyagram provides these kinds of file format as well.  

There are several kinds of objects in the diagram.  

* Title of a diagram
* Double circle represents a view.
* Gray background circle represents a server side process including action.
* Dashed arrow represents a screen transition between views.
* Straight arrow represents flow of the process, such as accepting a request, validation, database access and so on.
* Straight arrow is able to have an label, which describes an action and a result of the process, such as clicking a button, success, error and so on.


How to write source file
------------------------

Firstly you can define a title of the diagram with @ sign.  
    

    @[title]
    CRUD View Diagram
    

Next you can define views with # sign and its screen transitions with --> sign.  

Now we have 3 views, such as List View, Add View and Server Error View.  

List View and Add View are connected one another.  

You can define its own path below the view name as well.  

I highly recommend you to define those views first, since that would help you when you are trying to define server processes as a guide.  
    

    #[List View]
    /index
    
    --> Add View
    
    #[Add View]
    /add
    
    --> List View
    
    --> Add View

    #[Server Error]


Then you can define server processes with ==> sign connecting source process and destination process.  

As you can see, process is able to have multiple flows. Each flow has its own destination.  

You can add results of the processes, such as Valid, Invalid, Success, Database Error and so on. It will be used as labels placed beside the straight arrows.  


    $[GET /index]
    ==> List View
    
    $[GET /add]
    ==> Add View
    
    $[POST /add]
    ==> Validate
    
    $[Validate]
    Valid
    ==> Save
    
    Invalid
    ==> Add View
    
    $[Save]
    ==> Add View
    
    $[Save]
    Success
    ==> List View
    
    Database error
    ==> Server Error
    
    
Now that you can define the flows between the views and the processes with ==> sign.  


    #[List View]
    /index
    
    --> Add View
    
    Click add button
    ==> GET /add
    

    #[Add View]
    /add
    
    --> List View
    
    --> Add View

    Click back button
    ==> GET /index
    
    Click submit button
    ==> POST /add


How to install
--------------

pip3 command installs depending library, such as pyparsing automatically.  

After the installation, executable pyagram command will be placed in a bin directory, such as /usr/local/bin/pyagram.  


    pip3 install pyagram


How to execute
--------------

pyagram command accepts 2 kinds of options.  

T option represents image type, which accepts gif, png and svg.  

I option represents source file, which accepts text file.  

Output file is placed in the same place as the source file.  


    pyagram -T {image type} -I {source file}

    
    ''',
)
