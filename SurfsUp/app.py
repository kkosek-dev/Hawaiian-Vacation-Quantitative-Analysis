# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import datetime as dt
import numpy as np
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/karso/OneDrive/Desktop/Past Challenges/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return ( f"""
            <!DOCTYPE html>
            <html lang="en">
            
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Hawaii Climate API</title>
            </head>
           
            <body>
                <strong> <h2> Welcome to the Hawaii Climate API!</h2> </strong> 
                <br/>
                    Available Routes:
                <br/>
                <a href="http://127.0.0.1:5000/api/v1.0/precipitation">
                    /api/v1.0/precipitation</a>
                <br/>
                <a href="http://127.0.0.1:5000/api/v1.0/stations">
                    /api/v1.0/stations</a>
                <br/>
                <a href="http://127.0.0.1:5000/api/v1.0/tobs">
                    /api/v1.0/tobs</a>
                <br/>
                <strong> Search by Start to 2017-08-23 range: /start_date</strong>
                <br/>
                    /api/v1.0/YYYY-mm-dd
                <br/>
                <strong>Search by Start and End date range: /start_date/end_date</strong>
                <br/>
                    /api/v1.0/YYYY-mm-dd/YYYY-mm-dd
                <br/>
            </body>
    """ )

@app.route("/api/v1.0/precipitation")
def precipitation():
    date = dt.datetime(2016, 8, 22)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date).all()
    all_results = []
    for date, prcp in results:
        date_dict = {}
        date_dict[date] = prcp
        all_results.append(date_dict)
    return jsonify(all_results)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    all_results = list(np.ravel(results)) 
    return jsonify(all_results)

@app.route("/api/v1.0/tobs")
def tobs():
    date = dt.datetime(2016, 8, 22)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > date).all()
    all_results = list(np.ravel(results))
    return jsonify(all_results)

@app.route("/api/v1.0/<start>")
def startfunctionalitytest(start):
 
    canonicalized = start.replace(" ", "")
    date = dt.datetime.strptime(canonicalized, '%Y-%m-%d')
    
    date_list = session.query(Measurement.date).filter(Measurement.date >= date).all()
    data_list = session.query(np.min(Measurement.tobs),np.max(Measurement.tobs),np.mean(Measurement.tobs)).filter(Measurement.date >= date).all()

    return jsonify( { f"Start Date: {date_list}" : f"(TMIN, TMAX, TAVG): {data_list}"} )

@app.route("/api/v1.0/<start>/<end>")
def endfunctionality(start, end):
    
    canonicalized_start = start.replace(" ", "")
    start_date = dt.datetime.strptime(canonicalized_start, '%Y-%m-%d')
    canonicalized_end = end.replace(" ", "")
    end_date = dt.datetime.strptime(canonicalized_end, '%Y-%m-%d')
    
    date_list = session.query(Measurement.date).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    data_list = session.query(np.min(Measurement.tobs),np.max(Measurement.tobs),np.mean(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    return jsonify({ f"Dates Surveyed: {date_list} " : f"(TMIN, TMAX, TAVG): {data_list}"})

if __name__ == "__main__":
    app.run()
