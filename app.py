from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import next_gen

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/nfl_app"
mongo = PyMongo(app)

stats = mongo.db.stats

@app.route("/")
def index():
    stats = mongo.db.stats.find_one()
    return render_template("index.html", stats=stats)


@app.route("/scrape")
def scraper():
    stats_data = next_gen.scrape()
    stats.update({}, stats_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)