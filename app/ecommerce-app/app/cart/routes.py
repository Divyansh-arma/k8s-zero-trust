"""
Shopping cart routes
"""
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.cart import bp
from app.models import Product, CartItem, Order, OrderItem
from app import db

@bp.route('/')
@login_required
def view_cart():
    """Display shopping cart"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.total_price for item in cart_items)
    return render_template('cart/cart.html', cart_items=cart_items, total=total)

@bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add product to cart"""
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > product.stock:
        flash(f'Sorry, only {product.stock} items available in stock.', 'error')
        return redirect(url_for('main.product_detail', id=product_id))
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id, 
        product_id=product_id
    ).first()
    
    if cart_item:
        if cart_item.quantity + quantity <= product.stock:
            cart_item.quantity += quantity
            flash(f'Updated {product.name} quantity in cart.', 'success')
        else:
            flash(f'Cannot add more items. Stock limit: {product.stock}', 'error')
            return redirect(url_for('main.product_detail', id=product_id))
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
        flash(f'Added {product.name} to cart.', 'success')
    
    db.session.commit()
    return redirect(url_for('main.product_detail', id=product_id))

@bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    """Update cart item quantity"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('cart.view_cart'))
    
    new_quantity = int(request.form.get('quantity', 0))
    
    if new_quantity <= 0:
        db.session.delete(cart_item)
        flash('Item removed from cart.', 'info')
    elif new_quantity <= cart_item.product.stock:
        cart_item.quantity = new_quantity
        flash('Cart updated.', 'success')
    else:
        flash(f'Only {cart_item.product.stock} items available.', 'error')
    
    db.session.commit()
    return redirect(url_for('cart.view_cart'))

@bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('cart.view_cart'))
    
    product_name = cart_item.product.name
    db.session.delete(cart_item)
    db.session.commit()
    
    flash(f'Removed {product_name} from cart.', 'info')
    return redirect(url_for('cart.view_cart'))

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout process"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('main.products'))
    
    if request.method == 'POST':
        shipping_address = request.form.get('shipping_address')
        
        if not shipping_address:
            flash('Please provide a shipping address.', 'error')
            return render_template('cart/checkout.html', cart_items=cart_items)
        
        # Calculate total
        total = sum(item.total_price for item in cart_items)
        
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=shipping_address
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items and update stock
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                flash(f'Insufficient stock for {cart_item.product.name}.', 'error')
                db.session.rollback()
                return render_template('cart/checkout.html', cart_items=cart_items)
            
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price
            )
            db.session.add(order_item)
            
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
        
        # Clear cart
        for cart_item in cart_items:
            db.session.delete(cart_item)
        
        db.session.commit()
        
        flash(f'Order #{order.id} placed successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    total = sum(item.total_price for item in cart_items)
    return render_template('cart/checkout.html', cart_items=cart_items, total=total)