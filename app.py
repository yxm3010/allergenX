import qrcode
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
import os.path
import random


# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
# create the extension
db = SQLAlchemy()
login_manager = LoginManager()
# create the app
app = Flask(__name__)

# https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY
app.config["SECRET_KEY"] = 'm\xe9*Y\xc0\xd90\xb4\xce\xb9/h\xe3\xc3\xd3\xd1\xfa>\xc4\xf8C\x10\xa5\xbb'

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///allergenx.db"
app.config["SQLALCHEMY_BINDS"] = {
    "auth": "sqlite:///user.db"
}
# https://docs.sqlalchemy.org/en/20/core/engines.html
 
 # initialize the app with the extension
db.init_app(app)

# initialize the login manager
login_manager.init_app(app)

def get_score(check, opt):
        if(check):
            if not opt:
                return 0 # You cannot avoid allergen
            else:
                return 50 # Restrant has option to avoid allergen
        else:
            return 100 # Allergen not used in the ingredients 

class User(db.Model):
    __tablename__ = "users"
    __bind_key__ = "auth"

    customerID = db.Column('customerID', db.Integer, unique=True, primary_key=True)
    firstname = db.Column('firstname', db.String(120))
    lastname = db.Column('lastname', db.String(120))
    useremail = db.Column('email', db.String(120), unique=True)
    userpassword = db.Column('userpassword', db.String(120))
    selectplan = db.Column('selectplan', db.String(120))
    venuename = db.Column('venuename', db.String(120))
    address = db.Column('address', db.String(120))
    city = db.Column('city', db.String(120))
    state = db.Column('state', db.String(120))
    zip = db.Column('zip', db.Integer)
    membersince = db.Column('membersince', db.String(120))
    
    def is_active(self):
        return True

    def is_authenticated(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.customerID)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

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

@login_manager.user_loader
def load_user(customerID):
    return User.query.filter(User.customerID==customerID).first()

# Make it dynamic website using URL arguments. Store it in session cookie
@app.route("/main")
def main():
    session['customerID'] = request.args.get('location')
    print(request.args.get('location'))
    return render_template('index.html')

@app.route("/home")
def home():
    location = session['customerID']
    return redirect(url_for('main', location=location))

@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('test'))
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/register", methods=['POST', 'GET'])
def register():

    def _get_new_id():
        random.seed(int(datetime.now().timestamp()*1000))
        return int(random.random()*1000000)
    
    if not os.path.exists('user.db'):
        with app.app_context(): # I think this allows db to access app config data like SQLALCHEMY_DATABASE_URI
            db.create_all(["auth"]) # Creates bind for both allergenx.db and auth.db

    if request.method == "POST":
        db_row =  User(
            customerID = _get_new_id(),
            firstname = request.form['firstname'],
            lastname = request.form['lastname'],
            useremail = request.form['useremail'],
            userpassword = request.form['userpassword'],
            selectplan = request.form.get('selectplan'),
            venuename = request.form['venuename'],
            address = request.form['address'],
            city = request.form['city'],
            state = request.form['state'],
            zip = request.form['zip'],
            membersince = datetime.now().strftime("%m/%d/%y")
         )
        
        email_exits = User.query.filter(User.useremail==request.form['useremail']).all()

        if not email_exits:
            db.session.add(db_row)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return redirect(url_for('signup'))

@app.route("/auth", methods=['POST', 'GET'])
def auth():
    if request.method == "POST":
        useremail = request.form['useremail']
        userpassword = request.form['userpassword']
        result = User.query.filter(User.useremail==useremail,
                                   User.userpassword==userpassword).first()
        if result:
            login_user(result, remember=True)
            return redirect(url_for('test'))
    return redirect(url_for('login'))

@app.route("/test2")
@login_required
def test():
    if not os.path.exists('allergenx.db'):
        with app.app_context(): # I think this allows db to access app config data like SQLALCHEMY_DATABASE_URI
            db.create_all([None]) # Creates bind for both allergenx.db and auth.db
    return render_template('test2.html')

@app.route("/load_current_db", methods=['POST', 'GET'])
@login_required
def load_current_db():
    results = Allergen.query.filter_by(customerID=current_user.customerID).order_by(Allergen.item).all()
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

@app.route("/add_new_row", methods=['POST', 'GET'])
@login_required
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
                customerID = current_user.customerID,
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
@login_required
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
            _db_row = Allergen.query.filter_by(customerID=current_user.customerID, item=_itemName).first()
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
@login_required
def delete():
    if request.method == "POST":
        serverData = request.get_json()
        items = serverData[1]['items']
        print(serverData)
        for itemName in items:
            Allergen.query.filter_by(customerID=current_user.customerID, item=itemName).delete()
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
    
@app.route("/gen_qrcode", methods=['POST', 'GET'])
@login_required
def gen_qrcode():
    if request.method=="POST":
        print("QRCODE")
        pil_img = qrcode.make(f'https://corporate.mcdonalds.com/corpmcd/home.html?location={current_user.customerID}')
        img_IO = BytesIO()
        pil_img.save(img_IO,'PNG')
        img_IO.seek(0)
        return send_file(img_IO, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)

# References:
# https://stackoverflow.com/questions/38664088/flask-404-for-post-request