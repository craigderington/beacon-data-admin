from flask import Flask, request, render_template, jsonify, session, redirect, flash
import flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_admin import Admin
from sqlalchemy.sql.functions import now

from flask_admin.contrib.sqla import ModelView
import flask_login
from werkzeug import security
import wtforms

#from .constants import USER, USER_ROLE, ADMIN, INACTIVE, USER_STATUS
# User role
ADMIN = 0
STAFF = 1
USER = 2
USER_ROLE = {
    ADMIN: 'admin',
    STAFF: 'staff',
    USER: 'user',
}

# User status
INACTIVE = 0
NEW = 1
ACTIVE = 2
USER_STATUS = {
    INACTIVE: 'inactive',
    NEW: 'new',
    ACTIVE: 'active',
}


# Account Type
BASIC = 0
PRO = 1
PREMIUM = 2
ACCOUNT_TYPE = {
    BASIC: 'basic',
    PRO: 'pro',
    PREMIUM: 'premium'
}


#from flask_login import current_user
#from flask_admin.contrib import sqla


# create application
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["FLASK_ADMIN_SWATCH"] = "flatly"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
import config 

# alchemy
db = SQLAlchemy(app)

# create the Admin and the Views
admin = Admin(app, name="🦉 RMS", template_mode="bootstrap4")

# Model Class Definitions
class Dealer(db.Model):
    __tablename__ = "dealer"
    id = db.Column(db.Integer, primary_key=True)
    dealer_name = db.Column(db.String(255), nullable=False, unique=True)
    dealer_address1 = db.Column(db.String(255), nullable=False)
    dealer_address2 = db.Column(db.String(255), nullable=False)
    dealer_city = db.Column(db.String(255), nullable=False)
    dealer_state = db.Column(db.String(2), nullable=False)
    dealer_zip_code = db.Column(db.String(10), nullable=False)
    dealer_email = db.Column(db.String(255), nullable=True)
    dealer_phone = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        if self.id and self.dealer_name:
            return "{}".format(self.dealer_name)
    
    def get_dealer_email(self):
        if self.dealer_email:
            return "{}".format(str(self.dealer_email))
        return False

    def get_dealer_address(self):
        if self.dealer_address1 and self.dealer_address2 and self.dealer_city and self.dealer_state and self.dealer_zip_code:
            return "{} {} {} {} {}".format(self.dealer_address1, self.dealer_address2, self.dealer_city, self.dealer_state, self.dealer_zip_code)


class Receiver(db.Model):
    __tablename__ = "receiver"
    id = db.Column(db.Integer, primary_key=True)
    receiver_type_id = db.Column(db.Integer, db.ForeignKey("receivertype.id"), nullable=False)
    receiver = relationship("ReceiverType")
    receiver_name = db.Column(db.String(255), nullable=False, unique=True)
    receiver_fqdn = db.Column(db.String(255), nullable=False)
    receiver_ip = db.Column(db.String(255), nullable=False)
    receiver_status = db.Column(db.String(255), nullable=False)
    receiver_port = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        if self.id and self.receiver_name and self.receiver_status:
            return "name: {} status: {}".format(self.receiver_name, self.receiver_status)
        return "no name/status, ID: {}".format(str(self.id))

    def get_receiver_netaddr(self):
        if self.receiver_ip and self.receiver_port:
            return "{}:{}".format(self.receiver_ip,self.receiver_port)


class ReceiverType(db.Model):
    __tablename__ = "receivertype"
    id = db.Column(db.Integer, primary_key=True)
    receiver_type_name = db.Column(db.String(255), nullable=False)
    receiver_version = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        if self.id and self.receiver_type_name and self.receiver_version:
            return "name: {} version: {}".format(self.receiver_type_name, self.receiver_version)
        return "no name/version, ID: {}".format(str(self.id))


class DealerSettings(db.Model):
    __tablename__ = "dealersettings"
    id = db.Column(db.Integer, primary_key=True)
    dealer_id = db.Column(db.Integer, db.ForeignKey("dealer.id"), nullable=False)
    dealer_config = db.Column(db.String(1024), nullable=True) # stored as json

    def as_dict(self):
        return dict(self.dealer_config)
    
    def get_dealer_config(self):
        if self.dealer_config:
            return "{}".format(self.dealer_config.as_dict())
        return "{}".format(str(self.id))

class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    dealer_id = db.Column(db.Integer, db.ForeignKey("dealer.id"), nullable=False)
    dealer = relationship("Dealer")
    customer_name = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    customer_status = db.Column(db.String(255), nullable=False)
    customer_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        if self.id and self.customer_name:
            return "{}".format(self.customer_name)

    def is_active(self):
        if self.is_active:
            return True
        return False

