from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_admin import Admin
from forms import SearchForm
import config
from flask_admin.contrib.sqla import ModelView


# create application
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["FLASK_ADMIN_SWATCH"] = "flatly"

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
    sensor_type_name = db.Column(db.String(255), nullable=False)
    sensor_type_description = db.Column(db.String(255), nullable=False)
    sensor_type_code = db.Column(db.String(255), nullable=False)
    sensor_manufacturer = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        if self.id and self.sensor_type_name:
            return "{}".format(self.sensor_type_name)
        return "{}".format(str(self.id))


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
    pass

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