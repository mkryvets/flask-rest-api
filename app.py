from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database initialization
db = SQLAlchemy(app)

# Marshmallow initialization
ma = Marshmallow(app)


# Hospital Class/Model
class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    foundation_year = db.Column(db.Integer)
    adress = db.Column(db.String(100), unique=True)
    capacity = db.Column(db.Integer)

    def __init__(self, name, foundation_year, adress, capacity):
        self.name = name
        self.foundation_year = foundation_year
        self.adress = adress
        self.capacity = capacity


# Hospital Schema
class HospitalSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'foundation_year', 'adress', 'capacity')


# Hospital schema initialization
hospital_schema = HospitalSchema()
hospitals_schema = HospitalSchema(many=True)


# Create a Hospital
@app.route('/hospital', methods=['POST'])
def app_hospital():
    name = request.json['name']
    foundation_year = request.json['foundation_year']
    adress = request.json['adress']
    capacity = request.json['capacity']

    new_hospital = Hospital(name, foundation_year, adress, capacity)

    db.session.add(new_hospital)
    db.session.commit()

    return hospital_schema.jsonify(new_hospital)


# Get All Hospitals
@app.route('/hospital', methods=['GET'])
def get_hospitals():
    all_hospitals = Hospital.query.all()
    result = hospitals_schema.dump(all_hospitals)
    return jsonify(result.data)


# Get Single Hospital
@app.route('/hospital/<id>', methods=['GET'])
def get_hospital(id):
    hospital = Hospital.query.get(id)
    return hospital_schema.jsonify(hospital)


# Update a Hospital
@app.route('/hospital/<id>', methods=['PUT'])
def update_hospital(id):
    hospital = Hospital.query.get(id)

    name = request.json['name']
    foundation_year = request.json['foundation_year']
    adress = request.json['adress']
    capacity = request.json['capacity']

    hospital.name = name
    hospital.foundation_year = foundation_year
    hospital.adress = adress
    hospital.capacity = capacity

    db.session.commit()

    return hospital_schema.jsonify(hospital)


# Delete Hospital
@app.route('/hospital/<id>', methods=['DELETE'])
def delete_hospital(id):
    hospital = Hospital.query.get(id)
    db.session.delete(hospital)
    db.session.commit()
    return hospital_schema.jsonify(hospital)


# Run server
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
