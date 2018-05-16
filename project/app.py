import sqlite3
import requests
from flask import Flask, jsonify, g, redirect
from flasgger import Swagger

DATABASE = './passwords.db'
HIBP_URL = 'https://api.pwnedpasswords.com/pwnedpassword/'
application = Flask(__name__)
Swagger(application)


def get_db():
    db = getattr(g, '_passwords', None)
    if db is None:
        db = g._messages = sqlite3.connect(DATABASE)
    return db


@application.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_passwords', None)
    if db is not None:
        db.close()


def init_db():
    with application.app_context():
        db = get_db()
        with application.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


init_db()


def save_password(password, results):
    try:
        results = int(results)
    except ValueError:
        results = 0
    cursor = get_db().cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO password_storage VALUES (?, ?)",
        (str(password), int(results))
    )
    get_db().commit()
    return True


def retrieve_password(password):
    cursor = get_db().cursor()
    cursor.execute("SELECT breaches FROM password_storage WHERE password=?", (password,))
    breaches = cursor.fetchone()
    # If password is recorded as not being breached need to update by checking api to make sure this is still the case
    if breaches is None or breaches is 0:
        breaches = hibp_api(password)
        save_password(password, breaches)
    return breaches


def hibp_api(password):
    headers = {"User-Agent": "secureworks-python-app", }
    r = requests.get(HIBP_URL + password, headers)
    breaches = 0 if r.status_code == 404 else r.text
    return breaches


@application.route('/')
def index():
    return redirect("/apidocs/#!/default/get_passwords_password", code=302)


@application.route('/passwords/<password>', methods=['GET'])
def check_password(password):
    """
    Service to check password breaches using HIBP's api
    API made with Flask and Flasgger
    ---
    parameters:
      - in: path
        name: password
        description: The password to be checked.
        required: true
        type: string
    responses:
      404:
        description: Error with password retrieval
      200:
        description: Your saved password has been retrieved
        # schema:
        #     type: integer
        #     name: breaches
    """

    results = retrieve_password(password)
    response = jsonify({"breaches": results}) if results or results == 0 else jsonify({"error": "Something went wrong"})
    code = 200 if results or results == 0 else 404
    return response, code


if __name__ == "__main__":
    import os

    os.environ.setdefault("LC_ALL", "en_US.UTF-8")
    os.environ.setdefault("LANG", "en_US.UTF-8")

    application.run(debug=True)
