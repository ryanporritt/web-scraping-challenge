# Dependencies and Setup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask Setup
app = Flask(__name__)

# PyMongo Connection Setup
mongo = PyMongo(app, uri="mongodb://localhost:27017/missions_to_mars")

# Flask Routes
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("testindex.html", mars=mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_all()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

# Define Main Behavior
if __name__ == "__main__":
    app.run()