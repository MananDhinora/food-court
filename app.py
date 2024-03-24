import base64
import random
import re
import uuid

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace with your database connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:asdf@localhost/foodcourt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended for performance

mydb = SQLAlchemy(app)

# app = Flask(__name__)

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="asdf",
#   database="foodcourt"
# )

g_user_id = None



def generate_user_id():
    """Generates unique user id"""
    return f"UID-{uuid.uuid4()}"


def encode_password(password):
    """takes input password and encodes it in b64"""
    password_bytes = password.encode("ascii")
    base64_bytes = base64.b64encode(password_bytes)
    return str(base64_bytes.decode("ascii"))


def validate_email(email):
    """validates email using regex"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not (re.match(regex, email)):
        return {
            "error": "email is invalid",
            "success": "false"
        }, 400
    return True


@app.route('/')
def home_user():
    return render_template("signup.html")

@app.route('/login')
def home_login():
    return render_template("login.html")

@app.route('/userSignup', methods=['POST'])
def add_user_register():
    user_request_data = request.get_json()
    user_type = user_request_data['userType'] # ui give two options
    name = user_request_data['name']
    email = user_request_data['email']
    password = user_request_data['password']
    if user_type == '' or name == '' or email == '' or password == '':
        return {
            "error": "missing required fields",
            'success': 'false'
        }, 400

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not (re.match(regex, email)):
        return {
            "error": "email is invalid",
            "success": "false"
        }, 400

    encoded_password = encode_password(password)
    user_id = generate_user_id()

    try:
        with mydb.cursor() as cursor:
            sql = "INSERT INTO userdetails (user_id, user_type, name, email, password) VALUES (%s, %s, %s, %s, %s)"
            val = (user_id, user_type, name, email, encoded_password)
            cursor.execute(sql, val)
            mydb.commit()
            data = {
                "data": {
                    "userId": user_id,
                    "userType": user_type,
                    "name": name,
                    "email": email
                }
            }
            return data

    except Exception as e:
        return {
            "error": "Registration error, try again!",
            "success": "false",
            "exception": str(e)
        }, 400

g_user_id = None
@app.route('/userLogin', methods=['POST'])
def user_login():
    user_request_data = request.get_json()
    email = user_request_data['email']
    password = user_request_data['password']
    if email == '' or password == '':
        return {
            "error": "missing required fields",
            'success': 'false'
        }, 400

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not (re.match(regex, email)):
        return {
            "error": "email is invalid",
            "success": "false"
        }, 400

    encoded_password = encode_password(password)
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT user_id, email, password FROM `userdetails` WHERE `email` = %s"
            cursor.execute(sql, [email])
            result = cursor.fetchone()
            print("sql_execute:")
            if str(result[1]) == email and str(result[2]) == str(encoded_password):
                g_user_id = result[0]
                return {
                    "data": {
                        "userId": result[0],
                        "Login": "user logged in"
                    },
                    "success": "true"
                }, 200
            else:
                return {
                    "error": "Incorrect email or password",
                    "success": "false"
                }, 401

    except Exception as e:
        return {
            "error": "an error occurred while login",
            "success": "false",
            "exception": str(e)
        }, 400


@app.route('/getCanteen', methods=['GET'])
def get_canteens():
    # /getCanteenMenu?userId="UID-76"
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT * FROM foodcourt.canteen"
            cursor.execute(sql)
            result = cursor.fetchall()
            print("sql_execute:", result)
            canteens = []
            for i in result:
                uniq_dict = {"name": i[1], "cuisine": i[2], "rating": i[3]}
                canteens.append(uniq_dict)
            app.logger.info(canteens)
            return render_template("index.html", restaurants=canteens)
    except Exception as e:
        return {
            "error": "an error occurred while retrieving canteen details from DB",
            "success": "false",
            "exception": str(e)
        }, 400


@app.route('/getCanteenMenu', methods=['GET'])
def get_canteen_menu():
    # /getCanteenMenu?canteenName="Tea Post"
    canteen_name = str(request.args.get('canteenName'))
    try:
        with mydb.cursor() as cursor:
            sql = "SELECT * FROM foodmenu WHERE canteen_name = %s"
            cursor.execute(sql, [canteen_name])
            result = cursor.fetchall()
            dishes = []
            for i in result:
                uniq_dict = {"name": i[3], "rating": i[5], "quantity": 0, "price": i[4]}
                dishes.append(uniq_dict)
            return render_template("menu.html", dishes=dishes)
    except Exception as e:
        return {
            "error": "an error occurred while retrieving canteen menu details from DB",
            "success": "false",
            "exception": str(e)
        }, 400


@app.route('/addFoodCart', methods=['POST'])
def update_food_in_cart():
    # /addFoodCart?canteenName=Tea Post
    # input dict as below
    # {
    #     "userId": "UID-76",
    #     "cartItems": {
    #         "0": {
    #             "DishName": "Cold Coffee",
    #             "Price": "90",
    #             "Quantity": "2"
    #         },
    #         "1": {
    #             "DishName": "Ginger Tea",
    #             "Price": "60",
    #             "Quantity": "3"
    #         }
    #
    #     }
    #
    # }
    canteen_name = str(request.args.get('canteenName'))
    order_id = f"OID-{random.randint(1, 1000)}"
    user_request_data = request.get_json()
    if user_request_data == '':
        return {
            "error": "invalid request data",
            "success": "false"
        }, 400
    user_id = user_request_data['userId']
    try:
        with mydb.cursor() as cursor:
            for item in user_request_data['cartItems']:
                for num in item:
                    food_inp = user_request_data['cartItems'][num]
                    dish_name = food_inp['DishName']
                    price = food_inp['Price']
                    quantity = food_inp['Quantity']
                    sql = "INSERT INTO cart (order_id, user_id, canteen_name, dish_name, quantity, price_per_item) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (order_id, user_id, canteen_name, dish_name, quantity, price)
                    cursor.execute(sql, val)
                    mydb.commit()
            return {
                "data": {
                    "orderId": order_id,
                },
                "success": "true"
            }, 200
    except Exception as e:
        return {
            "error": "an error occurred while updating selected food items",
            "success": "false",
            "exception": str(e)
        }, 400

@app.route('/getCart', methods=['GET'])
def get_cart_items():
    # /getCart?orderId=OID-266
    order_id = str(request.args.get('orderId'))
    try:
        with mydb.cursor() as cursor:
            sql = f"SELECT * FROM cart WHERE order_id = %s"
            cursor.execute(sql, [order_id])
            result = cursor.fetchall()
            return {
                "data": {
                    "cartDetails": result
                },
                "success": "true"
            }, 200
    except Exception as e:
        return {
            "error": "an error occurred while retrieving cart item details from DB",
            "success": "false",
            "exception": str(e)
        }, 400


@app.route('/addMobile', methods=['GET'])
def add_user_mobile_details():
    # /getCart?userId=UID-76&mobileNumber=9909016074
    mobile_number = str(request.args.get('mobileNumber'))
    user_id = str(request.args.get('userId'))
    if mobile_number == '' or user_id == "":
        return {
            "error": "invalid input",
            "success": "false"
        }, 400
    if not re.match('[6-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', mobile_number):
        return {
            "error": "invalid mobile number",
            "success": "false"
        }, 400
    try:
        with mydb.cursor() as cursor:
            sql = "UPDATE userdetails set mobile_number = %s WHERE user_id = %s"
            val = (mobile_number, user_id)
            cursor.execute(sql, val)
            mydb.commit()
            return {
                "success": "true"
            }, 200
    except Exception as e:
        return {
            "error": "an error occurred while adding mobile number to DB",
            "success": "false",
            "exception": str(e)
        }, 400

@app.route('/menu')
def get_menu():
    with mydb.cursor() as cursor:
        # Get food items and their details from the database
        cursor.execute("SELECT * FROM foodmenu")
        food_items = cursor.fetchall()
    return render_template('menu.html', food_items=food_items)
