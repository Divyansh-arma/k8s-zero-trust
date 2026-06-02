"""
Pytest configuration and shared fixtures
"""
import os
import tempfile
import pytest
from app import create_app, db
from app.models import User, Category, Product


@pytest.fixture(scope='function')  # Changed from 'session' to 'function'
def app():
    """Create application for the tests."""
    # Create a temporary file to use as the database
    db_fd, db_path = tempfile.mkstemp()
    
    # Create the app with test configuration
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "WTF_CSRF_ENABLED": False,  # Disable CSRF for testing
        "SECRET_KEY": 'test-secret-key',
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()  # Clean up session
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
