from distutils.core import setup

setup(
    name='WEBB_DB_UTILS',
    version='0.1.0',
    author='Andrew Yan',
    author_email='ayan@usgs.gov',
    packages=['webb_utils'],
    license='LICENSE.txt',
    description='Python package for create dataframes and exports from the WEBB Database',
    long_description=open('README.txt').read(),
    install_requires=[
        "SQLAlchemy == 0.9.7",
        "cx-Oracle == 5.1.3",
        "numpy == 1.8.1",
        "openpyxl == 1.8.6",
        "pandas == 0.14.1",
        "python-dateutil == 2.2",
        "pytz == 2014.4",
        "six == 1.7.3",
    ],
)