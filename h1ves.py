from flask import Flask

app = Flask(__name__)


@app.route("/")
def start():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run()
