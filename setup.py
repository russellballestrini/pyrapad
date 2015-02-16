import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_mako',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'MySQL-python',
    'zope.sqlalchemy',
    'pygments', # syntax highlighting
    'webhelpers', # pagination
    'ago', # human readable timedelta
    'pastescript', # paster
    'slugify', # powerful uri slug lib
    'waitress', # web application server for development
    'uwsgi', # web application server for production
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='pyrapad',
      version='0.0',
      description='pyrapad',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pyrapad',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = pyrapad:main
      """,
      paster_plugins=['pyramid'],
      )

