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
    <h1>Welcome to the anti-epidemic system! </h1>
    <a href="/query1"> query the risk level of a location </a>
    <br>
    <a href="/update1"> update the risk level of a location </a>
    <br>
    <a href="/update2"> add a new test site </a>
    <br>
    <a href="/update3"> delete a test site </a>
    <br>
    <a href="/update4"> add a person </a>
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

@app.route('/update3') #delete a test site
def update3():
    test_site_name = request.args.get('test_site_name', '')
    if not test_site_name:
        return render_template('form.html', t1 = 'test_site_name')
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    deletion = ('''
        DELETE FROM `testing sites`
        WHERE test_site_name = %s
        ''')
    cursor.execute(deletion, (test_site_name,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return 'delete from testing sites (?, %s) successfully' % (test_site_name,)

@app.route('/update4') #add a person
def update4():
    ID_number = request.args.get('ID_number', '')
    person_name = request.args.get('person_name', '')
    advisor_name = request.args.get('advisor_name', '')
    if not ID_number.isdigit() or not person_name:
        return render_template('form.html', t1 = 'ID_number', t2 = 'person_name', t3 = 'advisor_name')
    ID_number = int(ID_number)

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    ret = None
    query = ('''
        SELECT COUNT(*) FROM person
        WHERE ID_number = %s
        ''')
    cursor.execute(query, (ID_number,))
    for x, in cursor:
        if x > 0:
            ret = 'person with this ID_number already exists!!!'
    if advisor_name != 'NULL':
        query = ('''
            SELECT ID_number FROM person
            WHERE person_name = %s
            ''')
        cursor.execute(query, (advisor_name,))
        advisor = None
        for x, in cursor:
            advisor = x
        if advisor is None:
            ret = 'cannot find this advisor!!!'
    if ret:
        cursor.close()
        cnx.close()
        return ret
    
    if advisor_name != 'NULL':
        insertion = ('''
            INSERT INTO person(ID_number, person_name, advisor) VALUES
            (%s, %s, %s);
            ''')
        cursor.execute(insertion, (ID_number, person_name, advisor))
    else:
        insertion = ('''
            INSERT INTO person(ID_number, person_name, advisor) VALUES
            (%s, %s, NULL);
            ''')
        cursor.execute(insertion, (ID_number, person_name))
    cnx.commit()
    cursor.close()
    cnx.close()
    return 'insert into person (%s, %s, ?) successfully' % (ID_number, person_name)

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
