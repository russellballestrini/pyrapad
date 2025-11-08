import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

requires = [
    # Pyramid - Modern Python 3 versions
    "pyramid>=2.0.2,<3.0",
    "pyramid_mako>=1.1.0,<2.0",
    "pyramid_debugtoolbar>=4.10,<5.0",
    "pyramid_tm>=2.5,<3.0",
    "pyramid_retry>=2.1.1,<3.0",
    "plaster_pastedeploy>=1.0.1,<2.0",

    # Database - SQLAlchemy 2.0 + migrations
    "SQLAlchemy>=2.0.25,<3.0",
    "alembic>=1.13.1,<2.0",
    "transaction>=4.0,<5.0",
    "zope.sqlalchemy>=3.1,<4.0",

    # Utilities - Latest stable versions
    "pygments>=2.17.2,<3.0",  # syntax highlighting
    "paginate>=0.5.7,<1.0",  # pagination (standalone package)
    "ago>=0.0.95,<1.0",  # human readable timedelta
    "python-slugify>=8.0.1,<9.0",  # powerful uri slug lib (renamed package)
    "waitress>=3.0.0,<4.0",  # web application server for development
    "MarkupSafe>=2.1.5,<3.0",  # template safety
    ]

# Optional dependencies for production and extended features
mysql_requires = [
    "mysqlclient>=2.2.1,<3.0",
]

s3_requires = [
    "boto3>=1.34.0,<2.0",
]

sandbox_requires = [
    "docker>=7.0.0,<8.0",
]

uwsgi_requires = [
    "uwsgi>=2.0.24,<3.0",
]

dev_requires = [
    # Testing
    "pytest>=8.0.0,<9.0",
    "pytest-cov>=4.1.0,<5.0",
    "pytest-mock>=3.12.0,<4.0",
    "WebTest>=3.0.0,<4.0",  # Functional testing for Pyramid

    # Code quality
    "black>=24.0.0,<25.0",
    "flake8>=7.0.0,<8.0",
    "mypy>=1.8.0,<2.0",
    ]

setup(
    name="pyrapad",
    version="2.0.0",  # Major version bump for Python 3 rewrite
    description="Code paste sharing application with syntax highlighting and execution",
    long_description=README,
    long_description_content_type="text/x-rst",
    classifiers=[
      "Programming Language :: Python",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.11",
      "Programming Language :: Python :: 3.12",
      "Framework :: Pyramid",
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
    author="Russell Ballestrini",
    author_email="russell@ballestrini.net",
    url="https://pad.yohdah.com",
    keywords="pyramid application paste code pad app pastebin syntax-highlighting",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=requires,
    extras_require={
        "dev": dev_requires,
        "testing": dev_requires,
        "mysql": mysql_requires,
        "s3": s3_requires,
        "sandbox": sandbox_requires,
        "uwsgi": uwsgi_requires,
        "production": mysql_requires + uwsgi_requires,
        "all": mysql_requires + s3_requires + sandbox_requires + uwsgi_requires + dev_requires,
    },
    entry_points={
        "paste.app_factory": ["main = pyrapad:main"],
        "console_scripts": [
            "pyrapad-migrate-storage = pyrapad.cli:migrate_storage",
        ],
    },
)
