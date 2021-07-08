from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application import db #app or application here?
from flask import current_app as app
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#db = SQLAlchemy(app)

# Model Class Definitions

class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)
    website = db.Column(
        db.String(60),
        index=False,
        unique=False,
        nullable=True
	)
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


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
    sensor_type_name = db.Column(db.String(255), nullable=False)
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
                str(self.sensor_id),
                self.sensor_observation_data
            )
        return "{}".format(str(self.id))

# End Data Model Class Objects