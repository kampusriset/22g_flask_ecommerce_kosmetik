from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth',__name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form.get('role', 'user')  # Default role is 'user'
        
        if User.get_user_by_username(username):
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('auth.register'))

        try:
            User.create_user(username, password, role, email)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration failed: {e}', 'danger')

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.get_user_by_username(username)
        if user and User.verify_password(username, password):
            session['user'] = {'user_id': user[0],'username': username, 'role': user[4]}  # Assume role is at index 4
            flash(f'Welcome, {username}!', 'success')
            if user[4] == 'admin':  # Role column is at index 4
                return redirect(url_for('auth.admin_dashboard'))
            return redirect(url_for('auth.user_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@auth.route('/admin-dashboard')
def admin_dashboard():
    if 'user' in session and session['user']['role'] == 'admin':
        return render_template('dashboard.html')
    flash('Access denied. Admins only.', 'danger')
    return redirect(url_for('auth.login'))


@auth.route('/user_dashboard')
def user_dashboard():
    if 'user' in session and session['user']['role'] == 'user':
        return render_template('home.html')
    flash('Access denied.', 'danger')
    return redirect(url_for('auth.login'))
    

@auth.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/update_password',methods=['GET','POST'])
def update_password():
    if 'user' not in session:
        flash('You need to log in first before updating your password','danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        user_id = session['user']['user_id']
        user = User.get_user_by_id(user_id)

        if user is None:
            flash("User not found.", "danger")
        elif not check_password_hash(user[1], current_password):  # Akses password dengan indeks 1
            flash("Current password is incorrect.", "danger")
        elif new_password != confirm_password:
            flash("New passwords do not match.", "danger")
        else:
            User.update_password(user_id, new_password)
            flash("Password updated successfully!", "success")
            return redirect(url_for('auth.user_dashboard'))
    return render_template('update_password.html')


    

       


   

    return render_template('update_password.html')
    

    


