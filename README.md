# Beacon 
A SQLAlchemy Flask Admin UI for the Beacon Data Model

A Flask Admin ModelView Admin for:

* Dealer
* Customer
* Location
* TankOrMeter
* Radio
* RadioSensor
* RadioSensorData
* RadioType
* SensorType
* User
* Additional models in development

### Getting Started

Clone this repository

```
$ git clone https://github.com/craigderington/beacon-data-admin.git
$ cd beacon-data-admin
$ virtualenv venv --python=python3
$ . venv/bin/activate
$ pip install -r requirements.txt
```

### Edit Environment Template

```
$ nano venv/lib/flask_admin/templates/bootstrap4/base.html
```

Line 40: Add 0px padding to container-fluid
```
<div class="container-fluid p-0">
```

Line 75: Add 50px; padding to block body
```
<div class="container-fluid p-50">
    {% block body %}{% endblock %}
</div>
```

### Start the Beacon Data Admin
```
$ gunicorn -b 0.0.0.0:8580 -w 2 app:app
[2021-06-16 11:16:56 -0400] [2614] [INFO] Starting gunicorn 20.1.0
[2021-06-16 11:16:56 -0400] [2614] [INFO] Listening at: http://0.0.0.0:8580 (2614)
[2021-06-16 11:16:56 -0400] [2614] [INFO] Using worker: sync
[2021-06-16 11:16:56 -0400] [2615] [INFO] Booting worker with pid: 2615
[2021-06-16 11:16:56 -0400] [2616] [INFO] Booting worker with pid: 2616
```

### Load the Admin in Browser


### TODOS

* User Token Authentication
* Forms &amp; Search Feature
* Blueprints
* App Factory Pattern
* Celery Integration
* Data Mining/Machine Learning



