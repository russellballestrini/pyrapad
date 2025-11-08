"""Command line utilities for pyrapad"""
import sys
from pyrapad.models import DBSession, get_all_pads, initialize_sql
from pyrapad.storage import get_storage_backend
from sqlalchemy import create_engine


def migrate_storage():
    """Migrate pads from one storage backend to another"""
    import argparse

    parser = argparse.ArgumentParser(description='Migrate pad storage between backends')
    parser.add_argument('--from', dest='source', required=True,
                        choices=['database', 'filesystem', 's3', 'pypi_vault'],
                        help='Source storage backend')
    parser.add_argument('--to', dest='dest', required=True,
                        choices=['database', 'filesystem', 's3', 'pypi_vault'],
                        help='Destination storage backend')
    parser.add_argument('--db-url', default='sqlite:///pyrapad.db',
                        help='Database URL for database backend')
    parser.add_argument('--fs-path', default='./pads',
                        help='Filesystem path for filesystem backend')
    parser.add_argument('--s3-bucket', help='S3 bucket name')
    parser.add_argument('--s3-region', default='us-east-1', help='S3 region')
    parser.add_argument('--pypi-path', default='./pypi-vault',
                        help='PyPI vault path')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be migrated without actually doing it')

    args = parser.parse_args()

    # Build configuration for source and destination
    source_config = _build_config(args, args.source)
    dest_config = _build_config(args, args.dest)

    # Initialize backends
    source_backend = get_storage_backend(args.source, source_config)
    dest_backend = get_storage_backend(args.dest, dest_config)

    # If source is database, initialize database connection
    if args.source == 'database':
        engine = create_engine(args.db_url)
        initialize_sql(engine)
        pads = get_all_pads()

        print(f"Found {len(pads)} pads to migrate from database")

        for pad in pads:
            if args.dry_run:
                print(f"[DRY RUN] Would migrate pad {pad.id} (URI: {pad.uri})")
            else:
                # Migrate the pad
                metadata = {
                    'syntax': pad.syntax,
                    'created': pad.created.isoformat() if pad.created else None,
                    'ip_addr': pad.ip_addr,
                    'wordwrap': pad.wordwrap,
                }
                dest_backend.save(pad.uri, pad.data, metadata)
                print(f"Migrated pad {pad.id} (URI: {pad.uri})")

    else:
        # Migrate from non-database backend
        keys = source_backend.list_keys()
        print(f"Found {len(keys)} pads to migrate from {args.source}")

        for key in keys:
            if args.dry_run:
                print(f"[DRY RUN] Would migrate key: {key}")
            else:
                content = source_backend.retrieve(key)
                if content:
                    dest_backend.save(key, content)
                    print(f"Migrated key: {key}")

    if args.dry_run:
        print("\nDry run complete. No changes were made.")
    else:
        print(f"\nMigration complete! Migrated from {args.source} to {args.dest}")


def _build_config(args, backend_type):
    """Build configuration dictionary for a backend"""
    config = {}

    if backend_type == 'filesystem':
        config['path'] = args.fs_path
    elif backend_type == 's3':
        config['bucket'] = args.s3_bucket
        config['region'] = args.s3_region
    elif backend_type == 'pypi_vault':
        config['path'] = args.pypi_path

    return config


if __name__ == '__main__':
    migrate_storage()
