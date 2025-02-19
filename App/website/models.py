import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, redirect, render_template, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'


class Database:
    def __init__(self):
        self.connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            database='e_shop',
            port=3307
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()


class User:
    def __init__(self, username, password, role='user', email=None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.email = email

    @staticmethod
    def create_user(username, password, role='user', email=None):
        db = Database()
        password_hash = generate_password_hash(password)
        db.cursor.execute(
            "INSERT INTO users (username, password_hash, role, email) VALUES (%s, %s, %s, %s)",
            (username, password_hash, role, email)
        )
        db.connection.commit()
        db.close()

    @staticmethod
    def get_user_by_username(username):
        db = Database()
        db.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = db.cursor.fetchone()
        db.close()
        return user

    @staticmethod
    def verify_password(username, password):
        db = Database()
        db.cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = db.cursor.fetchone()
        db.close()
        if result:
            return check_password_hash(result[0], password)
        return False
    
    @staticmethod
    def get_user_by_id(id):
        db = Database()
        try:
            db.cursor.execute("SELECT id, password_hash FROM users where id=%s",(id,))
            return db.cursor.fetchone()
        finally:
            db.close()

    @staticmethod
    def update_password(id,new_password):
        db = Database()
        password_hash = generate_password_hash(new_password)
        try:
            db.cursor.execute("UPDATE users SET password_hash=%s WHERE id=%s",(password_hash,id))
            db.connection.commit()
        finally:
            db.close()


class Product:
    def __init__(self,id,product_name,price,description,image):
        self.id = id
        self.product_name = product_name
        self.price = price
        self.description = description
        self.image = image
    
    @staticmethod
    def add_products(product_name,price,description,image):
        db = Database()
        db.cursor.execute(
            "INSERT INTO product (product_name,price,description,image) VALUES (%s,%s,%s,%s)",
            (product_name,price,description,image))
        db.connection.commit()
        db.close()

    @staticmethod
    def get_product():
        db = Database()
        db.cursor.execute("SELECT * FROM product")
        product = db.cursor.fetchall()
        db.close()
        return product
    
    @staticmethod
    def get_product_id(product_id):
        db = Database()
        db.cursor.execute("SELECT id, product_name, price, description, image FROM product WHERE id=%s", (product_id,))
        row = db.cursor.fetchone()
        db.close()
        
        if row:
            # Return a Product object, not a tuple
            return Product(
                id=row[0],
                product_name=row[1],
                price=row[2],
                description=row[3],
                image=row[4]
            )
        return None


    @staticmethod
    def delete_product(product_id):
        db = Database()
        db.cursor.execute("DELETE fROM product WHERE id=%s",(product_id,))
        db.connection.commit()
        db.close()

    @staticmethod
    def update_product(product_id,product):
        db = Database()
        db.cursor.execute("UPDATE product SET product_name=%s,price=%s,description=%s,image=%s WHERE id=%s",(product.product_name,product.price,product.description,product.image,product_id))
        db.connection.commit()
        db.close()

    @staticmethod
    def search_product(keyword):
        db = Database()
        try:
            search_query = f"{keyword}"
            db.cursor.execute("SELECT id,product_name,price,description,image FROM product WHERE product_name LIKE %s",(search_query,))
            return db.cursor.fetchall()
        finally:
            db.close()

class Cart:
    @staticmethod
    def add_to_cart(user_id,product_id,quantity):
        db = Database()
        db.cursor.execute("SELECT id FROM cart WHERE user_id=%s AND product_id=%s",(user_id,product_id))
        cart_item = db.cursor.fetchone()

        if cart_item:

            db.cursor.execute("UPDATE cart SET quantity = quantity + %s WHERE id=%s",(quantity,cart_item[0]))
        else:
            db.cursor.execute("INSERT INTO cart(user_id,product_id,quantity) VALUES  (%s, %s, %s)",(user_id,product_id,quantity))
        db.connection.commit()
        db.close()
    
    @staticmethod
    def get_cart_items(user_id):
        db = Database()
        db.cursor.execute(""" SELECT p.id, p.product_name, p.price, c.quantity, p.image, (p.price * c.quantity) AS total
            FROM cart c
            JOIN product p ON c.product_id = p.id
            WHERE c.user_id = %s
        """,(user_id,))
        cart_item = db.cursor.fetchall()
        db.close()
        return cart_item
    
    @staticmethod
    def remove_item(user_id,product_id):
        db=Database()
        db.cursor.execute("DELETE FROM cart WHERE user_id = %s AND product_id= %s",(user_id,product_id))
        db.connection.commit()
        db.close()
    
    @staticmethod
    def clear_cart(user_id):
        db=Database()
        db.cursor.execute("DELETE FROM cart WHERE user_id = %s",(user_id,))
        db.connection.commit()
        db.close()

class Order:
    @staticmethod
    def create_order(user_id,address,total_price):
        db = Database()
        db.cursor.execute(""" INSERT INTO orders (user_id,address,total_price,created_at) VALUES (%s,%s,%s,NOW()) """,(user_id,address,total_price))
        db.connection.commit()
        db.close()

    @staticmethod
    def get_order_by_id(user_id,order_id):
        db=Database()
        try:
            db.cursor.execute("SELECT order_id, total_price, created_at, address FROM orders WHERE user_id = %s AND order_id = %s", (user_id, order_id))
            return db.cursor.fetchone()
        finally:
            db.close()

    @staticmethod
    def get_order_item(order_id):
        db = Database()
        try:
            db.cursor.execute(""" 
                SELECT p.id, p.name, p.price, p.image, oi.quantity, (p.price * oi.quantity) AS total
                FROM order_items oi 
                JOIN product p ON oi.product_id = p.id
                WHERE oi.order_id = %s 
            """, (order_id,))
            return db.cursor.fetchall()
        finally:
            db.close()

    @staticmethod
    def get_orders_by_user(user_id):
        db = Database()
        try:
            cursor = db.cursor
            cursor.execute("SELECT order_id, total_price, created_at FROM orders WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
            orders = cursor.fetchall()  # Get all orders
            return orders
        except Exception as e:
            db.connection.rollback()
            raise e
        finally:
            db.close()