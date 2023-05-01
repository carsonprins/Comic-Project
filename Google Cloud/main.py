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
from flask import Flask, render_template, request, redirect, send_from_directory
import os
import shutil
from datetime import datetime
from google.cloud import datastore
from google.cloud import storage
from google.cloud.datastore import query as datastore_query
#from werkzeug.utils import secure_filename

CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

GENRES = [
    "Horror",
    "Superhero",
    "Crime",
    "Romance",
    "War",
    "Comedy",
    "Fantasy",
    "Western",
    "Mystery",
    "History",
    "Drama",
    "Science Fiction",
    "Nonfiction"
]

RELATIONS = [
    "Character reflects a person/deity from sacred text",
    "Story plot in comic reflects a plot in a sacred text",
    "Act from a sacred text is in the comic",
    "Scripture was quoted in comic",
    "Objects representing sacred text are present",
    "A person/deity from a sacred text is present",
    "A name of a person/deity in a sacred text is referred to",
    "A comic cover symbolizing a sacred text"
]
@app.route('/')
def index():
    datastore_client = datastore.Client()
    query = datastore_client.query(kind="comic")
    comic_registrants = list(query.fetch())
    return render_template("/homepage.html", comic_registrants=comic_registrants)

@app.route("/about", methods=["GET","POST"])
def redirAbout():
    # Redirect to the about page.
    return render_template("/about.html")

@app.route("/home", methods=["GET","POST"])
def redirHomepage():
    # Redirect to the home page.
    datastore_client = datastore.Client()
    query = datastore_client.query(kind="comic")
    comic_registrants = list(query.fetch())
    return render_template("/homepage.html", comic_registrants=comic_registrants)

@app.route("/library", methods=["GET","POST"])
def redirLibrary():
    # Redirect to the library page.
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Use the Cloud Datastore client to fetch information from Datastore about
    # each registrant.
    query = datastore_client.query(kind="comic")
    comic_registrants = list(query.fetch())
    return render_template("/library.html", comic_registrants=comic_registrants)

@app.route("/comic_template", methods=["GET","POST"])
def redirTemplate():
    # Redirect to the template page.
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    attribute = "reg_title"
    comic_name=request.args.get("comic_name")
    query = datastore_client.query(kind="comic")
    query.add_filter(attribute, "=", comic_name)

    # Use the Cloud Datastore client to fetch information from Datastore about
    # each registrant.

    comic_registrants = list(query.fetch())
    return render_template("/comic_template.html", comic_registrants=comic_registrants, read_comic = comic_name)

@app.route("/signup", methods=["GET","POST"])
def redirSignup():
    # Redirect to the signup page.
    return render_template("/signup.html")

@app.route("/login", methods=["GET","POST"])
def redirLogin():
    # Redirect to the login page.
    return render_template("/login.html")

@app.route("/home", methods=["GET","POST"])
def redirHome():
    # Redirect to the signup page.
    return render_template("/homepage.html")

@app.route("/submission", methods=["GET","POST"])
def redirSubmission():
    # Redirect to the signup page.
    return render_template("/submission.html", genres=GENRES, relations=RELATIONS)    

