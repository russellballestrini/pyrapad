"""Filesystem storage backend - stores pad data as files"""
import os
from pathlib import Path
from typing import Optional, Dict, Any
from pyrapad.storage import StorageBackend


class FilesystemBackend(StorageBackend):
    """
    Filesystem storage backend

    Stores pad content as individual files in a directory structure.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.base_path = Path(self.config.get('path', './pads'))
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, key: str) -> Path:
        """Get the filesystem path for a given key"""
        # Use first 2 chars of key for subdirectory (sharding)
        subdir = key[:2] if len(key) >= 2 else '00'
        file_path = self.base_path / subdir / f"{key}.txt"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return file_path

    def save(self, key: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Save content to filesystem"""
        file_path = self._get_file_path(key)
        file_path.write_text(content, encoding='utf-8')

        # Save metadata if provided
        if metadata:
            meta_path = file_path.with_suffix('.meta.json')
            import json
            meta_path.write_text(json.dumps(metadata), encoding='utf-8')

        return str(file_path)

    def retrieve(self, key: str) -> Optional[str]:
        """Retrieve content from filesystem"""
        file_path = self._get_file_path(key)
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
        return None

    def delete(self, key: str) -> bool:
        """Delete content from filesystem"""
        file_path = self._get_file_path(key)
        meta_path = file_path.with_suffix('.meta.json')

        deleted = False
        if file_path.exists():
            file_path.unlink()
            deleted = True

        if meta_path.exists():
            meta_path.unlink()

        return deleted

    def exists(self, key: str) -> bool:
        """Check if content exists in filesystem"""
        return self._get_file_path(key).exists()

    def list_keys(self, prefix: Optional[str] = None) -> list[str]:
        """List all keys in filesystem"""
        keys = []
        for file_path in self.base_path.rglob('*.txt'):
            key = file_path.stem
            if prefix is None or key.startswith(prefix):
                keys.append(key)
        return sorted(keys)
