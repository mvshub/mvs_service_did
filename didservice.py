#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sudo apt-get install sqlite3 libsqlite3-dev
# sudo pip3 install flask
# sudo pip3 install flask-restful
# sudo pip3 install flask-sqlalchemy
# sudo pip3 install sqlalchemy-utils

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
    exchanger = db.Column(db.String(32), unique=False)
    customer = db.Column(db.String(32), unique=False)
    did = db.Column(db.String(64), unique=True)
    address = db.Column(db.String(64), unique=True)

    def __init__(self, exchanger, customer, did, address):
        self.exchanger = exchanger
        self.customer = customer
        self.did = did
        self.address = address

    def __repr__(self):
        return '<Did %r>' % self.did

class JsonDid:
    def __init__(self, exchanger, customer, did, address):
        self.exchanger = exchanger
        self.customer = customer
        self.did = did
        self.address = address

    def as_dict(self):
       return self.__dict__

def is_valid(param, max_length):
    length = 0 if None == param else len(param)
    return length > 0 and length <= max_length


@app.route('/')
def root():
    return jsonify({'code' : code_success, result: "MVS service"})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'MVS service not found'}), 404)


# curl 'http://127.0.0.1:5000/mvs/api/v1/did' -i -X POST -H "Content-Type: application/json" -d '{"exchanger": "rightbtc", "customer": "kesalin", "did": "kesalin", "address": "MTrW3QK8mjmTYSozdkLa7k9hyCExUBWYwP"}'
@app.route('/mvs/api/v1/did', methods=['POST'])
def set_did():
    if (not request.json or 'exchanger' not in request.json
        or 'customer' not in request.json
        or 'did' not in request.json
        or 'address' not in request.json):
        print("invalid request json! {}".format(request.json))
        return jsonify({'error' : code_invalid_parameter, 'result' : 'invalid paremeter!'})

    exchanger = request.json['exchanger']
    customer = request.json['customer']
    did = request.json['did']
    address = request.json['address']

    if ((not is_valid(exchanger, max_exchanger_length))
        or (not is_valid(customer, max_customer_length))
        or (not is_valid(did, max_did_length))
        or (not is_valid(address, max_address_length))):
        return jsonify({'code' : code_invalid_parameter, 'result': 'invalid paremeter!'})

    target = Did.query.filter_by(exchanger = exchanger, customer=customer).first()
    if target:
        return jsonify({'error' : code_already_exist, 'result' : 'already exist!'})
    else:
        target = Did(exchanger, customer, did, address)
        db.session.add(target)
        db.session.commit()

        jsonDid = JsonDid(target.exchanger, target.customer, target.did, target.address)
        return jsonify({"error" : code_success, "result" : jsonDid.as_dict()})


# curl -i -X GET 'http://127.0.0.1:5000/mvs/api/v1/did/rightbtc/kesalin'
@app.route("/mvs/api/v1/did/<exchanger>/<customer>")
def get_did(exchanger, customer, methods=['GET']):
    if ((not is_valid(exchanger, max_exchanger_length))
        or (not is_valid(customer, max_customer_length))):
        return jsonify({'code' : code_invalid_parameter, 'result': 'invalid paremeter!'})

    did = Did.query.filter_by(exchanger=exchanger, customer=customer).first()
    if did:
        jsonDid = JsonDid(did.exchanger, did.customer, did.did, did.address)
        return jsonify({'code' : code_success, 'result': jsonDid.as_dict()})
    else:
        return jsonify({'code' : code_not_found, 'result': 'not found'})


# curl -i -X DELETE 'http://127.0.0.1:5000/mvs/api/v1/did/rightbtc/kesalin'
@app.route("/mvs/api/v1/did/<exchanger>/<customer>", methods=['DELETE'])
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
        return jsonify({'code' : code_success, 'result': jsonDid.as_dict()})
    else:
        return jsonify({'code' : code_not_found, 'result': 'not found'})

if __name__ == "__main__":
    if not sqlalchemy_utils.functions.database_exists(database_uri):
        db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True)
