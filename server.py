from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
app = Flask(__name__)

import mysql.connector

password = input('Enter MySQL connection password:')
config = {
  'user': 'root',
  'password': password,
  'host': '127.0.0.1',
  'database': 'anti-epidemic db'
}


@app.route('/') #index page
def index():
    return ('''
    This is index page.
    If you want to query the risk level of a location, go to /query1
    If you want to update the risk level of a location, go to /update1
    ''')

@app.route('/update1') #update the risk level of a location
def update1():
    location_name = request.args.get('location_name', '')
    risk_level = request.args.get('risk_level', '')

    if not location_name or not risk_level:
        return ('''
            update the risk level of a location!
            Please go to /update1?location_name={location_name}&risk_level={risk_level}
            ''')
    if risk_level != 'low' and risk_level != 'medium' and risk_level != 'high':
        return 'the risk level of a location must be low, medium or high'
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    deletion = ('''
        DELETE FROM location
        WHERE location_name = %s
        ''')
    cursor.execute(deletion, (location_name,))
    insertion = ('''
        INSERT INTO location(location_number, location_name, risk_level) VALUES
        (0, %s, %s);
        ''')
    cursor.execute(insertion, (location_name, risk_level))
    cnx.commit()
    cursor.close()
    cnx.close()
    return 'insert into location (?, %s, %s) successfully' % (location_name, risk_level)

@app.route('/query1') #query the risk level of a location
def query1():
    location_name = request.args.get('location_name', '')
    if not location_name:
        return ('''
            query the risk level of a location!
            Please go to /query1?location_name={location_name}
            ''')
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ('''
        SELECT risk_level FROM location
        WHERE `location_name` = %s
        ''')
    cursor.execute(query, (location_name,))
    res = 'The queried location cannot be found!!!'
    for risk_level, in cursor:
        res = 'The risk level of {} is {}'.format(location_name, risk_level)
    cursor.close()
    cnx.close()
    return res
