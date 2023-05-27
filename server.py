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

def test_site_number2test_site_name(test_site_number):
    query = ('''
        SELECT test_site_name FROM `testing sites`
        WHERE test_site_number = %s
        ''')
    cursor.execute(query, (test_site_number,))
    res = None
    for x, in cursor:
        res = x
    return res

def ID_number2person_name(ID_number):
    query = ('''
        SELECT person_name FROM person
        WHERE ID_number = %s
        ''')
    cursor.execute(query, (ID_number,))
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
    <br>
    <a href="/query2"> query the locations a person has been to between date A and date B </a>
    <br>
    <a href="/query3"> query all the persons that have been to a particular location and the dates </a>
    <br>
    <a href="/query4"> query all the test records of a person </a>
    <br>
    <a href="/query5"> query the most recent positive record of the person </a>
    <br>
    <a href="/query6"> query all the positive records in the test site </a>
    <br>
    <a href="/query7"> query all the positive records after some time </a>
    <br>
    <a href="/query8"> query all people who have traveled to dangerous places after some day but have not been tested after some time </a>
    <br>
    <a href="/query9"> query the fastest ten people belonged to the advisor who have been tested in some day </a>
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

@app.route('/query2') #query the locations a person has been to between date A and date B
def query2():
    person_name = request.args.get('person_name', '')
    dateA = request.args.get('dateA', '')
    dateB = request.args.get('dateB', '')
    if not person_name or not dateA or not dateB:
        return render_template('form.html', t1 = 'person_name', t2 = 'dateA', t3 = 'dateB')
    ID_number = person_name2ID_number(person_name)
    if ID_number is None:
        return 'cannot find this person!!!'
    query = ('''
        SELECT DISTINCT B.location_name FROM `travel record` as A, location as B
        WHERE (A.travel_date BETWEEN %s and %s) and A.travel_location = B.location_number and A.traveler = %s
        ''')
    cursor.execute(query, (dateA, dateB, ID_number,))
    ret = ''
    for location_name, in cursor:
        ret += location_name + '\n<br>\n'
    if not ret:
        return 'None'
    return ret

@app.route('/query3') #query all the persons that have been to a particular location and the dates
def query3():
    location_name = request.args.get('location_name', '')
    if not location_name:
        return render_template('form.html', t1 = 'location_name')
    location_number = location_name2location_number(location_name)
    if location_number is None:
        return 'cannot find this location!!!'
    query = ('''
        SELECT B.person_name, A.travel_date FROM `travel record` as A, person as B
        WHERE A.traveler = B.ID_number and A.travel_location = %s
        ''')
    cursor.execute(query, (location_number,))
    ret = ''
    for traveler_name, travel_date in cursor:
        ret += traveler_name + ' ' + str(travel_date) + '\n<br>\n'
    if not ret:
        return 'None'
    return ret

@app.route('/query4') #query all the test records of a person
def query4():
    tested_person_name = request.args.get('tested_person_name', '')
    if not tested_person_name:
        return render_template('form.html', t1 = 'tested_person_name')
    tested_person = person_name2ID_number(tested_person_name)
    if tested_person is None:
        return 'cannot find this person!!!'
    query = ('''
        SELECT A.test_result, A.test_datetime, B.test_site_name FROM `test record` as A, `testing sites` as B
        WHERE A.tested_person = %s and A.test_site = B.test_site_number
        ''')
    cursor.execute(query, (tested_person,))
    dict = {'0': 'Negative', '1': 'Positive'}
    ret = ''
    for test_result, test_datetime, test_site_name in cursor:
        ret += dict[str(test_result)] + ' ' + str(test_datetime) + ' ' + test_site_name + '\n<br>\n'
    if not ret:
        return 'None'
    return ret

@app.route('/query5') #query the most recent positive record of the person
def query5():
    person_name = request.args.get('person_name', '')
    if not person_name:
        return render_template('form.html', t1 = 'person_name')
    person_id=person_name2ID_number(person_name)
    query = ('''
        SELECT test_result,test_datetime,test_site FROM `test record`
        WHERE `tested_person` = %s and test_datetime>=all(
        SELECT test_datetime FROM `test record`
        WHERE `tested_person` = %s
        )
        ''')
    cursor.execute(query, (person_id,person_id))
    for test_result,test_datetime,test_site in cursor:
        if test_result:
            return '{} tested positive most recently in test site {} on {}'.format(person_name, test_site_number2test_site_name(test_site),test_datetime)
        else:
            return '{} tested negative most recently in test site {} on {}'.format(person_name, test_site_number2test_site_name(test_site),test_datetime)
    return 'The queried test record cannot be found!!!'


