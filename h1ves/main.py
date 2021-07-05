from flask import Flask

app = Flask(__name__)


@app.route("/license")
def get_license():
    return {'license': 'body'}
