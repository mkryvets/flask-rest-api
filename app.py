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

# Hospital Model
class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    foundation_year = db.Column(db.Integer)
    adress = db.Column(db.String(100), unique = True)
    capacity = db.Column(db.Integer)

    def __init__(self, name, foundation_year):
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
hospitals_schema = HospitalSchema(many = True)

# Run server
if __name__ == '__main__':
    app.run(debug=True)