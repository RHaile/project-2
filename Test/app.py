import os

import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/movie_data.sqlite"
db = SQLAlchemy(app)

class Movie_data(db.Model):
    __tablename__ = 'movie_data'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String)
    production_company = db.Column(db.String)
    director = db.Column(db.String)
    budget = db.Column(db.Integer)
    overview = db.Column(db.String)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.DateTime)
    revenue = db.Column(db.Integer)
    runtime = db.Column(db.Integer)
    status = db.Column(db.String)
    tagline = db.Column(db.String)
    title = db.Column(db.String)
    vote_average = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    profit = db.Column(db.Integer)

    def __repr__(self):
        return '<Movie_data %r>' % (self.name)

@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/factor_names")
def factor_names():
    """Return a list of factor names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Movie_data.runtime, Movie_data.vote_average, Movie_data.budget).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (factor names)
    return jsonify(list(df.columns)[0:])


@app.route("/factors/<factor>")
def factors(factor):
    """Return column name"""
    stmt = db.session.query(Movie_data.runtime, Movie_data.vote_average, Movie_data.budget).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1

    results = db.session.query(Movie_data.runtime, Movie_data.profit, Movie_data.budget, Movie_data.vote_average, Movie_data.title, Movie_data.genre, Movie_data.revevnue).all()
    df_r = read_sql_query(results, db.session.bind)

    df_results = df_r.loc[df[factor] > 1, ["factor", "profit", factor]]

    # Format the data to send as json
    data = {
        "runtimes": df_results.runtime.values.tolist(),
        "profits": df_results.profit.values.tolist(),
        "budgets": df_results.budget.values.tolist(),
        "ratings": df_results.vote_average.values.tolist(),
        "titles": df_results.title.values.tolist(),
        "genres": df_results.genre.values.tolist(),
        "revenues": df_results.revenue.values.tolist(),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
