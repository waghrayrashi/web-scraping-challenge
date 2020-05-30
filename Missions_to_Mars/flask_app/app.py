# MongoDB and Flask Application
# Dependencies and Setup
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# Flask Setup
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create the Flask Routes
# Root Route to Query MongoDB 
# Pass the Mars data Into HTML Template: index.html to Display Data
@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", mars=mars)

# Scrape Route to import `scrape_mars.py` code & call the `scrape` Function
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    # Run the scrape function
    mars_data = scrape_mars.scrape_all()
    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)
    # Redirect back to home page
    # return redirect("/")
    
    return "Scraping Completed Successfully"

# Define main behavior
if __name__ == "__main__":
    app.run()