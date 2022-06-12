from flask import Flask, render_template, request, session, redirect, url_for, abort
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
from pip._vendor import cachecontrol
import requests
import os
import pathlib
import uuid
import pymongo
from pymongo import MongoClient

app = Flask('app')
app.config['SESSION_TYPE'] = 's e c r e t'
app.secret_key = 's e c r e t'

cluster = pymongo.MongoClient("mongodb+srv://timotea:1234@cluster0.qfjdm.mongodb.net/?retryWrites=true&w=majority")
db = cluster["Posts"]
collection = db["Posts"]


#geocoding header
headers = {
        'apiKey': "NjgyOWM2MjA4NGRiNGRhOTgxODQ1NjgxNGVkMGJkMmQ6NmM4ZDY5NjAtYjVmNS00M2VlLWIxZGUtZGYwZGNmNTgyZjk1"
    }
#allow oauth without secure website
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

#important information for google stuff
GOOGLE_CLIENT_ID = "403366269449-k4m8rkruld2v4fpmkvgs9tvntomk4st9.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        address = request.form.get("address")
        url = "https://api.myptv.com/geocoding/v1/locations/by-address?street="
        words = address.split()
        url += words.pop(0)
        for word in words:
            url += "%20" + word
        response = requests.request("GET", url, headers=headers)
        latitude = response.json()['locations'][0]['referencePosition']['latitude']
        longitude = response.json()['locations'][0]['referencePosition']['longitude']
        obj = []
        for document in collection.find():
            if (abs(document['latitude'] - latitude) < 0.2) and (abs(document['longitude'] - longitude) < 0.2):
                thing = {"title": document['title'], "content": document['content'], "address": document['address']}
                obj.append(thing)
        return render_template("index.html", active=True, latitude=latitude, longitude=longitude, obj=obj)
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/posts.html", methods=["GET", "POST"])
def posts():
    if request.method == "POST":
        post_title = request.form.get("postTitle")
        post_content = request.form.get("postContent")
        post_address = request.form.get("address")
        url = "https://api.myptv.com/geocoding/v1/locations/by-address?street="
        words = post_address.split()
        url += words[0]
        words.pop(0)
        for word in words:
            url += "%20" + word
        response = requests.request("GET", url, headers=headers)
        latitude = response.json()['locations'][0]['referencePosition']['latitude']
        longitude = response.json()['locations'][0]['referencePosition']['longitude']
        post = {"_id": str(uuid.uuid4()), "title": post_title, "content": post_content, "address": post_address, "latitude": latitude, "longitude": longitude}
        collection.insert_one(post)
        return redirect('/posts.html')
    return render_template("posts.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/account")
def account():
    return render_template("account.html", session=session)


@app.route("/signup")
def signup():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)
    
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    session["picture"] = id_info.get("picture")
    session["logged_in"] = True
    return redirect("/protected_area")

@app.route("/protected_area")
def protected_area():
    print(session["name"])
    print(session["google_id"])
    print(session["email"])
    return redirect("/")    

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")





if __name__ == '__main__':
    app.run(debug=True)