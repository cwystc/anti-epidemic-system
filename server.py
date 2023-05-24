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
        return render_template('form.html', t1 = 'location_name', t2 = 'risk_level')
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

@app.route('/update2') #add a new test site
def update2():
    test_site_name = request.args.get('test_site_name', '')
    if not test_site_name:
        return render_template('form.html', t1 = 'test_site_name')
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    insertion = ('''
        INSERT INTO `testing sites`(test_site_number, test_site_name) VALUES
        (0, %s);
        ''')
    cursor.execute(insertion, (test_site_name,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return 'insert into testing sites (?, %s) successfully' % (test_site_name,)

@app.route('/query1') #query the risk level of a location
def query1():
    location_name = request.args.get('location_name', '')
    if not location_name:
        return render_template('form.html', t1 = 'location_name')
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
