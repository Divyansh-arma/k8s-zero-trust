"""
Flask application factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import threading

db = SQLAlchemy()
login_manager = LoginManager()
db_lock = threading.Lock()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ecommerce.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enhanced database configuration for production
    engine_options = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Database-specific configurations
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if 'mysql' in db_uri:
        # MySQL-specific configurations
        engine_options.update({
            'pool_size': 10,
            'max_overflow': 20,
            'pool_timeout': 30,
            'connect_args': {
                'connect_timeout': 10,
                'charset': 'utf8mb4',
                'autocommit': True
            }
        })
    elif 'sqlite' in db_uri:
        # SQLite-specific configurations
        engine_options.update({
            'connect_args': {
                'timeout': 20
            }
        })
    else:
        # Default configurations for other databases
        engine_options.update({
            'pool_size': 10,
            'max_overflow': 20,
            'pool_timeout': 30,
            'connect_args': {
                'timeout': 20
            }
        })
    
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = engine_options
    app.config['STRIPE_PUBLISHABLE_KEY'] = os.environ.get('STRIPE_PUBLISHABLE_KEY', '')
    app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY', '')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.cart import bp as cart_bp
    app.register_blueprint(cart_bp, url_prefix='/cart')
    
    # Create database tables
    with app.app_context():
        init_database()
    
    return app

def init_database():
    """Initialize database with proper error handling and concurrency control"""
    import time
    from sqlalchemy.exc import OperationalError
    
    max_retries = 5
    retry_delay = 2
    
    with db_lock:
        for attempt in range(max_retries):
            try:
                # Import models to ensure they're registered
                from app.models import User, Category, Product, CartItem, Order, OrderItem
                
                print(f"Database initialization attempt {attempt + 1}/{max_retries}")
                
                # Create all tables with retry logic
                db.create_all()
                
                # Verify tables exist by making a simple query
                User.query.limit(1).all()
                Category.query.limit(1).all()
                Product.query.limit(1).all()
                
                # Check if we need to create sample data
                try:
                    if Category.query.count() == 0:
                        create_sample_data()
                except:
                    print("Sample data creation skipped - tables may already exist")
                
                print("Database initialization successful")
                return
                
            except OperationalError as e:
                error_msg = str(e)
                if "was skipped since its definition is being modified by concurrent DDL statement" in error_msg:
                    print(f"Database table lock detected (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        retry_delay *= 1.5  # Exponential backoff
                        continue
                    else:
                        print("Max retries reached. Continuing without database initialization.")
                        return
                else:
                    print(f"Other database error: {e}")
                    break
                    
            except Exception as e:
                print(f"Database initialization error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print("Max retries reached. Continuing without database initialization.")
                    return
            
            finally:
                # Always try to clean up the session
                try:
                    db.session.rollback()
                except:
                    pass
def create_sample_data():
    """Create sample products and categories for demo purposes"""
    try:
        from app.models import Product, Category
        
        print("Creating sample data...")
        
        # Check if data already exists to avoid conflicts
        if Category.query.count() > 0:
            print("Sample data already exists, skipping creation")
            return
        
        # Create categories
        electronics = Category(name='Electronics', description='Electronic devices and gadgets')
        clothing = Category(name='Clothing', description='Fashion and apparel')
        books = Category(name='Books', description='Books and literature')
        
        db.session.add_all([electronics, clothing, books])
        db.session.flush()  # Get IDs without committing
        
        # Create sample products
        products = [
            Product(
                name='Wireless Headphones',
                description='High-quality wireless headphones with noise cancellation',
                price=99.99,
                stock=50,
                category_id=electronics.id,
                image_url='https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=400'
            ),
            Product(
                name='Smartphone',
                description='Latest smartphone with advanced features',
                price=699.99,
                stock=30,
                category_id=electronics.id,
                image_url='https://images.pexels.com/photos/404280/pexels-photo-404280.jpeg?auto=compress&cs=tinysrgb&w=400'
            ),
            Product(
                name='Classic T-Shirt',
                description='Comfortable cotton t-shirt in various colors',
                price=19.99,
                stock=100,
                category_id=clothing.id,
                image_url='https://images.pexels.com/photos/8532616/pexels-photo-8532616.jpeg?auto=compress&cs=tinysrgb&w=400'
            ),
            Product(
                name='Programming Guide',
                description='Complete guide to modern programming practices',
                price=29.99,
                stock=75,
                category_id=books.id,
                image_url='https://images.pexels.com/photos/256417/pexels-photo-256417.jpeg?auto=compress&cs=tinysrgb&w=400'
            ),
            Product(
                name='Laptop',
                description='High-performance laptop for professionals',
                price=1299.99,
                stock=15,
                category_id=electronics.id,
                image_url='https://images.pexels.com/photos/205421/pexels-photo-205421.jpeg?auto=compress&cs=tinysrgb&w=400'
            ),
            Product(
                name='Designer Jacket',
                description='Stylish jacket for all seasons',
                price=89.99,
                stock=25,
                category_id=clothing.id,
                image_url='https://images.pexels.com/photos/1183266/pexels-photo-1183266.jpeg?auto=compress&cs=tinysrgb&w=400'
            )
        ]
        
        db.session.add_all(products)
        db.session.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.session.rollback()