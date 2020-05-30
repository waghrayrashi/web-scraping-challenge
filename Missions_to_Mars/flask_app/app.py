# MongoDB and Flask Application
# Dependencies and Setup
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# Flask Setup
app = Flask(__name__)

# Setup PyMongo Connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create the Flask Routes
# Root Route to Query MongoDB 
# Pass the Mars data Into HTML Template: index.html to Display Data
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape Route to import `scrape_mars.py` code & call the `scrape` Function
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successfully Completed"

# Define Main Behavior
if __name__ == "__main__":
    app.run()