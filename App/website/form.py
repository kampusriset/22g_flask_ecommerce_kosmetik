from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from .models import Product,Cart,Order

form = Blueprint('form',__name__)


@form.route('/about')
def about():
    return render_template('about.html')

@form.route('/checkout', methods=['GET','POST'])
def checkout():
    if 'user' not in session:
        flash('You need to log in to add item in the cart','danger')
        return redirect(url_for('auth.login'))
    
    user_id = session['user']['user_id']

    if request.method == 'POST':

        address = request.form['address']
        total_price = request.form['total_price']

        try:
            Order.create_order(user_id,address,total_price)

            Cart.clear_cart(user_id)

            flash('Order placed successfully!', 'success')
            return redirect(url_for('form.order_confirmation'))
        except Exception as e:
            flash(f'Error placing order: {e}', 'danger')
            return redirect(url_for('form.checkout'))
    
    cart_items = Cart.get_cart_items(user_id)
    total_price = sum(item[5] for item in cart_items)

    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)


@form.route('/order_confirmation', methods=['GET'])
def order_confirmation():
    return render_template('order_confirmation.html')

@form.route('/order_details/<int:order_id>')
def order_details(order_id):
    if 'user' not in session:
        flash('You need to log in to add item in the cart','danger')
        return redirect(url_for('auth.login'))
    
    user_id = session['user']['user_id']
    
    try:
        order_info = Order.get_order_by_id(user_id,order_id)
        order_items = Order.get_order_item(order_id)

        if not order_info:
            flash('Order not found','danger')
            return redirect(url_for('controller.product_shop'))
        
        return render_template('order_details.html',order_info=order_info,order_items=order_items)
    except Exception as e:
        flash(f'Error retrieving order details: {e}', 'danger')
        return redirect(url_for('controller.product_shop'))


@form.route('/user_orders')
def user_orders():
    if 'user' not in session:
        flash('You need to log in to view your orders', 'danger')
        return redirect(url_for('auth.login'))
    
    user_id = session['user']['user_id']
    
    try:
        orders = Order.get_orders_by_user(user_id)  # Fetch user orders
        return render_template('user_orders.html', orders=orders)
    except Exception as e:
        flash(f'Error retrieving orders: {e}', 'danger')
        return redirect(url_for('controller.homepage'))
