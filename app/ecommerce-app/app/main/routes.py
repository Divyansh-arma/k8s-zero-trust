"""
Main application routes
"""
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp
from app.models import Product, Category, CartItem, Order, OrderItem
from app import db

@bp.route('/')
def index():
    """Homepage with featured products"""
    featured_products = Product.query.filter_by(is_active=True).limit(8).all()
    categories = Category.query.all()
    return render_template('main/index.html', products=featured_products, categories=categories)

@bp.route('/products')
def products():
    """Product catalog page with filtering and search"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(Product.name.contains(search) | 
                           Product.description.contains(search))
    
    products = query.paginate(
        page=page, per_page=12, error_out=False
    )
    
    categories = Category.query.all()
    
    return render_template('main/products.html', 
                         products=products, 
                         categories=categories,
                         current_category=category_id,
                         search_query=search)

@bp.route('/product/<int:id>')
def product_detail(id):
    """Individual product detail page"""
    product = Product.query.get_or_404(id)
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    
    return render_template('main/product_detail.html', 
                         product=product, 
                         related_products=related_products)

@bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')

@bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('main/contact.html')

@bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('main/profile.html', orders=orders)