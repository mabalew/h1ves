from flask import Flask
from boto.s3.connection import S3Connection

app = Flask(__name__)


@app.route("/")
def start():
    return {'status': 'ok',
            'H1VES_STAGING_API_KEY': S3Connection(os.environ['H1VES_STAGING_API_KEY'])}


if __name__ == '__main__':
    app.run()
