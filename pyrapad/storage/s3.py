"""S3 storage backend - stores pad data in AWS S3 or S3-compatible storage"""
from typing import Optional, Dict, Any
from pyrapad.storage import StorageBackend


class S3Backend(StorageBackend):
    """
    S3 storage backend

    Stores pad content in AWS S3 or S3-compatible object storage (MinIO, etc.)
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.bucket = self.config.get('bucket', 'pyrapad-storage')
        self.region = self.config.get('region', 'us-east-1')
        self.endpoint_url = self.config.get('endpoint_url')  # For S3-compatible services

        # Initialize S3 client (lazy loaded)
        self._client = None

    @property
    def client(self):
        """Lazy load boto3 S3 client"""
        if self._client is None:
            try:
                import boto3
                self._client = boto3.client(
                    's3',
                    region_name=self.region,
                    endpoint_url=self.endpoint_url
                )
                # Ensure bucket exists
                try:
                    self._client.head_bucket(Bucket=self.bucket)
                except:
                    self._client.create_bucket(Bucket=self.bucket)
            except ImportError:
                raise ImportError("boto3 is required for S3Backend. "
                                  "Install with: pip install pyrapad[s3]")
        return self._client

    def _get_s3_key(self, key: str) -> str:
        """Get the S3 object key for a given pad key"""
        # Use first 2 chars for prefix (sharding)
        prefix = key[:2] if len(key) >= 2 else '00'
        return f"pads/{prefix}/{key}.txt"

    def save(self, key: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Save content to S3"""
        s3_key = self._get_s3_key(key)
        extra_args = {}

        if metadata:
            # S3 metadata must be string values
            extra_args['Metadata'] = {k: str(v) for k, v in metadata.items()}

        self.client.put_object(
            Bucket=self.bucket,
            Key=s3_key,
            Body=content.encode('utf-8'),
            ContentType='text/plain',
            **extra_args
        )

        return f"s3://{self.bucket}/{s3_key}"

    def retrieve(self, key: str) -> Optional[str]:
        """Retrieve content from S3"""
        s3_key = self._get_s3_key(key)
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=s3_key)
            return response['Body'].read().decode('utf-8')
        except self.client.exceptions.NoSuchKey:
            return None

    def delete(self, key: str) -> bool:
        """Delete content from S3"""
        s3_key = self._get_s3_key(key)
        try:
            self.client.delete_object(Bucket=self.bucket, Key=s3_key)
            return True
        except Exception:
            return False

    def exists(self, key: str) -> bool:
        """Check if content exists in S3"""
        s3_key = self._get_s3_key(key)
        try:
            self.client.head_object(Bucket=self.bucket, Key=s3_key)
            return True
        except:
            return False

    def list_keys(self, prefix: Optional[str] = None) -> list[str]:
        """List all keys in S3"""
        keys = []
        paginator = self.client.get_paginator('list_objects_v2')

        s3_prefix = 'pads/'
        for page in paginator.paginate(Bucket=self.bucket, Prefix=s3_prefix):
            for obj in page.get('Contents', []):
                # Extract key from path: pads/ab/abc123.txt -> abc123
                s3_key = obj['Key']
                if s3_key.endswith('.txt'):
                    key = s3_key.split('/')[-1][:-4]  # Remove .txt extension
                    if prefix is None or key.startswith(prefix):
                        keys.append(key)

        return sorted(keys)
