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

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()


def person_name2ID_number(person_name):
    query = ('''
        SELECT ID_number FROM person
        WHERE person_name = %s
        ''')
    cursor.execute(query, (person_name,))
    res = None
    for x, in cursor:
        res = x
    return res

def location_name2location_number(location_name):
    query = ('''
        SELECT location_number FROM location
        WHERE location_name = %s
        ''')
    cursor.execute(query, (location_name,))
    res = None
    for x, in cursor:
        res = x
    return res

def test_site_name2test_site_number(test_site_name):
    query = ('''
        SELECT test_site_number FROM `testing sites`
        WHERE test_site_name = %s
        ''')
    cursor.execute(query, (test_site_name,))
    res = None
    for x, in cursor:
        res = x
    return res

@app.route('/') #index page
def index():
    return ('''
    <h1>Welcome to the anti-epidemic system! </h1>
    <a href="/update1"> add/update a location (and its risk level)</a>
    <br>
    <a href="/update2"> add a new test site </a>
    <br>
    <a href="/update3"> delete a test site </a>
    <br>
    <a href="/update4"> add a person </a>
    <br>
    <a href="/update5"> add a travel record </a>
    <br>
    <a href="/update6"> add a test record </a>
    <br>
    <a href="/query1"> query the risk level of a location </a>
    ''')

@app.route('/update1') #add/update a location (and its risk level)
def update1():
    location_name = request.args.get('location_name', '')
    risk_level = request.args.get('risk_level', '')

    if not location_name or not risk_level:
        return render_template('form.html', t1 = 'location_name', t2 = 'risk_level')
    if risk_level != 'low' and risk_level != 'medium' and risk_level != 'high':
        return 'the risk level of a location must be low, medium or high'
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
    return 'insert into location (?, %s, %s) successfully' % (location_name, risk_level)

@app.route('/update2') #add a new test site
def update2():
    test_site_name = request.args.get('test_site_name', '')
    if not test_site_name:
        return render_template('form.html', t1 = 'test_site_name')
    insertion = ('''
        INSERT INTO `testing sites`(test_site_number, test_site_name) VALUES
        (0, %s);
        ''')
    cursor.execute(insertion, (test_site_name,))
    cnx.commit()
    return 'insert into testing sites (?, %s) successfully' % (test_site_name,)

@app.route('/update3') #delete a test site
def update3():
    test_site_name = request.args.get('test_site_name', '')
    if not test_site_name:
        return render_template('form.html', t1 = 'test_site_name')
    deletion = ('''
        DELETE FROM `testing sites`
        WHERE test_site_name = %s
        ''')
    cursor.execute(deletion, (test_site_name,))
    cnx.commit()
    return 'delete from testing sites (?, %s) successfully' % (test_site_name,)

@app.route('/update4') #add a person
def update4():
    ID_number = request.args.get('ID_number', '')
    person_name = request.args.get('person_name', '')
    advisor_name = request.args.get('advisor_name', '')
    if not ID_number.isdigit() or not person_name:
        return render_template('form.html', t1 = 'ID_number', t2 = 'person_name', t3 = 'advisor_name')
    ID_number = int(ID_number)

    query = ('''
        SELECT COUNT(*) FROM person
        WHERE ID_number = %s
        ''')
    cursor.execute(query, (ID_number,))
    for x, in cursor:
        if x > 0:
            return 'person with this ID_number already exists!!!'
    if advisor_name != 'NULL':
        advisor = person_name2ID_number(advisor_name)
        if advisor is None:
            return 'cannot find this advisor'
    
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
    return 'insert into person (%s, %s, ?) successfully' % (ID_number, person_name)

@app.route('/update5') #add a travel record
def update5():
    traveler_name = request.args.get('traveler_name', '')
    travel_location_name = request.args.get('travel_location_name', '')
    travel_date = request.args.get('travel_date', '')
    if not traveler_name or not travel_location_name or not travel_date:
        return render_template('form.html', t1 = 'traveler_name', t2 = 'travel_location_name', t3 = 'travel_date')
    traveler = person_name2ID_number(traveler_name)
    if traveler is None:
        return 'cannot find this traveler'
    travel_location = location_name2location_number(travel_location_name)
    if travel_location is None:
        return 'cannot find this travel_location'
    insertion = ('''
        INSERT INTO `travel record`(travel_number, traveler, travel_location, travel_date) VALUES
        (0, %s, %s, %s);
        ''')
    cursor.execute(insertion, (traveler, travel_location, travel_date))
    cnx.commit()
    return 'insert into travel record (?, %d, %d, %s) successfully' % (traveler, travel_location, travel_date)

@app.route('/update6') #add a test record
def update6():
    test_result = request.args.get('test_result', '')
    test_datetime = request.args.get('test_datetime', '')
    tested_person_name = request.args.get('tested_person_name', '')
    test_site_name = request.args.get('test_site_name', '')
    if test_result != 'Positive' and test_result != 'Negative' or not test_datetime or not tested_person_name or not test_site_name:
        return render_template('form.html', t1 = 'test_result', t2 = 'test_datetime', t3 = 'tested_person_name', t4 = 'test_site_name')
    test_result = str(int(test_result == 'Positive'))
    tested_person = person_name2ID_number(tested_person_name)
    if tested_person is None:
        return 'cannot find this tested_person'
    test_site = test_site_name2test_site_number(test_site_name)
    if test_site is None:
        return 'cannot find this test_site'
    insertion = ('''
        INSERT INTO `test record`(test_number, test_result, test_datetime, tested_person, test_site) VALUES
        (0, b%s, %s, %s, %s);
        ''')
    cursor.execute(insertion, (test_result, test_datetime, tested_person, test_site))
    cnx.commit()
    return 'insert into test record (?, b\'%s\', %s, %d, %d) successfully' % (test_result, test_datetime, tested_person, test_site)

@app.route('/query1') #query the risk level of a location
def query1():
    location_name = request.args.get('location_name', '')
    if not location_name:
        return render_template('form.html', t1 = 'location_name')
    query = ('''
        SELECT risk_level FROM location
        WHERE `location_name` = %s
        ''')
    cursor.execute(query, (location_name,))
    for risk_level, in cursor:
        return 'The risk level of {} is {}'.format(location_name, risk_level)
    return 'The queried location cannot be found!!!'
