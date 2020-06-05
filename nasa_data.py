from flask import Flask, jsonify, render_template

#import python database toolkit
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import numpy as np
import scrape_mars
import pymongo
###################

conn = 'mongodb://localhost:27018'
client = pymongo.MongoClient(conn)
db = client.marsDB
collection = db.mars_data

#Create an app, being sure to pass __name__
app = Flask(__name__)

#
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    data = collection.find_one()
    #print(scrape_mars.scrape())
        #   title = x['news_title']
     #   image_url = x['featured_image_url']
      #  weather = x['mars_weather']
       # facts = x['mars_facts']
       # images = x['image_urls']
    

    #data_list = [news_p, title, image_url, weather, facts, images]
    return(
        render_template("index.html", data= data) 
    )

@app.route("/scrape")
def scrape_data():
    print("Server received request to scrape data...")
    string = scrape_mars.scrape()
    #title=string.get('news_title')
    #news = string.get('news_p')
    #collection.insert_one(string)
    collection.update({}, string, upsert=True)
    print(string['image_urls'][0]['img_url'])
    home()
    return 'Scrape completed. Reload the previous page to see the updated Mars information'
     #   'this is a test'
	#)


if __name__ == "__main__":
    app.run(debug=True)

