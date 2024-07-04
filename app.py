#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import mysql.connector
import urllib.parse

app = Flask(__name__, template_folder='static/templates')

password = "kayla@2020"
encoded_password = urllib.parse.quote_plus(password)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://farmlink_user:{encoded_password}@localhost:3306/fm_ln_0"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    return render_template('home.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/products', methods=['GET'])
def get_products():
    from models.products import Product
    products = Session.query(Product).all()
    result = []
    for product in products:
        product_info = {
            'name': product.name,
            'price': product.price,
            'farmer': product.farmer_id
        }
        result.append(product_info)
    return render_template("products.html", products=result)

@app.route('/login', methods=['GET', 'POST'])
def login():
    from models.farmers import Farmers
    from models.customers import Customers
    if request.method == 'POST':
        contact = request.form['contact']
        name = request.form['name']
        user_type = request.form['user_type']

        if user_type == 'customer':
            user = Customers.query.filter_by(contact=contact, name=name).first()
        elif user_type == 'farmer':
            user = Farmers.query.filter_by(contact=contact, name=name).first()

        if user:
            return redirect(url_for('dashboard', user_type=user_type))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user_type = request.args.get('user_type')
    if user_type == 'customer':
        return 'Welcome Customer'
    elif user_type == 'farmer':
        return 'Welcome Farmer'
    return 'Welcome'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
