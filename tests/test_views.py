"""Unit tests for views"""
import pytest
from pyramid import testing
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyrapad.models import Pad, DBSession, get_pad
from pyrapad import views


@pytest.mark.unit
class TestSaveView:
    """Tests for the save view"""

    def test_save_empty_data(self, app_config, db_session):
        """Test save view with no data shows form"""
        request = testing.DummyRequest()
        response = views.save(request)

        assert isinstance(response, dict)
        assert 'title' in response
        assert response['data'] == ''

    def test_save_new_pad(self, app_config, db_session):
        """Test creating a new pad"""
        request = testing.DummyRequest()
        request.params = {
            'data': 'print("hello")',
            'semail': '',  # Spam filter field
            'pad_id': '',
        }
        request.remote_addr = '127.0.0.1'

        response = views.save(request)

        assert isinstance(response, HTTPFound)
        assert '/' in response.location

    def test_save_spam_protection(self, app_config, db_session):
        """Test spam filter rejects submissions with email filled"""
        request = testing.DummyRequest()
        request.params = {
            'data': 'print("spam")',
            'semail': 'spam@example.com',  # Should trigger spam filter
            'pad_id': '',
        }

        response = views.save(request)

        assert isinstance(response, HTTPNotFound)

    def test_edit_existing_pad(self, app_config, db_session, sample_pad_data):
        """Test editing an existing pad"""
        # Create initial pad
        pad = Pad(**sample_pad_data)
        DBSession.add(pad)
        DBSession.flush()

        # Edit the pad
        request = testing.DummyRequest()
        request.params = {
            'data': 'print("updated")',
            'semail': '',
            'pad_id': str(pad.id),
        }
        request.remote_addr = '127.0.0.1'  # Same IP as original

        response = views.save(request)

        assert isinstance(response, HTTPFound)

        # Verify pad was updated
        updated_pad = get_pad(pad.id)
        assert updated_pad.data == 'print("updated")'


@pytest.mark.unit
class TestShowView:
    """Tests for the show view"""

    def test_show_existing_pad(self, app_config, db_session, sample_pad_data):
        """Test showing an existing pad"""
        pad = Pad(**sample_pad_data)
        DBSession.add(pad)
        DBSession.flush()

        request = testing.DummyRequest()
        request.matchdict = {'id': str(pad.id), 'uri': pad.uri}

        response = views.show(request)

        assert isinstance(response, dict)
        assert 'pad' in response
        assert 'pygdata' in response
        assert response['pad'].id == pad.id

    def test_show_nonexistent_pad(self, app_config, db_session):
        """Test showing a non-existent pad redirects home"""
        request = testing.DummyRequest()
        request.matchdict = {'id': '99999'}

        response = views.show(request)

        assert isinstance(response, HTTPFound)
        assert response.location == '/'

    def test_show_redirects_without_uri(self, app_config, db_session, sample_pad_data):
        """Test show redirects when URI is missing"""
        pad = Pad(**sample_pad_data)
        DBSession.add(pad)
        DBSession.flush()

        request = testing.DummyRequest()
        request.matchdict = {'id': str(pad.id)}  # No URI

        response = views.show(request)

        assert isinstance(response, HTTPFound)
        assert pad.uri in response.location


@pytest.mark.unit
class TestRawView:
    """Tests for the raw view"""

    def test_raw_returns_plain_text(self, app_config, db_session, sample_pad_data):
        """Test raw view returns plain text data"""
        pad = Pad(**sample_pad_data)
        DBSession.add(pad)
        DBSession.flush()

        request = testing.DummyRequest()
        request.matchdict = {'id': str(pad.id), 'uri': pad.uri}

        response = views.raw(request)

        assert response == pad.data


