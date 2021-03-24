
# Import all needed libraries
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database setup
# create engine to hawaii.sqlite
database_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def home():
    """List of all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitaion():
    
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    all_prcp = []
    for date, prcp, in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)




@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    
    results = session.query(Station.name, Station.id, Station.station).all()
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').all()
    session.close()

    return jsonify(results)



@app.route("/api/v1.0/<start>")
def min(start):


    session = Session(engine)

    first = session.query(Measurement).order_by(Measurement.date.asc()).first()
 
    session.close()

    lowest = session.query(Measurement.tobs, Measurement.date, func.min(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').all()
    session.close()

    lowest = [{"Date": lowest[0][1], "Minimum": lowest[0][0]}]


    avg = session.query(Measurement.tobs, Measurement.date, func.avg(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').all()
    session.close()

    avg = [{"Dates": "2010-01-01 and after", "Average": avg[0][2]}]
    

    max = session.query(Measurement.tobs, Measurement.date, func.max(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').all()
    session.close()

    max = [{"Date": max[0][1], "Maximum": max[0][0]}]
    
    return jsonify(lowest,avg,max)

@app.route("/api/v1.0/<start>/<end>")
def minmax(start,end):


    session = Session(engine)

    lastyear = session.query(Measurement).order_by(Measurement.date.desc()).first()
    session.close()
   

    min2 = session.query(Measurement.tobs, Measurement.date, func.min(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= '2017-08-23').all()
    session.close()

    min2 = [{"Date": min2[0][1], "Minimum": min2[0][0]}]

    avg2 = session.query(Measurement.tobs, Measurement.date, func.avg(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= '2017-08-23').all()
    session.close()

    avg2 = [{"Dates": "2010-01-01 to 2017-08-23", "Average": avg2[0][2]}]

    max2 = session.query(Measurement.tobs, Measurement.date, func.max(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= '2017-08-23').all()
    session.close()

    max2 = [{"Date": max2[0][1], "Maximum": max2[0][0]}]

    return jsonify(min2,avg2,max2)


    
if __name__ == "__main__":
    app.run(debug=True)