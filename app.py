from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import next_gen

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/nfl_app"
mongo = PyMongo(app)

rushstats = mongo.db.rushstats
passstats = mongo.db.passstats
recstats = mongo.db.recstats
fantstats= mongo.db.fantstats
schedule = mongo.db.datastats

@app.route("/")
def index():
    stats = mongo.db.stats.find_one()
    return render_template("index.html", stats=stats)


@app.route("/scrape")
def scraper():
    pass_data, rush_data, rec_data, temp_data, schedule_dict = next_gen.scrape()
    passstats.drop()
    rushstats.drop()
    recstats.drop()
    fantstats.drop()
    schedule.drop()
    passstats.insert_many(pass_data)
    rushstats.insert_many(rush_data)
    recstats.insert_many(rec_data)
    fantstats.insert_many(temp_data)
    schedule.insert_many(schedule_dict)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)