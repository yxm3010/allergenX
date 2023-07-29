from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os.path

# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///allergenx.db"
# https://docs.sqlalchemy.org/en/20/core/engines.html
# initialize the app with the extension
db.init_app(app)

def get_score(check, opt):
        if(check):
            if(opt == "No"):
                return 0 # You cannot avoid allergen
            else:
                return 50 # Restrant has option to avoid allergen
        else:
            return 100 # Allergen not used in the ingredients 

class Allergen(db.Model):
    __tablename__ = 'allergenx'
    customerID = db.Column('customerID', db.Integer)
    item = db.Column('item', db.String(50), primary_key=True)
    timestamp = db.Column('timestamp', db.DateTime)
    hasEggs = db.Column('hasEggs', db.String(10))
    eggOptions = db.Column('eggOptions', db.String(10))
    eggScore = db.Column('eggScore', db.Integer)
    hasNuts = db.Column('hasNuts', db.String(10))
    nutsOptions = db.Column('nutsOptions', db.String(10))
    nutsScore = db.Column('nutsScore', db.Integer)
    hasMilk = db.Column('hasMilk', db.String(10))
    milkOptions = db.Column('milkOptions', db.String(10))
    milkScore = db.Column('milkScore', db.Integer)
    

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/test2")
def test():
    if not os.path.exists('allergenx.db'):
        with app.app_context(): # I think this allows db to access app config data like SQLALCHEMY_DATABASE_URI
            db.create_all()
    return render_template('test2.html')

@app.route("/load_current_db", methods=['POST', 'GET'])
def load_current_db():
    results = Allergen.query.filter_by(customerID='0').order_by(Allergen.item).all()
    response = []
    for result in results:
        response.append(
            {'item': result.item,
             'eggScore': result.eggScore,
             'nutsScore': result.nutsScore,
             'milkScore': result.nutsScore}
        )
    
    print(response)
    return jsonify(response)

@app.route("/proc_allergen_db", methods=['POST', 'GET'])
def process():
    if request.method == "POST":
        allergen_data = request.get_json()
        print(allergen_data)
        db_row =  Allergen(
            customerID = allergen_data[0]['customerID'],
            item = allergen_data[1]['item'], 
            timestamp = datetime.now(),
            hasEggs = allergen_data[2]['hasEgg'],
            eggOptions = allergen_data[3]['eggOptions'], 
            eggScore = get_score(allergen_data[2]['hasEgg'], allergen_data[3]['eggOptions']),
            hasNuts = allergen_data[4]['hasNuts'],
            nutsOptions = allergen_data[5]['nutsOptions'], 
            nutsScore = get_score(allergen_data[4]['hasNuts'], allergen_data[5]['nutsOptions']),
            hasMilk = allergen_data[6]['hasMilk'],
            milkOptions = allergen_data[7]['milkOptions'], 
            milkScore = get_score(allergen_data[6]['hasMilk'], allergen_data[7]['milkOptions'])
            )
        db.session.add(db_row)
        db.session.commit()

        # Read back
        query = "SELECT * from allergenx WHERE item='%s'"% allergen_data[1]['item']
        results= db.session.execute(query).first()

        result = {'item': results[1],
                  'eggScore': results[5],
                  'nutsScore': results[8],
                  'milkScore': results[11]
                  }
        """ 'item': db.session.execute(db.select(Allergen.item).where(Allergen.customerID == allergen_data[0]['customerID'].where(Allergen.item == allergen_data[0]['customerID']))) """
        return jsonify(result)
    
@app.route("/del_allergen_db", methods=['POST', 'GET'])
def delete():
    if request.method == "POST":
        serverData = request.get_json()
        items = serverData[1]['items']
        print(serverData)
        for itemName in items:
            Allergen.query.filter_by(customerID=serverData[0]['customerID'], item=itemName).delete()
            db.session.commit()
    return True

if __name__ == "__main__":
    app.run(debug=True)

# References:
# https://stackoverflow.com/questions/38664088/flask-404-for-post-request