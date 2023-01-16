import flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_cors import CORS
from sqlalchemy.orm import backref
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome("/Users/mattiabernardi/Documents/01_Workspace/05_IOT/02_server/chromedriver")

# Creating the application
app = flask.Flask(__name__)
CORS(app)

# DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///prodinfo.db"

# Database related Stuff
db = SQLAlchemy(app)

# Database tables
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(35), nullable=False)
    brand = db.Column(db.String(35), nullable=False)
    asin = db.Column(db.String(35), unique=True, nullable=False)
    amount_in_stock = db.Column(db.Integer, nullable=False)
    reference_weight = db.Column(db.Float, nullable=False)
    last_measure = db.Column(db.Float, nullable=False)
    recently_added = db.Column(db.Boolean, nullable=False, default=False)
    ordered = db.relationship('Order', backref='product', lazy=True)

    def __repr__(self):
        return f"ID: {self.id}, Name: {self.name}, Last: {self.last_measure}"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    total_cost = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

def shouldAdd(asin):
    row = Product.query.filter_by(asin=asin).first()
    if row.recently_added == True:
        return False
    return True

def addToCart(asin):
    if (not shouldAdd(asin)) :
        return False
    url = "https://www.amazon.it/s?k="+asin+"&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_2"
    driver.implicitly_wait(1)
    driver.get(url)
    driver.maximize_window()

    driver.find_element_by_xpath(
        '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]/div'
        ).click()
    
    # Check for time based purchase
    try:
        driver.find_element_by_id("newAccordionRow").click()
        print("Periodic Purchase Available, Switching to single purchase...")
    except NoSuchElementException:
        print("No Periodic Purchase Available...")
    
    driver.find_element_by_id("add-to-cart-button").click()

    # Update the product status
    row =db.session.query(Product).filter_by(asin=asin).first()
    row.recently_added = True
    db.session.commit()
    
# Defining routes
@app.route('/<api_key>/bridge/<code>/get-status', methods=['GET'])
def bridgeRetrieve(api_key, code):
    if flask.request.method == 'GET':
        if api_key == "getdt2":
            row =db.session.query(Product).filter_by(sensor_id=code).first()
            status = 1
            if (row.last_measure < 0 or row.last_measure < row.reference_weight ) and row.amount_in_stock < 2: status = 3
            if (row.last_measure < row.reference_weight) and row.amount_in_stock > 1: status = 2
            print("Value and Status", row.last_measure, status)
            resp = {'ID': code, 'status': status}

            if status == 3 and shouldAdd(row.asin):
                addToCart(row.asin)

            return flask.jsonify(resp), 200

    
@app.route('/<api_key>/bridge/update-measure', methods=['POST'])
def bridge(api_key):
    if flask.request.method == 'POST':
        if api_key == "pstdt1":
            sens_id = flask.request.form['ID']
            value = flask.request.form['value']
            print(sens_id, value)

            prod_to_update = Product.query.filter_by(sensor_id=sens_id).first()
            old = prod_to_update.last_measure
            prod_to_update.last_measure = value
            db.session.commit()

            resp = {'ID': sens_id, 'old': old, 'new': value}

            return flask.jsonify(resp), 200


@app.route('/<api_key>/app/get-data', methods=['GET'])
def getDataForApp(api_key):
    if flask.request.method == 'GET':
        if api_key == 'rfrsh1':
            prods = db.session.query(Product).all()
            list = []
            for p in prods:
                res = {}
                res['sens_id'] = p.sensor_id
                res['name'] = p.name
                res['brand'] = p.brand
                res['asin'] = p.asin
                res['stock'] = p.amount_in_stock
                res['weight'] = p.reference_weight
                res['value'] = p.last_measure
                
                list.append(res)

            json_result = flask.jsonify(list)
            #json_result.headers.add("Access-Control-Allow-Origin", "*")
            return json_result, 201

@app.route('/<api_key>/app/post-data', methods=['POST'])
def postDataFromApp(api_key):
    if flask.request.method == 'POST':
        if api_key == 'update':
            data = flask.request.json
            sens_id = data.get('sens_id')
            name = data.get('name')
            brand = data.get('brand')
            asin = data.get('asin')
            weight = data.get('weight')
            stock = data.get('stock')
            print(sens_id, name, brand, asin)
            prod_to_update = Product.query.filter_by(sensor_id=sens_id).first()
            prod_to_update.name = name
            prod_to_update.brand = brand
            prod_to_update.asin = asin
            prod_to_update.amount_in_stock = stock
            prod_to_update.reference_weight = weight

            db.session.commit()

            resp = {'name': name, 'brand': brand}

            return flask.jsonify(resp), 201

@app.route('/<api_key>/app/post-data/new-sens', methods=['POST'])
def postDataFromAppCreate(api_key):
    if flask.request.method == 'POST':
        if api_key == 'create':
            data = flask.request.json
            sens_id = data.get('sens_id')
            name = data.get('name')
            brand = data.get('brand')
            asin = data.get('asin')
            weight = data.get('weight')
            stock = data.get('stock')
            value = data.get('value')
            prod_to_create = Product()
            prod_to_create.sensor_id = sens_id
            prod_to_create.name = name
            prod_to_create.brand = brand
            prod_to_create.asin = asin
            prod_to_create.amount_in_stock = stock
            prod_to_create.reference_weight = weight
            prod_to_create.last_measure = value


            db.session.add(prod_to_create)
            db.session.commit()

            resp = {'name': name, 'brand': brand}

            return flask.jsonify(resp), 201

if __name__ == "__main__":
    port = 80
    interface = "0.0.0.0"
    app.run(host=interface, port=port)