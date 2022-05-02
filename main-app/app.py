#! /usr/bin/python3

"""
Our application is based on code from the following application:

----

This is an example Flask | Python | Psycopg2 | PostgreSQL
application that connects to the 7dbs database from Chapter 2 of
_Seven Databases in Seven Weeks Second Edition_
by Luc Perkins with Eric Redmond and Jim R. Wilson.
The CSC 315 Virtual Machine is assumed.

John DeGood
degoodj@tcnj.edu
The College of New Jersey
Spring 2020

----

References

Flask documentation:  
https://flask.palletsprojects.com/  

Psycopg documentation:
https://www.psycopg.org/

This example code is derived from:
https://www.postgresqltutorial.com/postgresql-python/
https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
https://www.geeksforgeeks.org/python-using-for-loop-in-flask/
"""

import psycopg2
from config import config
from flask import Flask, render_template, request

# Connect to the PostgreSQL database server
def connect(query):
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall() and obtain column headers
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        rows.insert(0, colnames)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 

# app.py
app = Flask(__name__)


# home page
@app.route("/")
def home():
    return render_template('home.html')


# overall costs page
@app.route("/overall_monthly_cost")
def overall_monthly_cost():
    return render_template('overall-monthly-cost.html')


# meter costs page
@app.route("/meter_monthly_cost")
def meter_monthly_cost():
    return render_template('meter-monthly-cost.html')


# type costs page
@app.route("/type_monthly_cost")
def type_monthly_cost():
    return render_template('type-monthly-cost.html')


# handle overall queries
@app.route('/overall-query-handler', methods=['POST'])
def overall_query_handler():
    
    # set variables
    graph = False
    graphType = ""
    labels = []
    values = []
    title = ""

    # handle choice and set graph data
    if request.form['query_choice'] == "1":
        query = "SELECT * FROM OverallMonthlyCostAvg ORDER BY month;"
        rows = connect(query)
        graph = True
        graphType = "line"
        for row in rows:
            labels.append(row[0])
            values.append(row[1])
        del labels[0]
        del values[0]
        title = "Average Monthly Cost"

    # handle choice
    elif request.form['query_choice'] == "2":
        query = "SELECT * FROM OverallMonthlyCostAvg WHERE averageCost IN (SELECT MAX(averageCost) FROM OverallMonthlyCostAvg);"
        rows = connect(query)
        title = "Most Expensive Month"

    # handle choice
    elif request.form['query_choice'] == "3":
        query = "SELECT * FROM OverallMonthlyCostAvg WHERE averageCost IN (SELECT MIN(averageCost) FROM OverallMonthlyCostAvg);"
        rows = connect(query)
        title = "Least Expensive Month"

    # in case something fails
    else:
        return render_template('overall-monthly-cost.html')

    # get headers
    headers = rows[0]
    del rows[0]

    # return web page
    return render_template('overall-monthly-cost.html', rows=rows, graph=graph, graphType=graphType, labels=labels, values=values, title=title, headers=headers)


@app.route('/meter-query-handler', methods=['POST'])
def meter_query_handler():
    # set variables
    graph = False
    graphType = ""
    labels = []
    values = []
    title = ""

    # handle choice and set graph data
    if request.form['query_choice'] == "1":
        query = "SELECT * FROM MeterMonthlyCostAvg WHERE meterName = \'?\' ORDER BY month;"
        query = query.replace('?', request.form['meter'])
        rows = connect(query)
        graph = True
        graphType = "line"
        for row in rows:
            labels.append(row[3])
            values.append(row[5])
        del labels[0]
        del values[0]
        title = "Average Cost of each Month for " + request.form['meter']

    # handle choice
    elif request.form['query_choice'] == "2":
        query = "SELECT * FROM MeterMonthlyCostAvg WHERE month = \'?\' ORDER BY meterName;"
        query = query.replace('?', request.form['month'])
        rows = connect(query)
        title = "Average Cost of Each Meter in Month #" + request.form['month']

    # handle choice
    elif request.form['query_choice'] == "3":
        query = "SELECT meterName, AVG(averageCost)::numeric(10,2) FROM MeterMonthlyCostAvg GROUP BY meterName ORDER BY meterName;"
        rows = connect(query)
        title = "Average Monthly Cost"

    # handle choice
    elif request.form['query_choice'] == "4":
        query = "SELECT meterName, meterType, month, averageCost FROM MeterMonthlyCostAvg WHERE averagecost IN (SELECT MAX(averageCost) FROM MeterMonthlyCostAvg GROUP BY meterName) ORDER BY meterName;"
        rows = connect(query)
        title = "Most Expensive Month for Each Meter"

    # handle choice
    elif request.form['query_choice'] == "5":
        query = "SELECT meterName, meterType, month, averageCost FROM MeterMonthlyCostAvg WHERE averagecost IN (SELECT MIN(averageCost) FROM MeterMonthlyCostAvg GROUP BY meterName) ORDER BY meterName;"
        rows = connect(query)
        title = "Least Expensive Month for Each Meter"
    
    # in case something goes wrong
    else:
        return render_template('meter-monthly-cost.html')

    # get headers
    headers = rows[0]
    del rows[0]

    # return web page
    return render_template('meter-monthly-cost.html', rows=rows, graph=graph, graphType=graphType, labels=labels, values=values, title=title, headers=headers)


