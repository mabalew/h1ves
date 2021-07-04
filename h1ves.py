from flask import Flask

app = Flask(__name__)


@app.route("/")
def start():
    return {'status': 'ok',
            'H1VES_STAGING_API_KEY': env['H1VES_STAGING_API_KEY']}

if __name__ == '__main__':
    app.run()
