"""Unit tests for storage backends"""
import pytest
import tempfile
from pathlib import Path
from pyrapad.storage import get_storage_backend
from pyrapad.storage.database import DatabaseBackend
from pyrapad.storage.filesystem import FilesystemBackend


@pytest.mark.unit
class TestStorageFactory:
    """Tests for storage backend factory"""

    def test_get_database_backend(self):
        """Test getting database backend"""
        backend = get_storage_backend('database')
        assert isinstance(backend, DatabaseBackend)

    def test_get_filesystem_backend(self):
        """Test getting filesystem backend"""
        backend = get_storage_backend('filesystem', {'path': '/tmp/test'})
        assert isinstance(backend, FilesystemBackend)

    def test_unknown_backend_raises_error(self):
        """Test that unknown backend raises ValueError"""
        with pytest.raises(ValueError, match="Unknown storage backend"):
            get_storage_backend('unknown')


@pytest.mark.unit
class TestFilesystemBackend:
    """Tests for filesystem storage backend"""

    def test_save_and_retrieve(self):
        """Test saving and retrieving content"""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend({'path': tmpdir})

            # Save content
            key = 'test-pad-123'
            content = 'print("hello world")'
            result = backend.save(key, content)

            assert str(tmpdir) in result
            assert backend.exists(key)

            # Retrieve content
            retrieved = backend.retrieve(key)
            assert retrieved == content

    def test_delete(self):
        """Test deleting content"""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend({'path': tmpdir})

            key = 'test-pad-delete'
            backend.save(key, 'some content')
            assert backend.exists(key)

            # Delete
            result = backend.delete(key)
            assert result is True
            assert not backend.exists(key)

    def test_list_keys(self):
        """Test listing keys"""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend({'path': tmpdir})

            # Create multiple pads
            backend.save('pad-001', 'content 1')
            backend.save('pad-002', 'content 2')
            backend.save('pad-003', 'content 3')

            keys = backend.list_keys()
            assert len(keys) == 3
            assert 'pad-001' in keys
            assert 'pad-002' in keys
            assert 'pad-003' in keys

    def test_list_keys_with_prefix(self):
        """Test listing keys with prefix filter"""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend({'path': tmpdir})

            backend.save('python-001', 'python code')
            backend.save('python-002', 'more python')
            backend.save('javascript-001', 'js code')

            keys = backend.list_keys(prefix='python')
            assert len(keys) == 2
            assert 'python-001' in keys
            assert 'python-002' in keys
            assert 'javascript-001' not in keys

    def test_save_with_metadata(self):
        """Test saving content with metadata"""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend({'path': tmpdir})

            key = 'test-with-meta'
            content = 'test content'
            metadata = {'syntax': 'python', 'author': 'test'}

            backend.save(key, content, metadata)

            # Check metadata file exists
            meta_file = Path(tmpdir) / key[:2] / f"{key}.meta.json"
            assert meta_file.exists()

    def test_retrieve_nonexistent_key(self):
        """Test retrieving non-existent key returns None"""
        with tempfile.TemporaryDirectory() as tmpdir:
            backend = FilesystemBackend({'path': tmpdir})

            result = backend.retrieve('nonexistent-key')
            assert result is None
