from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os.path
import requests

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
            if not opt:
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
    hasWheat = db.Column('hasWheat', db.String(10))
    wheatOptions = db.Column('wheatOptions', db.String(10))
    wheatScore = db.Column('wheatScore', db.Integer)
    hasFish = db.Column('hasFish', db.String(10))
    fishOptions = db.Column('fishOptions', db.String(10))
    fishScore = db.Column('fishScore', db.Integer)
    hasShellfish = db.Column('hasShellfish', db.String(10))
    shellfishOptions = db.Column('shellfishOptions', db.String(10))
    shellfishScore = db.Column('shellfishScore', db.Integer)
    hasSesami = db.Column('hasSesami', db.String(10))
    sesamiOptions = db.Column('sesamiOptions', db.String(10))
    sesamiScore = db.Column('sesamiScore', db.Integer)
    hasPeanuts = db.Column('hasPeanuts', db.String(10))
    peanutsOptions = db.Column('peanutsOptions', db.String(10))
    peanutsScore = db.Column('peanutsScore', db.Integer)
    hasSoy = db.Column('hasSoy', db.String(10))
    soyOptions = db.Column('soyOptions', db.String(10))
    soyScore = db.Column('soyScore', db.Integer)

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
             'milkScore': result.milkScore,
             'wheatScore': result.wheatScore,
             'fishScore': result.fishScore,
             'shellfishScore': result.shellfishScore,
             'sesamiScore': result.sesamiScore,
             'peanutsScore': result.peanutsScore,
             'soyScore': result.soyScore,}
        )
    
    print(response)
    return jsonify(response)

# @app.route("/proc_allergen_db", methods=['POST', 'GET'])
# def process():
#     if request.method == "POST":
#         allergen_data = request.get_json()
#         print(allergen_data)
#         db_row =  Allergen(
#             customerID = allergen_data[0]['customerID'],
#             item = allergen_data[1]['item'], 
#             timestamp = datetime.now(),
#             hasEggs = allergen_data[2]['hasEgg'],
#             eggOptions = allergen_data[3]['eggOptions'], 
#             eggScore = get_score(allergen_data[2]['hasEgg'], allergen_data[3]['eggOptions']),
#             hasNuts = allergen_data[4]['hasNuts'],
#             nutsOptions = allergen_data[5]['nutsOptions'], 
#             nutsScore = get_score(allergen_data[4]['hasNuts'], allergen_data[5]['nutsOptions']),
#             hasMilk = allergen_data[6]['hasMilk'],
#             milkOptions = allergen_data[7]['milkOptions'], 
#             milkScore = get_score(allergen_data[6]['hasMilk'], allergen_data[7]['milkOptions'])
#             )
#         db.session.add(db_row)
#         db.session.commit()

#         # Read back
#         query = "SELECT * from allergenx WHERE item='%s'"% allergen_data[1]['item']
#         results= db.session.execute(query).first()

#         result = {'item': results[1],
#                   'eggScore': results[5],
#                   'nutsScore': results[8],
#                   'milkScore': results[11]
#                   }
#         """ 'item': db.session.execute(db.select(Allergen.item).where(Allergen.customerID == allergen_data[0]['customerID'].where(Allergen.item == allergen_data[0]['customerID']))) """
#         return jsonify(result)

