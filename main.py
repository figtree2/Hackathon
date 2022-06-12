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

cluster = MongoClient("mongodb+srv://figtree:1234@cluster0.j0ptd.mongodb.net/?retryWrites=true&w=majority")
db = cluster["Cluster0"]
collection = db["Posts"]

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
    # post_title = request.form.get("postTitle")
    # post_content = request.form.get("postContent")
    # post = {"title": post_title, "content": post_content}
    # collection.insert_one(post)
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

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