@app.route('/reg_submission', methods=["GET","POST"])
def register():
    """Process user registation"""
    file = request.files['image']
    #move the file to static folder
    filename = file.filename
    file.save('static/' + filename)
    title = request.form.get("title")
    alttitle = request.form.get("alttitle")
    issue = request.form.get("issue")
    issuenum = request.form.get("issuenum")
    volume = request.form.get("volume")
    pubyear = request.form.get("pubyear")
    seriesyear = request.form.get("seriesyear")
    publisher = request.form.get("publisher")
    author = request.form.get("author")
    artist = request.form.get("artist")
    inker = request.form.get("inker")
    colorist = request.form.get("colorist")
    letterer = request.form.get("letterer")
    genre = request.form.getlist("genre")
    otherInput = request.form.get("otherInput")
    mainChar = request.form.get("mainChar")
    when = request.form.get("when")
    where = request.form.get("where")
    summary = request.form.get("summary")
    warning = request.form.get("warning")
    sacredtext = request.form.get("sacredtext")
    relation = request.form.getlist("relation")
    otherInput2 = request.form.get("otherInput2")
    referfile = request.form.get("referfile")
    entry = request.form.get("entry")
    contributors = request.form.get("contributors")
    externallinks = request.form.get("externallinks")

    
    

    if not filename:
        return render_template("comic_failure.html", userMissing="a file.")
    if not title:
        return render_template("comic_failure.html", userMissing="the year the comic was published.")
    if not pubyear:
        return render_template("comic_failure.html", userMissing="the year the comic was published.")
    if not publisher:
        return render_template("comic_failure.html", userMissing="the religious component of the comic.")
    if not sacredtext:
        return render_template("comic_failure.html", userMissing="the religious component of the comic.")
    if not entry:
        return render_template("comic_failure.html", userMissing="the religious component of the comic.")
    
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    # The kind for the new entity.
    kind = "comic"
    # The name/ID for the new entity.
    regname = title
    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, regname)

    # Construct the new entity using the key. Set dictionary values for entity
    entity = datastore.Entity(key)
    entity["reg_image"] = filename
    entity["reg_title"] = title
    entity["reg_alttitle"] = alttitle
    entity["reg_issue"] = issue
    entity["reg_issuenum"] = issuenum
    entity["reg_volume"] = volume
    entity["reg_pubyear"] = pubyear
    entity["reg_seriesyear"] = seriesyear
    entity["reg_publisher"] = publisher
    entity["reg_author"] = author
    entity["reg_artist"] = artist
    entity["reg_inker"] = inker
    entity["reg_colorist"] = colorist
    entity["reg_letterer"] = letterer
    genre = str(genre).strip('[]')
    entity["reg_genre"] = genre
    entity["reg_otherInput"] = otherInput
    entity["reg_mainChar"] = mainChar
    entity["reg_when"] = when
    entity["reg_where"] = where
    entity["reg_summary"] = summary
    entity["reg_warning"] = warning
    entity["reg_sacredtext"] = sacredtext
    relation = str(relation).strip('[]')
    entity["reg_relation"] = relation
    entity["reg_otherInput2"] = otherInput2
    entity["reg_referfile"] = referfile
    entity["reg_entry"] = entry
    entity["reg_contributors"] = contributors
    entity["reg_externallinks"] = externallinks

    # Save the new entity to Datastore.
    datastore_client.put(entity)

    return redirect("/library")
    
@app.route("/filter", methods=["GET", "POST"])
def filterComics():
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    search = request.form.get("search")
    attribute = "reg_title"

    # Query for entities that contain the substring in reg_title
    query = datastore_client.query(kind="comic")
    query.add_filter(attribute, "=", search)

    comic_registrants = list(query.fetch())
    return render_template("/homepage.html", comic_registrants=comic_registrants)

@app.route("/filterLib", methods=["GET","POST"])
def filterLibrary():
    #Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    search = request.form.get("search")
    attribute = "reg_title"
    query = datastore_client.query(kind="comic")
    query.add_filter(attribute, "=", search)
    comic_registrants = list(query.fetch())
    return render_template("/library.html", comic_registrants=comic_registrants)

@app.route("/delete", methods=["GET","POST"])
def delete():
    #Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    delete = request.form.get("delete")

    query = datastore_client.query(kind="comic")
    name = "reg_title"
    query = query.add_filter(name, "=", delete)
    comic_registrants = list(query.fetch())
    for comic in comic_registrants:
            key = comic.key
            datastore_client.delete(key)
    return redirect("/library")

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]

import hashlib

@app.route('/reg_signup', methods=["GET","POST"])
def registerSignup():
    email = request.form.get("email")
    pwd = request.form.get("pwd").encode('utf-8')  # Convert password to bytes.

    # Hash the password using SHA-256.
    hashed_pwd = hashlib.sha256(pwd).hexdigest()

    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # The kind for the new entity.
    kind = "account"

    # The name/ID for the new entity.
    regname = email

    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, regname)

    # Create the entity and set the properties.
    entity = datastore.Entity(key)
    entity["reg_email"] = email
    entity["reg_pwd"] = hashed_pwd

    # Save the new entity to Datastore.
    datastore_client.put(entity)

    return redirect("/home")

@app.route('/reg_login', methods=["GET","POST"])
def login():
    email = request.form.get("email")
    pwd = request.form.get("pwd").encode('utf-8')  # Convert password to bytes.

    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # The kind for the entity.
    kind = "account"

    # The name/ID for the entity.
    regname = email

    # Create the Cloud Datastore key for the entity.
    key = datastore_client.key(kind, regname)

    # Get the entity from Datastore.
    entity = datastore_client.get(key)

    if entity:
        # Hash the entered password using SHA-256.
        hashed_pwd = hashlib.sha256(pwd).hexdigest()

        if hashed_pwd == entity["reg_pwd"]:
            # Passwords match, redirect to home page.
            return redirect("/home")
        else:
            # Passwords do not match, display error message.
            return "Invalid email or password"
    else:
        # Account not found, display error message.
        return "Invalid email or password"
