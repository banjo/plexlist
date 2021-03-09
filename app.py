from flask import Flask, jsonify, redirect, request, session
from flask_cors import CORS, cross_origin
import os
from plex import Plex
from errors import SignInError, NotMediaServerError, NoServerError, UserError
from helpers import authorize
import json

app = Flask(__name__, static_folder="./client/dist", static_url_path="/")
CORS(app)

# constants
USERNAME = "username"
PASSWORD = "password"
SERVER = "server"
IMDB_ID = "id"

# configurations for session
# TODO: load from env
app.config["SECRET_KEY"] = "lI3K6Ga5o57MyP5LgZlz!#11ADDfgaef!??!?!!feafeaEFAEF"
app.config["SESSION_PERMANENT"] = False



@app.route('/sign-in', methods=['POST'])
@cross_origin(supports_credentials=True)
def sign_in():
    data = request.json

    if (not data):
        return {"error": "You need to include username and password"}, 400

    username = data[USERNAME]
    password = data[PASSWORD]

    if (not username or not password):
        return {"error": "You need to include username and password"}, 400

    try:
        plex_server = Plex(username, password)
    except SignInError:
        return {"error": "Wrong username or password"}, 401

    session[USERNAME] = username
    session[PASSWORD] = password
    return {"message": "Success"}, 200


@app.route('/test')
@authorize
def test():
    print(session[USERNAME])
    return "string"


@app.route('/get-servers')
@cross_origin(supports_credentials=True)
@authorize
def get_servers():
    username = session[USERNAME]
    password = session[PASSWORD]
    plex_server = Plex(username, password)
    servers = plex_server.get_plex_server_resources()
    names = [server.name for server in servers]
    return jsonify(names)


@app.route('/choose-server', methods=['POST'])
@cross_origin(supports_credentials=True)
@authorize
def choose_server():
    data = request.json
    if (not data):
        return {"error": "You need to include a server name"}, 400

    server = data[SERVER]

    if (not server):
        return {"error": "You need to include a server name"}, 400

    username = session[USERNAME]
    password = session[PASSWORD]
    plex_server = Plex(username, password)
    try:
        plex_server.add_resource_by_name(server)
    except NotMediaServerError:
        return {"error": "Not a plex server"}, 400
    except NoServerError:
        return {"error": "No server with that name"}, 400

    session[SERVER] = server
    return {"message": "Success"}, 200


@app.route("/get-users")
@cross_origin(supports_credentials=True)
@authorize
def get_users():
    username = session[USERNAME]
    password = session[PASSWORD]
    server = session[SERVER]

    if (not username or not password or not server):
        return {"error": "Could not find session data"}, 500

    plex_server = Plex(username, password)
    plex_server.add_resource_by_name(server)
    plex_server.connect()
    users = plex_server.get_users()

    return jsonify(users)


@app.route("/scrape-imdb", methods=['POST'])
@cross_origin(supports_credentials=True)
@authorize
def scrape_imdb():
    data = request.json
    if (not data):
        return {"error": "You need to include an IMDb id"}, 400

    imdb_id = data[IMDB_ID]

    if (not imdb_id):
        return {"error": "You need to include an IMDb id"}, 400

    username = session[USERNAME]
    password = session[PASSWORD]
    server = session[SERVER]

    if (not username or not password or not server):
        return {"error": "Could not find session data"}, 500

    plex_server = Plex(username, password)
    plex_server.add_resource_by_name(server)
    plex_server.connect()
    movies = plex_server.scrape_imdb("https://www.imdb.com/list/" + imdb_id)

    if (not movies):
        return {"error": "You need to include a valid IMDb id"}, 400

    session[IMDB_ID] = imdb_id

    return jsonify(movies)


@app.route("/add-movies", methods=['POST'])
@cross_origin(supports_credentials=True)
@authorize
def add_movies():
    data = request.json
    if (not data):
        return {"error": "You need to include movies, playlist name and users"}, 400

    movie_list = json.loads(data["movies"])
    name = data["name"]
    users = json.loads(data["users"])

    if (not movie_list or not name or not users):
        return {"error": "You need to include movies, playlist name and users"}, 400

    username = session[USERNAME]
    password = session[PASSWORD]
    server = session[SERVER]
    imdb_id = session[IMDB_ID]

    if (not username or not password or not server or not imdb_id):
        return {"error": "Could not find session data"}, 500

    plex_server = Plex(username, password)
    plex_server.add_resource_by_name(server)
    plex_server.connect()
    playlist, failed_movies = plex_server.add_playlist(name, movie_list)
    plex_server.copy_to_users(playlist, users)

    return jsonify(failed_movies)


@app.route("/sign-out")
@cross_origin(supports_credentials=True)
@authorize
def sign_out():
    session.clear()
    return {"message": "Success"}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")