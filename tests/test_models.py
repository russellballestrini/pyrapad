"""Unit tests for models"""
import pytest
from datetime import datetime
from pyrapad.models import Pad, get_pad, get_all_pads, get_all_syntaxes, DBSession


@pytest.mark.unit
class TestPadModel:
    """Tests for the Pad model"""

    def test_pad_creation(self, db_session, sample_pad_data):
        """Test creating a new pad"""
        pad = Pad(**sample_pad_data)
        assert pad.uri == 'test-pad'
        assert pad.data == sample_pad_data['data']
        assert pad.syntax == 'python'
        assert pad.ip_addr == '127.0.0.1'
        assert isinstance(pad.created, datetime)
        assert pad.disabled is False
        assert pad.wordwrap is False

    def test_pad_persistence(self, db_session, sample_pad_data):
        """Test saving and retrieving a pad"""
        pad = Pad(**sample_pad_data)
        DBSession.add(pad)
        DBSession.flush()

        assert pad.id is not None
        retrieved = DBSession.query(Pad).filter_by(id=pad.id).first()
        assert retrieved is not None
        assert retrieved.uri == 'test-pad'
        assert retrieved.data == sample_pad_data['data']

    def test_pad_unique_uri(self, db_session, sample_pad_data):
        """Test that URIs must be unique"""
        pad1 = Pad(**sample_pad_data)
        DBSession.add(pad1)
        DBSession.flush()

        # Try to create another pad with same URI
        pad2 = Pad(**sample_pad_data)
        DBSession.add(pad2)

        with pytest.raises(Exception):  # IntegrityError
            DBSession.flush()

    def test_pad_soft_delete(self, db_session, sample_pad_data):
        """Test soft delete functionality"""
        pad = Pad(**sample_pad_data)
        pad.disabled = True
        DBSession.add(pad)
        DBSession.flush()

        # get_all_pads should not return disabled pads
        pads = get_all_pads()
        assert pad not in pads

    def test_get_pad(self, db_session, sample_pad_data):
        """Test get_pad function"""
        pad = Pad(**sample_pad_data)
        DBSession.add(pad)
        DBSession.flush()

        retrieved = get_pad(pad.id)
        assert retrieved is not None
        assert retrieved.id == pad.id

        # Test non-existent pad
        assert get_pad(99999) is None

    def test_get_all_pads(self, db_session, sample_pad_data):
        """Test get_all_pads function"""
        # Create multiple pads
        for i in range(5):
            data = sample_pad_data.copy()
            data['uri'] = f'test-pad-{i}'
            pad = Pad(**data)
            DBSession.add(pad)
        DBSession.flush()

        pads = get_all_pads()
        assert len(pads) == 5

        # Should be ordered by id descending
        assert pads[0].id > pads[-1].id

    def test_get_all_syntaxes(self, db_session, sample_pad_data):
        """Test get_all_syntaxes function"""
        syntaxes = ['python', 'javascript', 'ruby', 'python']  # python appears twice

        for i, syntax in enumerate(syntaxes):
            data = sample_pad_data.copy()
            data['uri'] = f'test-pad-{i}'
            data['syntax'] = syntax
            pad = Pad(**data)
            DBSession.add(pad)
        DBSession.flush()

        result = get_all_syntaxes()
        unique_syntaxes = [s[0] for s in result if s[0] is not None]

        assert len(unique_syntaxes) == 3  # Should have 3 unique syntaxes
        assert 'python' in unique_syntaxes
        assert 'javascript' in unique_syntaxes
        assert 'ruby' in unique_syntaxes

    def test_pad_wordwrap_default(self, db_session, sample_pad_data):
        """Test wordwrap defaults to False"""
        pad = Pad(**sample_pad_data)
        assert pad.wordwrap is False

    def test_pad_without_syntax(self, db_session):
        """Test creating a pad without syntax"""
        pad = Pad(
            uri='no-syntax',
            data='Some plain text',
            ip_addr='127.0.0.1'
        )
        DBSession.add(pad)
        DBSession.flush()

        assert pad.syntax is None
        assert pad.id is not None
