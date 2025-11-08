"""FileVault storage backend - stores pad data using filevault package"""
from typing import Optional, Dict, Any
from pathlib import Path
from pyrapad.storage import StorageBackend


class FileVaultBackend(StorageBackend):
    """
    FileVault storage backend

    Uses the filevault package to store pad content in a hash-based
    directory tree structure for efficient organization and retrieval.

    See: https://pypi.org/project/filevault/
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.vault_path = self.config.get('path', './file-vault')
        self.depth = self.config.get('depth', 2)
        self.salt = self.config.get('salt', 'pyrapad')

        # Initialize vault (lazy loaded)
        self._vault = None

    @property
    def vault(self):
        """Lazy load FileVault Vault instance"""
        if self._vault is None:
            try:
                from filevault import Vault
                self._vault = Vault(
                    vaultpath=self.vault_path,
                    depth=self.depth,
                    salt=self.salt
                )
                # Ensure vault path exists
                Path(self.vault_path).mkdir(parents=True, exist_ok=True)
            except ImportError:
                raise ImportError("filevault is required for PyPIVaultBackend. "
                                  "Install with: pip install filevault")
        return self._vault

    def save(self, key: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save content to file vault

        Uses the key to generate a hash-based filename and stores the content.

        Args:
            key: Unique identifier (pad URI)
            content: The content to store
            metadata: Optional metadata about the content

        Returns:
            The vault path where content was saved
        """
        # Create filename based on key (hash-based path)
        vault_filename = self.vault.create_filename(key, '.txt', absolute=True)

        # Ensure parent directory exists
        Path(vault_filename).parent.mkdir(parents=True, exist_ok=True)

        # Write content to vault file
        with open(vault_filename, 'w', encoding='utf-8') as f:
            f.write(content)

        # Save metadata if provided
        if metadata:
            import json
            meta_filename = vault_filename.replace('.txt', '.meta.json')
            with open(meta_filename, 'w', encoding='utf-8') as f:
                json.dump(metadata, f)

        return vault_filename

    def retrieve(self, key: str) -> Optional[str]:
        """
        Retrieve content from file vault

        Args:
            key: Unique identifier (pad URI)

        Returns:
            The stored content, or None if not found
        """
        vault_filename = self.vault.create_filename(key, '.txt', absolute=True)

        try:
            with open(vault_filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None

    def delete(self, key: str) -> bool:
        """
        Delete content from file vault

        Args:
            key: Unique identifier (pad URI)

        Returns:
            True if deletion was successful, False otherwise
        """
        vault_filename = self.vault.create_filename(key, '.txt', absolute=True)
        meta_filename = vault_filename.replace('.txt', '.meta.json')

        deleted = False
        try:
            Path(vault_filename).unlink()
            deleted = True
        except FileNotFoundError:
            pass

        # Also delete metadata if it exists
        try:
            Path(meta_filename).unlink()
        except FileNotFoundError:
            pass

        return deleted

    def exists(self, key: str) -> bool:
        """
        Check if content exists in file vault

        Args:
            key: Unique identifier (pad URI)

        Returns:
            True if content exists, False otherwise
        """
        vault_filename = self.vault.create_filename(key, '.txt', absolute=True)
        return Path(vault_filename).exists()

    def list_keys(self, prefix: Optional[str] = None) -> list[str]:
        """
        List all keys in file vault

        Note: This requires iterating through the vault directory structure
        and reverse-engineering keys from filenames, which is not directly
        supported by filevault. This is a limitation of the hash-based storage.

        Args:
            prefix: Optional prefix to filter keys (not supported)

        Returns:
            List of storage keys (may be limited)
        """
        keys = []
        vault_path = Path(self.vault_path)

        if not vault_path.exists():
            return keys

        # Walk through the vault directory to find all .txt files
        for txt_file in vault_path.rglob('*.txt'):
            # Extract relative path from vault root
            rel_path = txt_file.relative_to(vault_path)
            # The filename (without .txt) is the hash
            # We can't easily reverse the hash to get the original key
            # So we'll return the hash as the identifier
            hash_key = txt_file.stem
            keys.append(hash_key)

        return sorted(keys)

    def get_metadata(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve metadata for a key

        Args:
            key: Unique identifier (pad URI)

        Returns:
            Metadata dictionary, or None if not found
        """
        vault_filename = self.vault.create_filename(key, '.txt', absolute=True)
        meta_filename = vault_filename.replace('.txt', '.meta.json')

        try:
            import json
            with open(meta_filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