class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    customer = relationship("Customer")
    location_type = db.Column(db.String(255), nullable=False)
    location_address1 = db.Column(db.String(255), nullable=False)
    location_date = db.Column(db.DateTime)

    def __repr__(self):
        if self.id and self.customer and self.location_address1:
            return "{} - {}".format(self.customer, self.location_address1)
        return "Customer Not Found: {}".format(self.location_address1)


class Tank(db.Model):
    __tablename__ = "tank"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    customer = relationship("Customer")
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    location = relationship("Location")
    tank_radio_id = db.Column(db.ForeignKey("radio.id"))
    tank_radio = relationship("Radio")
    tank_name = db.Column(db.String(255), nullable=False)
    tank_position = db.Column(db.String(255), nullable=False)
    tank_capacity = db.Column(db.Integer, nullable=False, default=0)
    tank_inspection_date = db.Column(db.DateTime)
    tank_install_date = db.Column(db.DateTime)
    
    def __repr__(self):
        if self.id and self.tank_name and self.tank_capacity:
            return "{}-{} gal".format(self.tank_name, self.tank_capacity)
        return "{} gal".format(self.tank_capacity)


class RadioType(db.Model):
    __tablename__ = "radiotype"
    id = db.Column(db.Integer, primary_key=True)
    radio_type_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        if self.id and self.radio_type_name:
            return "{}".format(self.radio_type_name)
        return "{}".format(str(self.id))


class SensorType(db.Model):
    __tablename__ = "sensortype"
    id = db.Column(db.Integer, primary_key=True)
    sensor_type_name = db.Column(db.String(255), nullable=False, unique=True)
    sensor_type_description = db.Column(db.String(255), nullable=False)
    sensor_type_code = db.Column(db.String(255), nullable=False)
    sensor_manufacturer = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        if self.id and self.sensor_type_name:
            return "{}".format(self.sensor_type_name)
        return "{}".format(str(self.id))

    def get_sensor_type_code(self):
        if self.sensor_type_code:
            return "{}".format(self.sensor_type_code)


class Radio(db.Model):
    __tablename__ = "radio"
    id = db.Column(db.Integer, primary_key=True)
    dealer_id = db.Column(db.Integer, db.ForeignKey("dealer.id"), nullable=False)
    dealer = relationship("Dealer")
    radio_imei = db.Column(db.String(255), nullable=False)
    radio_mtu_id = db.Column(db.String(255), nullable=False)
    radio_serial_number = db.Column(db.String(255), nullable=False, unique=True)
    radio_network_id = db.Column(db.String(255), nullable=True)
    radio_type_id = db.Column(db.Integer, db.ForeignKey("radiotype.id"), nullable=False)
    radio_type = relationship("RadioType")
    radio_params = db.Column(db.String(255), nullable=True)
    radio_receiver_url = db.Column(db.String(255), nullable=True)
    radio_receiver_port = db.Column(db.Integer, nullable=True)
    radio_receiver_ip = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        if self.id and self.radio_network_id:
            return "{}".format(self.radio_network_id)
        return "{}".format(self.id)
    
    def get_radio_params(self):
        if self.radio_params:
            return "{}".format(str(self.radio_params))
        return "{}".format(str(self.id))

    def get_radio_receiver_netaddr(self):
        if self.radio_receiver_ip and self.radio_receiver_port:
            return "{}:{}".format(self.radio_receiver_ip,self.radio_receiver_port)


