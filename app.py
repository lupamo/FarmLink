#!/usr/bin/python3
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, joinedload
from models.customers import Customers
from models.farmers import Farmers
from models.products import Product
import mysql.connector
import urllib.parse

app = Flask(__name__, template_folder='static/templates')
app.secret_key = 'supersecretkey'

password = "kayla@2020"
encoded_password = urllib.parse.quote_plus(password)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://farmlink_user:{encoded_password}@localhost:3306/fm_ln_0"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = '/uploads' 
db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = scoped_session(sessionmaker(bind=engine))

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='farmlink_user',
        password='kayla@2020',
        database='fm_ln_0'
    )
    return connection

@app.route('/')
def home():
    """route to home page"""
    return render_template('home.html')

@app.route('/sign_in')
def sign_in():
    """function to render sign-up page"""
    return render_template('sign_in.html')

@app.route('/sign_up_or_login', methods=['POST'])
def sign_up_or_login():
    user_type = request.form['user_type']
    name = request.form['name']
    contact = request.form['contact']
    address = request.form.get('address')  # Address is required for sign-up

    user = None

    if user_type == 'customer':
        user = db.session.query(Customers).filter_by(name=name, contact=contact).first()
        if not user:
            # Sign up new customer
            new_customer = Customers(name=name, contact=contact, address=address)
            db.session.add(new_customer)
            db.session.commit()
            return redirect(url_for('login'))

    elif user_type == 'farmer':
        user = db.session.query(Farmers).filter_by(name=name, contact=contact).first()
        if not user:
            """Sign up new farmer"""
            new_farmer = Farmers(name=name, contact=contact, address=address)
            db.session.add(new_farmer)
            db.session.commit()
            return redirect(url_for('login'))

    if user:
        """Successful login"""
        session['user_id'] = user.id
        session['user_type'] = user_type
        return redirect(url_for('dashboard', user_type=user_type))
    else:
        # Login failed
        return "Invalid login credentials"

@app.route('/products', methods=['GET'])
def get_products():
    from models.products import Product
    session = Session()
    products = session.query(Product).options(joinedload(Product.farmer)).all()

    result = []
    for product in products:
        product_info = {
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity,
            'farmer': product.farmer.name if product.farmer else '', # Access farmer's name directly from the loaded object
            'contact': product.farmer.contact if product.farmer else '' # Access farmer's contact directly from the loaded object
        }
        result.append(product_info)
    return render_template("products.html", products=result)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form['user_type']
        name = request.form['name']
        contact = request.form['contact']

        user = None  # Initialize user variable

        if user_type == 'customer':
            user = db.session.query(Customers).filter_by(name=name, contact=contact).first()
        elif user_type == 'farmer':
            user = db.session.query(Farmers).filter_by(name=name, contact=contact).first()

        if user:
            """Successful login"""
            session['user_id'] = user.id
            session['user_type'] = user_type
            return redirect(url_for('dashboard', user_type=user_type))
        else:
            # Login failed
            return "Invalid login credentials"
    return render_template('login.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session or session.get('user_type') != 'farmer':
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        Description = request.form['Description']
        price = int(request.form['price'])
        quantity = int(request.form['quantity'])
        farmer_id = session['user_id']  # Using session to get farmer_id

        image_file = request.files.get('image')
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Saving image to: {image_path}")
            image_file.save(image_path)
        else:
            image_path = None

        new_product = Product(name=name, Description=Description, price=price,
                              quantity=quantity, farmer_id=farmer_id, image=image_path)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('dashboard', user_type='farmer'))
        except Exception as e:
            db.session.rollback()
            return render_template('error.html', error=str(e))

    current_user = db.session.query(Farmers).get(session['user_id'])
    return render_template('add_product.html', current_user=current_user)


@app.route('/dashboard')
def dashboard():
    user_type = request.args.get('user_type')
    if user_type == 'customer':
        products = db.session.query(Product).all()
        product_list = []
        for product in products:
            product_info = {
                'name': product.name,
                'price': product.price,
                'farmer': {
                    'name': product.farmer.name,
                    'contact': product.farmer.contact,
                    'address': product.farmer.address
                }
            }
            product_list.append(product_info)
        return render_template('products.html', products=products)
    elif user_type == 'farmer':
        return redirect(url_for('add_product'))

    return 'Welcome'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
