"""PyPI Vault storage backend - stores pad data in PyPI-compatible package repository"""
import hashlib
from typing import Optional, Dict, Any
from pyrapad.storage import StorageBackend


class PyPIVaultBackend(StorageBackend):
    """
    PyPI Vault storage backend

    Stores pad content using PyPI simple repository format.
    This backend creates pseudo-packages where each pad is stored
    as a "distribution" in a PyPI-like structure.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.vault_url = self.config.get('url', 'https://pypi.example.com')
        self.base_path = self.config.get('path', './pypi-vault')

        # For file-based PyPI vault
        if self.base_path:
            from pathlib import Path
            Path(self.base_path).mkdir(parents=True, exist_ok=True)

    def _get_package_name(self, key: str) -> str:
        """Convert pad key to PyPI package name"""
        # PyPI package names: lowercase, hyphens allowed
        return f"pyrapad-{key.lower()}"

    def _get_simple_path(self, package_name: str) -> str:
        """Get the simple API path for a package"""
        # PyPI simple repository structure: /simple/{package}/
        return f"{self.base_path}/simple/{package_name}"

    def save(self, key: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save content to PyPI vault

        Creates a pseudo-package with the content as the distribution.
        """
        package_name = self._get_package_name(key)

        # File-based PyPI vault
        if self.base_path:
            from pathlib import Path
            import json

            package_dir = Path(self._get_simple_path(package_name))
            package_dir.mkdir(parents=True, exist_ok=True)

            # Create package file (using content hash as version)
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()[:8]
            version = f"1.0.{content_hash}"

            # Save content as a "distribution"
            dist_file = package_dir / f"{package_name}-{version}.txt"
            dist_file.write_text(content, encoding='utf-8')

            # Create index.html for simple API
            index_html = f"""<!DOCTYPE html>
<html>
<head><title>Links for {package_name}</title></head>
<body>
<h1>Links for {package_name}</h1>
<a href="{package_name}-{version}.txt">{package_name}-{version}.txt</a><br/>
</body>
</html>"""
            (package_dir / 'index.html').write_text(index_html)

            # Save metadata
            if metadata:
                meta_file = package_dir / f"{package_name}-{version}.meta.json"
                meta_file.write_text(json.dumps(metadata), encoding='utf-8')

            return f"pypi://{package_name}/{version}"

        # Remote PyPI vault (would require HTTP API calls)
        return f"{self.vault_url}/simple/{package_name}"

    def retrieve(self, key: str) -> Optional[str]:
        """Retrieve content from PyPI vault"""
        package_name = self._get_package_name(key)

        if self.base_path:
            from pathlib import Path

            package_dir = Path(self._get_simple_path(package_name))
            if not package_dir.exists():
                return None

            # Find latest distribution file
            dist_files = list(package_dir.glob(f"{package_name}-*.txt"))
            if not dist_files:
                return None

            # Return content from latest version (sorted by name)
            latest_file = sorted(dist_files)[-1]
            return latest_file.read_text(encoding='utf-8')

        return None

    def delete(self, key: str) -> bool:
        """Delete content from PyPI vault"""
        package_name = self._get_package_name(key)

        if self.base_path:
            from pathlib import Path
            import shutil

            package_dir = Path(self._get_simple_path(package_name))
            if package_dir.exists():
                shutil.rmtree(package_dir)
                return True

        return False

    def exists(self, key: str) -> bool:
        """Check if content exists in PyPI vault"""
        package_name = self._get_package_name(key)

        if self.base_path:
            from pathlib import Path
            package_dir = Path(self._get_simple_path(package_name))
            return package_dir.exists()

        return False

    def list_keys(self, prefix: Optional[str] = None) -> list[str]:
        """List all keys in PyPI vault"""
        keys = []

        if self.base_path:
            from pathlib import Path

            simple_dir = Path(self.base_path) / 'simple'
            if not simple_dir.exists():
                return keys

            for package_dir in simple_dir.iterdir():
                if package_dir.is_dir():
                    # Extract original key from package name
                    # pyrapad-abc123 -> abc123
                    package_name = package_dir.name
                    if package_name.startswith('pyrapad-'):
                        key = package_name[8:]  # Remove 'pyrapad-' prefix
                        if prefix is None or key.startswith(prefix):
                            keys.append(key)

        return sorted(keys)