class RadioSensor(db.Model):
    __tablename__ = "radiosensor"
    id = db.Column(db.Integer, primary_key=True)
    sensor_name = db.Column(db.String(255), nullable=False)
    radio_id = db.Column(db.Integer, db.ForeignKey("radio.id"), nullable=False)
    radio = relationship("Radio")
    sensor_type_id = db.Column(db.Integer, db.ForeignKey("sensortype.id"), nullable=False)
    sensor_type = relationship("SensorType")
    sensor_latitude = db.Column(db.String(255), nullable=False)
    sensor_longitude = db.Column(db.String(255), nullable=False)
    sensor_datastream = db.Column(db.String(1024), nullable=False)
    sensor_observation = db.Column(db.String(255), nullable=False)
    sensor_thing = db.Column(db.String(255), nullable=False)
    sensor_location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    sensor_location = relationship("Location")
    sensor_params = db.Column(db.String(255), nullable=False)
    sensor_flow = db.Column(db.String(255), nullable=False)
    sensor_calculate = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=True)
    customer = relationship("Customer")

    def __repr__(self):
        if self.id and self.sensor_name and self.sensor_type:
            return "{}.{}".format(self.sensor_type, self.sensor_name)
        return "{}".format(str(self.id))
    
    def get_sensor_params(self):
        if self.sensor_params:
            return "{}".format(str(self.sensor_params))
    
    def get_sensor_data(self):
        if self.sensor_data:
            return "{}".format(self.sensor_data)
    
    def get_sensor_location(self):
        if self.sensor_location:
            return "{}.{}".format(self.sensor_name, self.sensor_location)
        return "{}".format(self.sensor_location)
    
    def get_sensor_latlong(self):
        if self.sensor_latitude and self.sensor_longitude:
            return "{}/{}".format(self.sensor_latitude, self.sensor_longitude)
    
    def get_sensor_customer(self):
        if self.customer_id:
            return "{}".format(self.customer)
        return "{}".format(str(self.customer_id))


class RadioSensorData(db.Model):
    __tablename__ = "radiosensordata"
    id = db.Column(db.Integer, primary_key=True)
    radio_id = db.Column(db.Integer, db.ForeignKey("radio.id"), nullable=False)
    radio = relationship("Radio")
    sensor_id = db.Column(db.Integer, db.ForeignKey("radiosensor.id"), nullable=False)
    sensor_type_data = db.Column(db.String(255), nullable=True)
    sensor_observation_data = db.Column(db.String(255), nullable=True)
    sensor_timestamp_data = db.Column(db.String(255), nullable=True)
    sensor_historical_data = db.Column(db.String(255), nullable=True)
    sensor_location_data = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        if self.id and self.radio and self.sensor_observation_data:
            return "Radio: {} Sensor ID: {} Sensor Data: {}".format(
                self.radio, 
                str(sensor_id),
                self.sensor_observation_data
            )
        return "{}".format(str(self.id))

# End Data Model Class Objects

class Users(db.Model, flask_login.UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255))

    email = db.Column(db.String(255), unique=True)
    email_activation_key = db.Column(db.String(255))

    created_time = db.Column(db.DateTime, default=now)

    _password = db.Column('password', db.String(100), nullable=False)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = security.generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = db.synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return security.check_password_hash(self.password, password)

    role_code = db.Column(db.SmallInteger, default=USER, nullable=False)

    @property
    def role(self):
        return USER_ROLE[self.role_code]

    def is_admin(self):
        return self.role_code == ADMIN

    def is_authenticated(self):
        return True

    # One-to-many relationship between users and user_statuses.
    status_code = db.Column(db.SmallInteger, default=INACTIVE)

    @property
    def status(self):
        return USER_STATUS[self.status_code]

    # Class methods

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter_by(email=login).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first_or_404()

    def check_email(self, email):
        return Users.query.filter(Users.email == email).count() == 0

    def __unicode__(self):
        _str = '%s. %s' % (self.id, self.name)
        return str(_str)




@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id) #User or Users?


# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Search using auto complete from database
    :params search term, str
    :return template
    """
    form1 = SearchForm(request.form)

    return render_template(
        "search.html",
        form=form1
    )


@app.route("/search", methods=["GET", "POST"])
def get_search_results():
    resp = Radio.query.all()
    radios = [r.as_dict() for r in resp]
    return jsonify(radios)


@app.route("/login", methods=["GET"])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = wtforms.LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        flask_login.login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        #if not is_safe_url(next):
        #    return flask.abort(400)

        return redirect(next or flask.url_for('index'))
    return render_template('login.html', form=form)

# create the model views for our classes
admin.add_view(ModelView(Dealer, db.session, endpoint="dealer"))
admin.add_view(ModelView(Customer, db.session, endpoint="customer"))
admin.add_view(ModelView(Location, db.session, endpoint="location"))
admin.add_view(ModelView(Tank, db.session, endpoint="tank"))
admin.add_view(ModelView(RadioType, db.session, endpoint="radiotype"))
admin.add_view(ModelView(Radio, db.session, endpoint="radio"))
admin.add_view(ModelView(RadioSensor, db.session, endpoint="radiosensor"))
admin.add_view(ModelView(RadioSensorData, db.session, endpoint="radiosensordata"))
admin.add_view(ModelView(SensorType, db.session, endpoint="sensortype"))
# admin.add_view(ModelView(User, db.session))

if __name__ == "__main__":
    # start the app
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )

    #need users, roles(admin users, customers, etc)