@app.route("/add_new_row", methods=['POST', 'GET'])
def add_new_row():
    if request.method == "POST":

        _hasEggs = True if (request.form.get('eggCheck')) else False
        _eggOptions = True if (request.form.get('eggOptions') == "Yes") else False

        _hasNuts = True if (request.form.get('nutsCheck')) else False
        _nutsOptions = True if (request.form.get('nutsOptions') == "Yes") else False

        _hasMilk = True if (request.form.get('milkCheck')) else False
        _milkOptions = True if (request.form.get('milkOptions') == "Yes") else False

        _hasWheat = True if (request.form.get('wheatCheck')) else False
        _wheatOptions = True if (request.form.get('wheatOptions') == "Yes") else False

        _hasFish = True if (request.form.get('fishCheck')) else False
        _fishOptions = True if (request.form.get('fishOptions') == "Yes") else False

        _hasShellfish = True if (request.form.get('shellfishCheck')) else False
        _shellfishOptions = True if (request.form.get('shellfishOptions') == "Yes") else False

        _hasSesami = True if (request.form.get('sesamiCheck')) else False
        _sesamiOptions = True if (request.form.get('sesamiOptions') == "Yes") else False

        _hasPeanuts = True if (request.form.get('peanutsCheck')) else False
        _peanutsOptions = True if (request.form.get('peanutsOptions') == "Yes") else False

        _hasSoy = True if (request.form.get('soyCheck')) else False
        _soyOptions = True if (request.form.get('soyOptions') == "Yes") else False
        
        db_row =  Allergen(
                customerID = 0,
                item = request.form['itemname'], 
                timestamp = datetime.now(),
                hasEggs = _hasEggs,
                eggOptions = _eggOptions, 
                eggScore = get_score(_hasEggs, _eggOptions),
                hasNuts = _hasNuts,
                nutsOptions = _nutsOptions, 
                nutsScore = get_score(_hasNuts, _nutsOptions),
                hasMilk = _hasMilk,
                milkOptions = _milkOptions,
                milkScore = get_score(_hasMilk, _milkOptions),
                hasWheat = _hasWheat,
                wheatOptions = _wheatOptions, 
                wheatScore = get_score(_hasWheat, _wheatOptions),
                hasFish = _hasFish,
                fishOptions = _fishOptions, 
                fishScore = get_score(_hasFish, _fishOptions),
                hasShellfish = _hasShellfish,
                shellfishOptions = _shellfishOptions, 
                shellfishScore = get_score(_hasShellfish, _shellfishOptions),
                hasSesami = _hasSesami,
                sesamiOptions = _sesamiOptions, 
                sesamiScore = get_score(_hasSesami, _sesamiOptions),
                hasPeanuts = _hasPeanuts,
                peanutsOptions = _peanutsOptions, 
                peanutsScore = get_score(_hasPeanuts, _peanutsOptions),
                hasSoy = _hasSoy,
                soyOptions = _soyOptions, 
                soyScore = get_score(_hasSoy, _soyOptions)
                )
        try:
            db.session.add(db_row)
            db.session.commit()
            return redirect(url_for('test'))
        except:
            return redirect(url_for('test'))

