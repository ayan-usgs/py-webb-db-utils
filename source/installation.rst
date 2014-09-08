Package Installation
*****************************
If not already installed, you will want to install Python 2.7. Downloads can be found
at https://www.python.org/download/releases/. The 32-bit verson of Python is recommended
as it is better supported by the Python community.

A complier may also need to be installed. 

There are a number of Python package dependencies that are required for the running
of this package. These dependencies are summarized in requirements.txt and are summarized
here for convenience. All of these packages may be installed using pip 
(e.g. ``pip install python-dateutil``).

- SQLAlchemy==0.9.7
- cx-Oracle==5.1.3
- numpy==1.8.1
- pandas==0.14.1
- python-dateutil==2.2
- pytz==2014.4
- six==1.7.3

Some of these dependencies may prove difficult to install on Windows. If this is a problem, Anaconda
(http://continuum.io/download), a SciPy distribution, will have many of the necessary dependencies
ready to go. Alternatively, unofficial binaries of these packages may be found from the University of
California, Irvine at http://www.lfd.uci.edu/~gohlke/pythonlibs/.