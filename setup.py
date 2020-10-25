import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

requires = [
    # Pyramid.
    "pyramid",
    "pyramid_mako",
    "pyramid_debugtoolbar",
    "pyramid_tm",
    "pyramid_retry",
    "plaster_pastedeploy",

    # Model.
    #"MySQL-python",
    # needed to pin because 2.0.0 breaks py 2.7 compatibility.
    "mysqlclient==1.4.6",
    "SQLAlchemy",
    "transaction",
    # needed to pin because 1.2 breaks py 2.7 compatibility.
    "zope.sqlalchemy==1.1",

    # misc.
    # needed to pin because 12.6.0 breaks py 2.7 compatibility.
    "pygments==2.5.2", # syntax highlighting
    "webhelpers", # pagination
    "ago", # human readable timedelta
    "slugify", # powerful uri slug lib
    "waitress", # web application server for development
    "uwsgi", # web application server for production
    
    # needed to pin because next 2.0.0 breaks py 2.7 compatibility.
    "MarkupSafe==1.1.1",
    ]

setup(
    name="pyrapad",
    version="0.1.0",
    description="pyrapad",
    long_description=README,
    classifiers=[
      "Programming Language :: Python",
      "Framework :: Pyramid"
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
    author="Russell Ballestrini",
    author_email="russell@ballestrini.net",
    url="https://pad.yohdah.com",
    keywords="pyramid application paste code pad app",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="pyrapad",
    install_requires = requires,
    entry_points = {
        "paste.app_factory": ["main = pyrapad:main"],
    },
)
