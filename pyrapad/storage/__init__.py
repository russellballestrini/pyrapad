"""Storage backend abstraction for pyrapad"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class StorageBackend(ABC):
    """Abstract base class for storage backends"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize storage backend with configuration

        Args:
            config: Configuration dictionary for the backend
        """
        self.config = config or {}

    @abstractmethod
    def save(self, key: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save content to storage

        Args:
            key: Unique identifier for the content
            content: The content to store
            metadata: Optional metadata about the content

        Returns:
            Storage URL or identifier where content was saved
        """
        pass

    @abstractmethod
    def retrieve(self, key: str) -> Optional[str]:
        """
        Retrieve content from storage

        Args:
            key: Unique identifier for the content

        Returns:
            The stored content, or None if not found
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        Delete content from storage

        Args:
            key: Unique identifier for the content

        Returns:
            True if deletion was successful, False otherwise
        """
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        Check if content exists in storage

        Args:
            key: Unique identifier for the content

        Returns:
            True if content exists, False otherwise
        """
        pass

    @abstractmethod
    def list_keys(self, prefix: Optional[str] = None) -> list[str]:
        """
        List all keys in storage

        Args:
            prefix: Optional prefix to filter keys

        Returns:
            List of storage keys
        """
        pass


def get_storage_backend(backend_type: str, config: Optional[Dict[str, Any]] = None) -> StorageBackend:
    """
    Factory function to get the appropriate storage backend

    Args:
        backend_type: Type of backend ('database', 'filesystem', 's3', 'pypi_vault')
        config: Configuration for the backend

    Returns:
        Initialized storage backend instance

    Raises:
        ValueError: If backend_type is not recognized
    """
    from pyrapad.storage.database import DatabaseBackend
    from pyrapad.storage.filesystem import FilesystemBackend
    from pyrapad.storage.s3 import S3Backend
    from pyrapad.storage.pypi_vault import PyPIVaultBackend

    backends = {
        'database': DatabaseBackend,
        'filesystem': FilesystemBackend,
        's3': S3Backend,
        'pypi_vault': PyPIVaultBackend,
    }

    if backend_type not in backends:
        raise ValueError(f"Unknown storage backend: {backend_type}. "
                         f"Available backends: {', '.join(backends.keys())}")

    return backends[backend_type](config)