@app.route('/type-query-handler', methods=['POST'])
def type_query_handler():
    
    # set variables
    graph = False
    graphType = ""
    labels = []
    values = []
    title = ""

    # handle choice and set graph data
    if request.form['query_choice'] == "1":
        if request.form['type'] == "Other":
            query = "SELECT meterType, month, averageUsage FROM TypeMonthlyCostAvg WHERE meterType = \'Other\' ORDER BY month;"
            rows = connect(query)
            for row in rows:
                labels.append(row[1])
                values.append(row[2])
            del labels[0]
            del values[0]
        else:
            query = "SELECT * FROM TypeMonthlyCostAvg WHERE meterType = \'?\' ORDER BY month;"
            query = query.replace('?', request.form['type'])
            rows = connect(query)
            for row in rows:
                labels.append(row[1])
                values.append(row[3])
            del labels[0]
            del values[0]
        graph = True
        graphType = "line"
        title = "Average Cost of each Month for " + request.form['type']

    # handle choice and set graph data
    elif request.form['query_choice'] == "2":
        query = "SELECT * FROM TypeMonthlyCostAvg WHERE month = \'?\' ORDER BY meterType;"
        query = query.replace('?', request.form['month'])
        rows = connect(query)
        graph = True
        graphType = "bar"
        for row in rows:
            if not (row[0] == "Other"):
                labels.append(row[0])
                values.append(row[3])
        del labels[0]
        del values[0]
        title = "Average Cost of Each Type in Month #" + request.form['month']

    # handle choice and set graph data
    elif request.form['query_choice'] == "3":
        query = "SELECT meterType, AVG(averageCost)::numeric(10,2) FROM TypeMonthlyCostAvg GROUP BY meterType;"
        rows = connect(query)
        graph = True
        graphType = "bar"
        for row in rows:
            if not (row[0] == "Other"):
                labels.append(row[0])
                values.append(row[1])
        del labels[0]
        del values[0]
        title = "Average Monthly Cost"

    # handle choice
    elif request.form['query_choice'] == "4":
        query = " SELECT meterType, month, averageCost FROM TypeMonthlyCostAvg WHERE averagecost IN (SELECT MAX(averageCost) FROM TypeMonthlyCostAvg GROUP BY meterType) ORDER BY meterType;"
        rows = connect(query)
        title = "Most Expensive Month for Each Type"

    # handle choice
    elif request.form['query_choice'] == "5":
        query = "SELECT meterType, month, averageCost FROM TypeMonthlyCostAvg WHERE averagecost IN (SELECT MIN(averageCost) FROM TypeMonthlyCostAvg GROUP BY meterType) ORDER BY meterType;"
        rows = connect(query)
        title = "Least Expensive Month for Each Type"

    # in case something goes wrong
    else:
        return render_template('type-monthly-cost.html')

    # get headers
    headers = rows[0]
    del rows[0]

    # return web page
    return render_template('type-monthly-cost.html', rows=rows, graph=graph, graphType=graphType, labels=labels, values=values, title=title, headers=headers)


# run application
if __name__ == '__main__':
    app.run(debug = True)
