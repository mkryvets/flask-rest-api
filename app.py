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
    name = db.Column(db.String(100), unique=True, nullable=False)
    foundation_year = db.Column(db.Integer, nullable=False)
    adress = db.Column(db.String(100), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    departments = db.relationship('Department', cascade='all,delete', backref='hospital')

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


# Department Class/Model
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))

    def __init__(self, name, hospital_id):
        self.name = name
        self.hospital_id = hospital_id


# Department Schema
class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'hospital_id')


# Department schema initialization
department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)


# Create a Department
@app.route('/department', methods=['POST'])
def app_department():
    name = request.json['name']
    hospital_id = request.json['hospital_id']

    new_department = Department(name, hospital_id)

    db.session.add(new_department)
    db.session.commit()

    return department_schema.jsonify(new_department)


# Get All Departments
@app.route('/department', methods=['GET'])
def get_departments():
    all_departments = Department.query.all()
    result = departments_schema.dump(all_departments)
    return jsonify(result.data)


# Get Single Department
@app.route('/department/<id>', methods=['GET'])
def get_department(id):
    department = Department.query.get(id)
    return department_schema.jsonify(department)


# Update a Department
@app.route('/department/<id>', methods=['PUT'])
def update_department(id):
    department = Department.query.get(id)

    name = request.json['name']
    hospital_id = request.json['hospital_id']

    department.name = name
    department.hospital_id = hospital_id

    db.session.commit()

    return department_schema.jsonify(department)


# Delete Department
@app.route('/department/<id>', methods=['DELETE'])
def delete_department(id):
    department = Department.query.get(id)
    db.session.delete(department)
    db.session.commit()
    return department_schema.jsonify(department)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