@pytest.mark.unit
class TestCloneView:
    """Tests for the clone view"""

    def test_clone_existing_pad(self, app_config, db_session, sample_pad_data):
        """Test cloning an existing pad"""
        pad = Pad(**sample_pad_data)
        DBSession.add(pad)
        DBSession.flush()

        request = testing.DummyRequest()
        request.matchdict = {'id': str(pad.id)}

        response = views.clone(request)

        assert isinstance(response, dict)
        assert response['data'] == pad.data
        assert response['pad_id'] == ''  # New pad, not edit


@pytest.mark.unit
class TestEditView:
    """Tests for the edit view"""

    def test_edit_view_loads_pad(self, app_config, db_session, sample_pad_data):
        """Test edit view loads pad data"""
        pad = Pad(**sample_pad_data)
        DBSession.add(pad)
        DBSession.flush()

        request = testing.DummyRequest()
        request.matchdict = {'id': str(pad.id)}

        response = views.edit(request)

        assert isinstance(response, dict)
        assert response['data'] == pad.data
        assert response['pad_id'] == str(pad.id)


@pytest.mark.unit
class TestRandomView:
    """Tests for the random view"""

    def test_random_redirects(self, app_config, db_session, sample_pad_data):
        """Test random view redirects to a pad"""
        # Create a pad
        pad = Pad(**sample_pad_data)
        DBSession.add(pad)
        DBSession.flush()

        request = testing.DummyRequest()
        response = views.random(request)

        assert isinstance(response, HTTPFound)
        assert '/' in response.location


@pytest.mark.unit
class TestRecentView:
    """Tests for the recent view"""

    def test_recent_shows_pads(self, app_config, db_session, sample_pad_data):
        """Test recent view shows list of pads"""
        # Create multiple pads
        for i in range(25):
            data = sample_pad_data.copy()
            data['uri'] = f'test-pad-{i}'
            pad = Pad(**data)
            DBSession.add(pad)
        DBSession.flush()

        request = testing.DummyRequest()
        request.params = {}

        response = views.recent(request)

        assert isinstance(response, dict)
        assert 'pads' in response
        assert response['pad_count'] == 25
        assert response['current_page'] == 1


@pytest.mark.unit
class TestSyntaxesView:
    """Tests for the syntaxes view"""

    def test_syntaxes_lists_all(self, app_config, db_session, sample_pad_data):
        """Test syntaxes view lists all unique syntaxes"""
        for syntax in ['python', 'javascript', 'ruby']:
            data = sample_pad_data.copy()
            data['uri'] = f'test-{syntax}'
            data['syntax'] = syntax
            pad = Pad(**data)
            DBSession.add(pad)
        DBSession.flush()

        request = testing.DummyRequest()
        response = views.syntaxes(request)

        assert isinstance(response, dict)
        assert 'syntaxes' in response
        assert len(response['syntaxes']) == 3


@pytest.mark.unit
class TestAlterView:
    """Tests for the alter view"""

    def test_alter_updates_uri(self, app_config, db_session, sample_pad_data):
        """Test alter view updates pad URI"""
        pad = Pad(**sample_pad_data)
        DBSession.add(pad)
        DBSession.flush()

        request = testing.DummyRequest(post={'save': '1'})
        request.matchdict = {'id': str(pad.id), 'uri': pad.uri}
        request.params = {
            'newuri': 'new-uri-name',
            'newsyntax': 'javascript',
        }
        request.POST = {'save': '1'}

        response = views.alter(request)

        assert isinstance(response, HTTPFound)

        # Verify pad was updated
        updated_pad = get_pad(pad.id)
        assert updated_pad.syntax == 'javascript'


@pytest.mark.unit
class TestGuessLexerName:
    """Tests for the guess_lexer_name helper"""

    def test_guess_python(self):
        """Test guessing Python syntax"""
        code = 'def hello():\n    print("world")'
        result = views.guess_lexer_name(code)
        assert result == 'python'

    def test_guess_unknown_returns_text(self):
        """Test unknown syntax returns 'text'"""
        code = 'asdfasdfasdf'
        result = views.guess_lexer_name(code)
        assert result == 'text'
