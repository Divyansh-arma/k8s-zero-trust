"""
Admin routes for managing products and orders
"""
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from app.admin import bp
from app.models import Product, Category, Order, User
from app.admin.forms import ProductForm, CategoryForm
from app import db

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         recent_orders=recent_orders)

@bp.route('/products')
@login_required
@admin_required
def manage_products():
    """Manage products"""
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/products.html', products=products)

@bp.route('/product/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    """Add new product"""
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data,
            image_url=form.image_url.data
        )
        db.session.add(product)
        db.session.commit()
        
        flash(f'Product {product.name} added successfully!', 'success')
        return redirect(url_for('admin.manage_products'))
    
    return render_template('admin/add_product.html', form=form)

@bp.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    """Edit existing product"""
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data
        product.image_url = form.image_url.data
        
        db.session.commit()
        flash(f'Product {product.name} updated successfully!', 'success')
        return redirect(url_for('admin.manage_products'))
    
    return render_template('admin/edit_product.html', form=form, product=product)

@bp.route('/orders')
@login_required
@admin_required
def manage_orders():
    """Manage orders"""
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/orders.html', orders=orders)

@bp.route('/order/<int:id>')
@login_required
@admin_required
def order_detail(id):
    """View order details"""
    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)

@bp.route('/categories')
@login_required
@admin_required
def manage_categories():
    """Manage categories"""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@bp.route('/category/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    """Add new category"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        
        flash(f'Category {category.name} added successfully!', 'success')
        return redirect(url_for('admin.manage_categories'))
    
    return render_template('admin/add_category.html', form=form)