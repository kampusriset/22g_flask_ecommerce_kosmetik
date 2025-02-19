from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from .models import Product,Cart

controller = Blueprint('controller',__name__)

@controller.route('/')
def homepage():
     try:
        products = Product.get_product()
        return render_template('home.html',products=products)
     except Exception as e:
        flash(f"error you cant access product {e}",'danger')
        return redirect(url_for('auth.user_dashboard'))

@controller.route('/product_shop',methods=['GET'])
def product_shop():
    try:
       products = Product.get_product()
       return render_template('product_shop.html',products = products)
    except Exception as e:
        flash(f"error you cant access product {e}",'danger')
        return redirect(url_for('auth.user_dashboard'))

@controller.route('add_to_cart/<int:product_id>',methods=['POST'])
def add_to_cart(product_id):
    if 'user' not in session:
        flash('You need to log in to add item in the cart','danger')
        return redirect(url_for('auth.login'))
    
    user_id = session['user']['user_id']
    quantity = int(request.form.get('quantity',1))

    try:
        Cart.add_to_cart(user_id,product_id,quantity)
        flash('product added to cart sucessfully','success')
        return redirect(url_for('controller.product_shop'))
    except Exception as e:
        flash(f'Error adding to cart {e}','danger')
        return redirect(url_for('controller.product_shop'))

@controller.route('/view_cart')
def view_cart():
    if 'user' not in session:
        flash('You need to log in to add item in the cart','danger')
        return redirect(url_for('auth.login'))
    user_id = session['user']['user_id']
    try :
        cart_items = Cart.get_cart_items(user_id)
        total_price = sum(item[5] for item in cart_items)
        return render_template('cart.html',cart_items=enumerate(cart_items),total_price=total_price)
    except Exception as e:
        flash(f'error retrieving cart : {e}','danger')
        return redirect(url_for('controller.product_shop'))

@controller.route('/delete_item/<int:product_id>',methods=['POST'])
def delete_item(product_id):
    if 'user' not in session:
        flash('You need to log in to add item in the cart','danger')
        return redirect(url_for('auth.login'))
    user_id = session['user']['user_id']
    try:
        Cart.remove_item(user_id,product_id)
        flash('Product sucessfully removed','success')
        return redirect(url_for('controller.view_cart'))
    except Exception as e:
        flash(f"error removing product from cart : {e}",'danger')
        return redirect(url_for('controller.product_shop'))

@controller.route('/clear_cart')
def clear_cart():
    if 'user' not in session:
        flash('You need to log in to add item in the cart','danger')
        return redirect(url_for('auth.login'))
    user_id = session['user']['user_id']
    try:
        Cart.clear_cart(user_id)
        flash('Cart cleared successfully.', 'success')
        return redirect(url_for('controller.view_cart'))
    except Exception as e:
        flash(f"Error clearing cart: {e}", 'danger')
        return redirect(url_for('controller.view_cart'))
    
@controller.route('/checkout')
def checkout():
    return render_template('cart.html')

@controller.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('query', '')  # Ambil keyword dari URL parameter
    
    if not keyword:
        flash("Please enter a search term.", "warning")
        return redirect(url_for('controller.product_shop'))

    try:
        results = Product.search_product(keyword)
        return render_template('search_results.html', products=results, keyword=keyword)
    except Exception as e:
        flash(f"Error searching for products: {e}", "danger")
        return redirect(url_for('controller.product_shop'))
