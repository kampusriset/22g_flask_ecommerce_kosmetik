from flask import Flask
import os


def create_app():
    app = Flask(__name__,template_folder='template')
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['DEBUG']= True

    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
    app.config['UPLOAD_FOLDER'] = upload_folder

    from .controllers import controller
    from .admin import admin
    from .auth import auth
    from .form import form


    app.register_blueprint(controller,url_prefix='/')
    app.register_blueprint(form,url_prefix='/form')
    app.register_blueprint(admin,url_prefix='/admin')
    app.register_blueprint(auth,url_prefix='/auth')


    @app.get('/add_product')
    def add_product():
        return ""
    
    return app
