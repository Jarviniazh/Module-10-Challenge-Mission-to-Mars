from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection, mars_app is the database name
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app_ch"
mongo = PyMongo(app)

# set up app route
@app.route("/")
def index():
   # mars is the collection of database
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Set scraping route, just a button on index page
@app.route("/scrape")
def scrape():
   # Create a new variable to access the database 
   mars = mongo.db.mars # Access the database
   # Create a new variable to access the scrape script and hold the newly scraped data
   mars_data = scraping.scrape_all() 
   # Update the new data to the database, upsert=update if exist or insert if first time
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   # Redirect to index page
   return redirect('/', code=302) #302 means redirect

if __name__ == "__main__":
   app.run(debug=True)