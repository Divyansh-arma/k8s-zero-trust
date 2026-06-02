"""
Main Flask application entry point for AWS Elastic Beanstalk
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))
from app import create_app

application = create_app()

if __name__ == "__main__":
    # Use environment variables for configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    application.run(host=host, port=port, debug=debug_mode)
    #