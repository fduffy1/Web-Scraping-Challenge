from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app,uri ="mongodb://localhost:27017/mars_db")

@app.route("/")
def index():
    data = mongo.db.scrape.find_one()
    return render_template("index.html",mars=data)

@app.route("/scrape")
def scrape_page():
    data = scrape_mars.scrape()
    mongo.db.scrape.update({},data,upsert = True)
    return redirect("/")

if __name__ == "__main__":
    app.run()