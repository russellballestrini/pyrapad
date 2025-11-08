# Pyrapad - Modern Code Paste Application

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A modern code paste sharing application with syntax highlighting, code execution, and multiple storage backends.

**Live Demo:** https://pad.yohdah.com

## ✨ Features

- **Syntax Highlighting**: Support for 400+ programming languages via Pygments
- **Code Execution**: Run code directly in browser using secure Docker sandboxes
- **Multiple Storage Backends**:
  - Database (SQLite/MySQL)
  - Filesystem
  - AWS S3 / S3-compatible storage
  - PyPI Vault (custom package-based storage)
- **Modern Python 3.11+**: Fully migrated from Python 2.7
- **SQLAlchemy 2.0**: Type-safe models with Alembic migrations
- **Pyramid 2.x**: Latest web framework features
- **Comprehensive Tests**: 80%+ code coverage with pytest

## 🚀 Quick Start

### Requirements

- Python 3.11 or higher
- SQLite (included) or MySQL (optional)
- Docker (optional, for code execution)

### Installation

```bash
# Clone the repository
git clone https://github.com/russellballestrini/pyrapad.git
cd pyrapad

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Install optional features
pip install -e ".[sandbox]"  # For code execution
pip install -e ".[mysql]"    # For MySQL support
pip install -e ".[s3]"       # For S3 storage
pip install -e ".[dev]"      # For development/testing

# Run database migrations
alembic upgrade head

# Start the development server
pserve development.ini
```

Visit http://localhost:6543 to see your local instance!

## 📖 Usage

### Creating a Pad

1. Navigate to the homepage
2. Paste your code
3. Optional: Select syntax highlighting language
4. Click "Submit"
5. Share the generated URL

### Running Code

1. View any pad
2. Click the "Run Code" button
3. See execution results inline

### Storage Backends

Configure storage backend in `development.ini`:

```ini
# Database storage (default)
storage.backend = database

# Filesystem storage
storage.backend = filesystem
storage.filesystem.path = ./pads

# S3 storage
storage.backend = s3
storage.s3.bucket = my-pads
storage.s3.region = us-east-1

# PyPI Vault storage
storage.backend = pypi_vault
storage.pypi_vault.path = ./pypi-vault
```

### Migrating Storage

Migrate pads between storage backends:

```bash
# Migrate from database to filesystem
pyrapad-migrate-storage --from database --to filesystem --fs-path ./pads

# Migrate from filesystem to S3
pyrapad-migrate-storage --from filesystem --to s3 \\
  --fs-path ./pads --s3-bucket my-bucket --s3-region us-east-1

# Dry run (preview without changes)
pyrapad-migrate-storage --from database --to filesystem --dry-run
```

## 🧪 Testing

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=pyrapad --cov-report=html

# Run specific test categories
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only
pytest -m functional     # Functional/E2E tests only
```

## 🏗️ Architecture

### Project Structure

```
pyrapad/
├── pyrapad/                # Main package
│   ├── __init__.py        # App factory
│   ├── models.py          # SQLAlchemy models
│   ├── views.py           # View handlers
│   ├── storage/           # Storage backends
│   │   ├── __init__.py   # Base interface
│   │   ├── database.py   # Database backend
│   │   ├── filesystem.py # Filesystem backend
│   │   ├── s3.py         # S3 backend
│   │   └── pypi_vault.py # PyPI vault backend
│   ├── sandbox/           # Code execution
│   │   ├── __init__.py
│   │   └── executor.py   # Docker sandbox executor
│   ├── templates/         # Mako templates
│   ├── static/            # CSS, JS, images
│   └── lib/               # Utilities
├── tests/                 # Test suite
│   ├── conftest.py       # Pytest fixtures
│   ├── test_models.py    # Model tests
│   ├── test_views.py     # View tests
│   └── test_storage.py   # Storage tests
├── alembic/               # Database migrations
├── setup.py               # Package configuration
├── pytest.ini             # Test configuration
└── development.ini        # App configuration
```

### Database Schema

```sql
CREATE TABLE pad (
    id INTEGER PRIMARY KEY,
    uri VARCHAR(64) UNIQUE NOT NULL,
    syntax VARCHAR(16),
    data TEXT NOT NULL,
    disabled BOOLEAN DEFAULT FALSE,
    wordwrap BOOLEAN DEFAULT FALSE,
    created DATETIME,
    ip_addr VARCHAR(64)
);
```

## 🔒 Security

### Code Execution Sandbox

Code execution uses Docker with multiple security layers:

- **Network Isolation**: No network access
- **Resource Limits**: CPU and memory restrictions
- **Read-Only Filesystem**: Immutable container filesystem
- **Capability Dropping**: No privileged operations
- **Timeout Protection**: Automatic termination after 5 seconds

### Supported Languages

- Python 3.11
- JavaScript (Node.js 20)
- Ruby 3
- Bash

## 📦 Deployment

### Production Configuration

1. Update `production.ini`:
```ini
[app:main]
use = egg:pyrapad

pyramid.reload_templates = false
pyramid.debug_authorization = false
pyramid.debug_notfound = false

sqlalchemy.url = mysql://user:pass@localhost/pyrapad

storage.backend = s3
storage.s3.bucket = production-pads
storage.s3.region = us-east-1

sandbox.enabled = true
sandbox.timeout = 5
sandbox.memory_limit = 128m
```

2. Use production server:
```bash
# Install uWSGI
pip install -e ".[uwsgi]"

# Run with uWSGI
uwsgi --ini-paste production.ini
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install -e ".[production]"
RUN alembic upgrade head

EXPOSE 6543
CMD ["pserve", "production.ini"]
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Russell Ballestrini**
- Email: russell@ballestrini.net
- Website: https://pad.yohdah.com

## 🙏 Acknowledgments

- **Pyramid Framework** - Modern Python web framework
- **SQLAlchemy** - The Python SQL toolkit
- **Pygments** - Syntax highlighting library
- **Docker** - Containerization platform

## 📊 Project Status

- ✅ Python 3.11+ migration complete
- ✅ SQLAlchemy 2.0 migration complete
- ✅ Multiple storage backends implemented
- ✅ Code execution sandbox implemented
- ✅ Comprehensive test suite (80%+ coverage)
- 🚧 UI improvements in progress
- 🚧 Authentication system planned

---

**Note**: This is version 2.0.0, a complete rewrite from the original Python 2.7 codebase with modern features and architecture.
