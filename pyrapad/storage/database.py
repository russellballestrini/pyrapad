"""Database storage backend - stores pad data in database"""
from typing import Optional, Dict, Any
from pyrapad.storage import StorageBackend


class DatabaseBackend(StorageBackend):
    """
    Database storage backend

    This is the default/legacy behavior where pad content
    is stored directly in the database 'data' column.
    """

    def save(self, key: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save content to database

        For DatabaseBackend, the actual saving happens in the Pad model,
        so this method just returns the key as a placeholder.

        Args:
            key: Unique identifier (pad URI)
            content: The content to store
            metadata: Optional metadata (unused for database backend)

        Returns:
            The key (pad URI)
        """
        # Database storage is handled directly by the Pad model
        # This method exists for interface consistency
        return key

    def retrieve(self, key: str) -> Optional[str]:
        """
        Retrieve content from database

        For DatabaseBackend, retrieval happens through the Pad model,
        so this method is a placeholder.

        Args:
            key: Unique identifier (pad URI)

        Returns:
            None (retrieval handled by Pad model)
        """
        # Database retrieval is handled directly by the Pad model
        # This method exists for interface consistency
        return None

    def delete(self, key: str) -> bool:
        """
        Delete content from database

        For DatabaseBackend, deletion happens through the Pad model,
        so this method is a placeholder.

        Args:
            key: Unique identifier (pad URI)

        Returns:
            True (deletion handled by Pad model)
        """
        # Database deletion is handled by setting Pad.disabled = True
        # This method exists for interface consistency
        return True

    def exists(self, key: str) -> bool:
        """
        Check if content exists in database

        Args:
            key: Unique identifier (pad URI)

        Returns:
            True (existence check handled by Pad model)
        """
        # Existence check is handled by the Pad model
        # This method exists for interface consistency
        return True

    def list_keys(self, prefix: Optional[str] = None) -> list[str]:
        """
        List all keys in database

        Args:
            prefix: Optional prefix to filter keys

        Returns:
            Empty list (listing handled by Pad model)
        """
        # Listing is handled by get_all_pads()
        # This method exists for interface consistency
        return []
