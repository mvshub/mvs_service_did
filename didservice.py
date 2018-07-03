#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sudo apt-get install sqlite3 libsqlite3-dev
# sudo pip3 install flask
# sudo pip3 install flask-sqlalchemy
# sudo pip3 install sqlalchemy-utils

# python3 didservice.py

import json
from flask import Flask, abort, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy_utils

database_uri = 'sqlite:///dids.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

max_exchanger_length        = 32
max_customer_length         = 32
max_did_length              = 64
max_address_length          = 40

code_success                = 0
code_invalid_parameter      = 1
code_not_found              = 2
code_already_exist          = 3

class Did(db.Model):
    __tablename__ = 'dids'

    id = db.Column(db.Integer, primary_key=True)
    exchanger = db.Column(db.String(max_exchanger_length), unique=False)
    customer = db.Column(db.String(max_customer_length), unique=False)
    did = db.Column(db.String(max_did_length), unique=True)
    address = db.Column(db.String(max_address_length), unique=True)

    def __init__(self, exchanger, customer, did, address):
        self.exchanger = exchanger
        self.customer = customer
        self.did = did
        self.address = address

    def __repr__(self):
        return '<Did %r>' % self.did

class ObjectEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class JsonDid:
    def __init__(self, exchanger, customer, did, address):
        self.exchanger = exchanger
        self.customer = customer
        self.did = did
        self.address = address

def is_valid(param, max_length):
    length = 0 if None == param else len(param)
    return length > 0 and length <= max_length

@app.route('/')
def root():
    return "MVS micro service"

# RESTfull API
# http://127.0.0.1:5000/adddid/rightbtc/kesalin/kesalin/MTqgx7CHA8y1TUF1re5NLyT4mzKvCxWTyi
@app.route('/adddid/<exchanger>/<customer>/<did>/<address>')
def add_did(exchanger, customer, did, address):
    if ((not is_valid(exchanger, max_exchanger_length))
        or (not is_valid(customer, max_customer_length))
        or (not is_valid(did, max_did_length))
        or (not is_valid(address, max_address_length))):
        return jsonify({'code' : code_invalid_parameter, 'result': 'invalid paremeter!'})

    target = Did.query.filter_by(exchanger=exchanger, customer=customer).first()
    if target:
        return jsonify({'error' : code_already_exist, 'result' : 'already exist!'})
    else:
        target = Did(exchanger, customer, did, address)
        db.session.add(target)
        db.session.commit()

        jsonDid = JsonDid(target.exchanger, target.customer, target.did, target.address)
        return jsonify({"error" : 0, "result" : json.dumps(jsonDid, cls=ObjectEncoder)})

# RESTfull API
# http://127.0.0.1:5000/getdid/rightbtc/kesalin
@app.route("/getdid/<exchanger>/<customer>")
def get_did(exchanger, customer):
    if ((not is_valid(exchanger, max_exchanger_length))
        or (not is_valid(customer, max_customer_length))):
        return jsonify({'code' : code_invalid_parameter, 'result': 'invalid paremeter!'})

    did = Did.query.filter_by(exchanger=exchanger, customer=customer).first()
    if did:
        jsonDid = JsonDid(did.exchanger, did.customer, did.did, did.address)
        return jsonify({'code' : code_success, 'result': json.dumps(jsonDid, cls=ObjectEncoder)})
    else:
        return jsonify({'code' : code_not_found, 'result': 'not found'})

# RESTfull API
# http://127.0.0.1:5000/deletedid/rightbtc/kesalin
@app.route("/deletedid/<exchanger>/<customer>")
def delete_did(exchanger, customer):
    if ((not is_valid(exchanger, max_exchanger_length))
        or (not is_valid(customer, max_customer_length))):
        return jsonify({'code' : code_invalid_parameter, 'result': 'invalid paremeter!'})

    dids = Did.query.filter_by(exchanger=exchanger, customer=customer).all()
    if dids:
        for did in dids:
            db.session.delete(did)
            db.session.commit()

        did = dids[0]
        jsonDid = JsonDid(did.exchanger, did.customer, did.did, did.address)
        return jsonify({'code' : code_success, 'result': json.dumps(jsonDid, cls=ObjectEncoder)})
    else:
        return jsonify({'code' : code_not_found, 'result': 'not found'})


if __name__ == "__main__":
    if not sqlalchemy_utils.functions.database_exists(database_uri):
        db.create_all()

    app.run(debug=True)