@app.route('/query6') #query all the positive records in the test site
def query6():
    test_site_name = request.args.get('test_site_name', '')
    if not test_site_name:
        return render_template('form.html', t1 = 'test_site_name')
    test_site_number=test_site_name2test_site_number(test_site_name)
    query = ('''
        SELECT test_datetime,tested_person FROM `test record`
        WHERE `test_site` = %s and test_result = 1
        ''')
    cursor.execute(query, (test_site_number,))
    res=''
    for test_datetime,tested_person in cursor.fetchall():
        res+='{} tested positive in test site {} on {} <br>'.format(ID_number2person_name(tested_person), test_site_name, test_datetime)
    if not res:
        return 'The queried test record cannot be found!!!'
    return res

@app.route('/query7') #query all the positive records after some time
def query7():
    test_datetime = request.args.get('test_datetime', '')
    if not test_datetime:
        return render_template('form.html', t1 = 'test_datetime')
    query = ('''
        SELECT tested_person,test_site,test_datetime FROM `test record`
        WHERE `test_datetime`>= %s and test_result = 1
        ''')
    cursor.execute(query, (test_datetime,))
    res=''
    for tested_person,test_site,t_datetime in cursor.fetchall():
        res+='{} tested positive in test site {} on {} <br>'.format(ID_number2person_name(tested_person), test_site_number2test_site_name(test_site), t_datetime)
    if not res:
        return 'The queried test record cannot be found!!!'
    return res

@app.route('/query8') #query all people who have traveled to dangerous places after some day but have not been tested after some time
def query8():
    risk_level = request.args.get('risk_level', '')
    travel_date=request.args.get('travel_date','')
    test_datetime = request.args.get('test_datetime','')
    if not test_datetime or not risk_level or not travel_date:
        return render_template('form.html', t1='risk_level', t2='travel_date', t3 = 'test_datetime')
    if risk_level=='low':
        query = ('''
            SELECT traveler FROM `travel record`
            WHERE `travel_date` >= %s
            EXCEPT
            SELECT tested_person FROM `test record`
            WHERE  `test_datetime` >= %s
            ''')
    elif risk_level=='medium':
        query = ('''
            SELECT traveler FROM `travel record`
            WHERE `travel_date` >= %s and `travel_location` not in (SELECT `location_number` FROM `location` WHERE risk_level='low')
            EXCEPT
            SELECT tested_person FROM `test record`
            WHERE  `test_datetime` >= %s
            ''')
    elif risk_level=='high':
        query = ('''
            SELECT traveler FROM `travel record`
            WHERE `travel_date` >= %s and `travel_location` in (SELECT `location_number` FROM `location` WHERE risk_level='high')
            EXCEPT
            SELECT tested_person FROM `test record`
            WHERE  `test_datetime` >= %s
            ''')
    else:
        return 'the risk level of a location must be low, medium or high'
    cursor.execute(query, (travel_date,test_datetime))
    res=''
    for tested_person, in cursor.fetchall():
        res+='{}, '.format(ID_number2person_name(tested_person))
    if not res:
        return 'The queried person cannot be found!!!'
    return res[:-2]+' have traveled to dangerous places after {} but have not been tested after {}'.format(travel_date,test_datetime)


@app.route('/query9') #query the fastest ten people belonged to the advisor who have been tested in some day
def query9():
    test_date = request.args.get('test_date', '')
    advisor_name=request.args.get('advisor_name','')
    if not test_date or not advisor_name:
        return render_template('form.html', t1 = 'test_date',t2='advisor_name')
    advisor_id=person_name2ID_number(advisor_name)
    query = ('''
        SELECT tested_person,test_site,test_datetime FROM `test record`
        WHERE DATE(`test_datetime`)=%s and tested_person in (SELECT ID_number FROM `person` WHERE advisor=%s) 
        ORDER BY test_datetime asc
        ''')
    cursor.execute(query, (test_date,advisor_id))
    res=''
    count=0
    for tested_person,test_site,t_datetime in cursor.fetchall():
        count+=1
        if count==11:
            break
        res+='{} has been tested in test site {} on {} <br>'.format(ID_number2person_name(tested_person), test_site_number2test_site_name(test_site), t_datetime)
    if not res:
        return 'The queried person cannot be found!!!'
    return res
