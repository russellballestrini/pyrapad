"""Pytest configuration and fixtures"""
import pytest
from pyramid import testing
from pyramid.config import Configurator
from webtest import TestApp
from sqlalchemy import create_engine
from pyrapad.models import Base, DBSession, initialize_sql


@pytest.fixture
def app_config():
    """Create Pyramid testing configuration"""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:',
        'mako.directories': 'pyrapad:templates',
        'google_analytics_key': '',
    })
    yield config
    testing.tearDown()


@pytest.fixture
def db_session():
    """Create in-memory SQLite database session"""
    engine = create_engine('sqlite:///:memory:')
    session = initialize_sql(engine)
    yield session
    session.remove()
    Base.metadata.drop_all(engine)


@pytest.fixture
def testapp():
    """Create WebTest application for functional testing"""
    from pyrapad import main
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:',
        'mako.directories': 'pyrapad:templates',
        'google_analytics_key': '',
        'pyramid.includes': '',  # Disable debugtoolbar for tests
    }
    app = main({}, **settings)
    return TestApp(app)


@pytest.fixture
def sample_pad_data():
    """Sample pad data for testing"""
    return {
        'uri': 'test-pad',
        'data': 'def hello():\n    print("Hello, World!")\n',
        'syntax': 'python',
        'ip_addr': '127.0.0.1',
    }
