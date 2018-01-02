from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, exc
from sqlalchemy.orm import sessionmaker
from database import Base, Property
from flask import session as login_session
import random
import string
import httplib2
import json
from flask import make_response
import requests
import os

app = Flask(__name__)

engine = create_engine('sqlite:///propertylisting.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/property')
def showIndex():
    properties = session.query(Property).order_by(asc(Property.id))
    return render_template('index.html', properties=properties)
    
@app.route('/property/new', methods = ['GET', 'POST'])
def addProperty():
    if request.method == 'POST':
        newListing = Property(address = request.form['address'], price = request.form['price'], description = request.form['description'], bathroom = request.form['bathroom'], bedroom = request.form['bathroom'], sqft = request.form['sqft'], rentOrSale = request.form['rentOrSale'])
        session.add(newListing)
        try:
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            print 'integrity error '
            print e
            return render_template('newProperty.html')
        session.commit()
        return redirect(url_for('showIndex'))
    else:
        return render_template('newProperty.html')
    
@app.route('/property/<int:property_id>/')
def showProperty(property_id):
    property = session.query(Property).filter_by(id = property_id).one()
    return render_template('property.html', property=property)
    
@app.route('/property/<int:property_id>/edit', methods = ['GET', 'POST'])
def editProperty(property_id):
    editedProperty = session.query(Property).filter_by(id=property_id).one()
    if request.method == 'POST':
        if request.form['address']:
            editedProperty.address = request.form['address']
        if request.form['price']:
            editedProperty.price = request.form['price']
        if request.form['description']:
            editProperty.description = request.form['description']
        if request.form['bathroom']:
            editProperty.bathroom = request.form['bathroom']
        if request.form['bedroom']:
            editProperty.bedroom = request.form['bathroom']
        if request.form['sqft']:
            editProperty.sqft = request.form['sqft']
        if request.form['rentOrSale']:
            editedProperty.rentOrSale = request.form['rentOrSale']
        session.add(editedProperty)
        session.commit()
        return redirect(url_for('showProperty', property_id=editedProperty.id))
    else:
        return render_template('editProperty.html', property=editedProperty)

@app.route('/property/<int:property_id>/delete', methods = ['POST', 'GET'])
def deleteProperty(property_id):
    property = session.query(Property).filter_by(id=property_id).one()
    
    if request.method == 'POST':
        session.delete(property)
        session.commit()
        return redirect(url_for('showIndex'))
    else:
        return render_template('deleteProperty.html', property=property)
    
@app.route('/map')
def propertyMap():
    properties = session.query(Property)
    return render_template('propertyMap.html', properties=properties)
    
@app.route('/regmap')
def regMap():
    properties = session.query(Property)
    return render_template('regMap.html', properties=properties)
    


if __name__ == '__main__':
    app.debug = True
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
