# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask, render_template, request, redirect
import os
from datetime import datetime
from google.cloud import datastore
from google.cloud import storage

CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("homepage.html")

@app.route("/about", methods=["GET","POST"])
def redirAbout():
    # Redirect to the about page.
    return render_template("/about.html")

@app.route("/home", methods=["GET","POST"])
def redirHomepage():
    # Redirect to the home page.
    return render_template("/homepage.html")

@app.route("/library", methods=["GET","POST"])
def redirLibrary():
    # Redirect to the library page.
    return render_template("/library.html")

@app.route("/signup", methods=["GET","POST"])
def redirSignup():
    # Redirect to the signup page.
    return render_template("/signup.html")

@app.route("/home", methods=["GET","POST"])
def redirHome():
    # Redirect to the signup page.
    return render_template("/homepage.html")

@app.route("/submission", methods=["GET","POST"])
def redirSubmission():
    # Redirect to the signup page.
    return render_template("/submission.html")    

@app.route('/registration', methods=["GET","POST"])
def register():
    """Process user registation"""
    name = request.form.get("name")
    year = request.form.get("year")
    author = request.form.get("author")
    genre = request.form.get("genre")
    relig = request.form.get("relig")

    if not name:
        return render_template("comic_failure.html", userMissing="your name.")
    if not year:
        return render_template("comic_failure.html", userMissing="the year the comic was published.")
    if not author:
        return render_template("comic_failure.html", userMissing="the author.")
    if not genre:
        return render_template("comic_failure.html", userMissing="the genre of the comic.")
    if not relig:
        return render_template("comic_failure.html", userMissing="the religicious component of the comic.")
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    # The kind for the new entity.
    kind = "comics"
    # The name/ID for the new entity.
    regname = name
    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, regname)

    # Construct the new entity using the key. Set dictionary values for entity
    # registrant name and sports
    entity = datastore.Entity(key)
    entity["reg_name"] = name
    entity["reg_year"] = year
    entity["reg_author"] = author
    entity["reg_genre"] = genre
    entity["reg_relig"] = relig


    # Save the new entity to Datastore.
    datastore_client.put(entity)

    # Redirect to the registrants page.
    return redirect("/comic_registrants")

@app.route("/comic_registrants")
def comicRegistrants():
     # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Use the Cloud Datastore client to fetch information from Datastore about
    # each registrant.
    query = datastore_client.query(kind="comics")
    comic_registrants = list(query.fetch())
    return render_template("comic_registrants.html", comic_registrants=comic_registrants)

@app.route("/show", methods=["GET","POST"])
def redirShow():
    # Redirect to the registrants page.
    return redirect("/comic_registrants")

@app.route("/filter", methods=["GET","POST"])
def filterComics():
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    flter = request.form.get("filter")
    attribute = request.form.get("attribute")

    query = datastore_client.query(kind="comics")
    query = query.add_filter(attribute, "=", flter)
    comic_registrants = list(query.fetch())
    return render_template("comic_registrants.html", comic_registrants=comic_registrants)

@app.route("/delete", methods=["GET","POST"])
def delete():
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    delete = request.form.get("delete")

    # The kind for the new entity.
    #kind = "comics"
    # The name/ID for the new entity.
    #regname = delete
    # Create the Cloud Datastore key for the new entity.
    #key = datastore_client.key(kind, regname)
    #entity = datastore.Entity(key)
    #entity["reg_delete"] = delete
    
    query = datastore_client.query(kind="comics")
    name = "reg_name"
    query = query.add_filter(name, "=", delete)
    comic_registrants = list(query.fetch())
    for comic in comic_registrants:
            key = comic.key
            datastore_client.delete(key)
    return redirect("/comic_registrants")

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
