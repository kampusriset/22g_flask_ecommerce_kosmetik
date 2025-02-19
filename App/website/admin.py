from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from .models import Product
from werkzeug.utils import secure_filename
import os
from flask import current_app
from traceback import print_exception as print_exc



admin = Blueprint('admin',__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if a file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_admin():
    user = session.get('user')
    return user and user.get('role') == 'admin'

@admin.route('/add_product', methods = ['GET','POST'])
def add_product():

    if not is_admin():
        flash('Access denied. only Admin can access this site','danger')
        return redirect(url_for('auth.user_dashboard'))
    
    if request.method == 'POST':
        product_name = request.form['product_name']
        price = request.form['price']
        description = request.form['description']
        file = request.files['product_image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = current_app.config['UPLOAD_FOLDER']
            file.save(os.path.join(file_path, filename))

            try:
                Product.add_products(product_name,price,description,filename)
                flash("product added sucessfully",'success')
                return redirect(url_for('admin.add_product'))
            except Exception as e:
                flash(f"Error adding product: {e}",'danger')

        else:
            flash('Invalid file type. Please upload an image.', 'danger')
            return redirect(url_for('admin.add_product'))
        
    return render_template('add_product.html')      


@admin.route('/product_list')
def product_list():
    try:
        products = Product.get_product()
        return render_template('product_list.html',products = products)
    except Exception as e:
        flash(f"error you cant access product {e}",'danger')
        print_exc(e)
        return redirect(url_for('auth.user_dashboard'))
    
@admin.route('/delete/<int:product_id>',methods = ['POST'])
def product_delete(product_id):
    if not is_admin():
        return redirect(url_for('auth.login'))
    Product.delete_product(product_id)
    return redirect(url_for('admin.product_list'))

@admin.route('/update/<int:product_id>',methods=['GET','POST'])
def product_update(product_id):
    if not is_admin():
        flash('Access denied. only Admin can access this site','danger')
        return redirect(url_for('auth.user_dashboard'))

    # product = Product(product_id, "", 0, "", "")

    if request.method == 'POST':
        product_name = request.form['product_name']
        price = request.form['price']
        description = request.form['description']
        file = request.files['product_image']
        

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = current_app.config['UPLOAD_FOLDER']
            file.save(os.path.join(file_path, filename))

            try:
                product = Product(product_id,product_name,price,description,filename)
                Product.update_product(product_id,product)

                flash("product updated sucessfully",'success')
                return redirect(url_for('admin.product_list'))
            except Exception as e:
                flash(f"Error updating product: {e}",'danger')
                return redirect(url_for('admin.update/<int:product_id>'))
        else:
            flash('Invalid file type. Please upload an image.', 'danger')
            return redirect(url_for('admin.update/<int:product_id>'))
    if request.method == 'GET':
        product = Product.get_product_id(product_id)
        
    print(f"Product loaded for update: {product}")
    return render_template('update_product.html',product=product)     