@app.route("/update_row", methods=['POST', 'GET'])
def update_row():
    if request.method == "POST":

        _itemName = request.form['itemname']
        
        _hasEggs = True if (request.form.get('eggCheck')) else False
        _eggOptions = True if (request.form.get('eggOptions') == "Yes") else False

        _hasNuts = True if (request.form.get('nutsCheck')) else False
        _nutsOptions = True if (request.form.get('nutsOptions') == "Yes") else False

        _hasMilk = True if (request.form.get('milkCheck')) else False
        _milkOptions = True if (request.form.get('milkOptions') == "Yes") else False

        _hasWheat = True if (request.form.get('wheatCheck')) else False
        _wheatOptions = True if (request.form.get('wheatOptions') == "Yes") else False

        _hasFish = True if (request.form.get('fishCheck')) else False
        _fishOptions = True if (request.form.get('fishOptions') == "Yes") else False

        _hasShellfish = True if (request.form.get('shellfishCheck')) else False
        _shellfishOptions = True if (request.form.get('shellfishOptions') == "Yes") else False

        _hasSesami = True if (request.form.get('sesamiCheck')) else False
        _sesamiOptions = True if (request.form.get('sesamiOptions') == "Yes") else False

        _hasPeanuts = True if (request.form.get('peanutsCheck')) else False
        _peanutsOptions = True if (request.form.get('peanutsOptions') == "Yes") else False

        _hasSoy = True if (request.form.get('soyCheck')) else False
        _soyOptions = True if (request.form.get('soyOptions') == "Yes") else False

        try:
            _db_row = Allergen.query.filter_by(customerID=0, item=_itemName).first()
            print("dbrow")
            print(_db_row.item)
            print(_hasEggs)
            _db_row.timestamp = datetime.now()
            _db_row.hasEggs = _hasEggs
            _db_row.eggOptions = _eggOptions
            _db_row.eggScore = get_score(_hasEggs, _eggOptions)
            _db_row.hasNuts = _hasNuts
            _db_row.nutsOptions = _nutsOptions
            _db_row.nutsScore = get_score(_hasNuts, _nutsOptions)
            _db_row.hasMilk = _hasMilk
            _db_row.milkOptions = _milkOptions
            _db_row.milkScore = get_score(_hasMilk, _milkOptions)
            _db_row.hasWheat = _hasWheat
            _db_row.wheatOptions = _wheatOptions
            _db_row.wheatScore = get_score(_hasWheat, _wheatOptions)
            _db_row.hasFish = _hasFish
            _db_row.fishOptions = _fishOptions
            _db_row.fishScore = get_score(_hasFish, _fishOptions)
            _db_row.hasShellfish = _hasShellfish
            _db_row.shellfishOptions = _shellfishOptions
            _db_row.shellfishScore = get_score(_hasShellfish, _shellfishOptions)
            _db_row.hasSesami = _hasSesami
            _db_row.sesamiOptions = _sesamiOptions
            _db_row.sesamiScore = get_score(_hasSesami, _sesamiOptions)
            _db_row.hasPeanuts = _hasPeanuts
            _db_row.peanutsOptions = _peanutsOptions
            _db_row.peanutsScore = get_score(_hasPeanuts, _peanutsOptions)
            _db_row.hasSoy = _hasSoy
            _db_row.soyOptions = _soyOptions
            _db_row.soyScore = get_score(_hasSoy, _soyOptions)
            db.session.commit()
            return redirect(url_for('test'))
        except:
            return redirect(url_for('test'))


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

@app.route("/query_db", methods=['POST', 'GET'])
def query_db():
    if request.method == "POST":
        allergen_data = request.get_json()

        chkWheat = allergen_data[1]['chkWheat']
        chkMilk = allergen_data[2]['chkMilk']
        chkEggs = allergen_data[3]['chkEggs']
        chkFish = allergen_data[4]['chkFish']
        chkShellfish = allergen_data[5]['chkShellfish']
        chkSesame = allergen_data[6]['chkSesame']
        chkNuts = allergen_data[7]['chkNuts']
        chkPeanuts = allergen_data[8]['chkPeanuts']
        chkSoy = allergen_data[9]['chkSoy']

        # Query data
        # This is not an elegant way to do dynamic query but implemented by successive subqueries to filter down

        results = Allergen.query.filter(Allergen.customerID==allergen_data[0]['customerID'])

        if chkMilk:
            results = results.filter(Allergen.milkScore>=50)
        
        if chkEggs:
            results = results.filter(Allergen.eggScore>=50)
        
        if chkNuts:
            results = results.filter(Allergen.nutsScore>=50)
        
        if chkWheat:
            results = results.filter(Allergen.wheatScore>=50)
        
        if chkFish:
            results = results.filter(Allergen.fishScore>=50)
        
        if chkShellfish:
            results = results.filter(Allergen.shellfishScore>=50)
        
        if chkSesame:
            results = results.filter(Allergen.sesamiScore>=50)
        
        if chkPeanuts:
            results = results.filter(Allergen.peanutsScore>=50)
        
        if chkSoy:
            results = results.filter(Allergen.soyScore>=50)

        results = results.order_by(Allergen.item)
        response = []
        for result in results.all():
            response.append({'item': result.item,
                    'eggScore': result.eggScore,
                    'nutsScore': result.nutsScore,
                    'milkScore': result.milkScore,
                    'wheatScore': result.wheatScore,
                    'fishScore': result.fishScore,
                    'shellfishScore': result.shellfishScore,
                    'sesamiScore': result.sesamiScore,
                    'peanutsScore': result.peanutsScore,
                    'soyScore': result.soyScore
                    })
        
        # Debug
        print(response)

        return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)

# References:
# https://stackoverflow.com/questions/38664088/flask-404-for-post-request