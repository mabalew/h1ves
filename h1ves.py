from flask import Flask, request, jsonify
from hives import main
from hives import hive
from hives import log

app = Flask(__name__)


@app.route("/")
def start():
    return hive.start()


@app.route("/version")
def get_version():
    return {'version': main.get_version()}


@app.route("/license")
def get_license():
    return {'license': main.get_license()}


@app.route("/hive")
def get_hive():
    return hive.get_hive()


@app.route("/hive/<int:id>", methods=['POST', 'GET', 'PUT', 'DELETE'])
def _hive(id):
    """CRUD operations on hive."""
    # Prepare header
    header = {'version': main.get_version()}
    if request.method == 'GET':
        """Returns selected hive details."""
        header['message'] = "This endpoint adds new hive with id {}.".format(id)
        result = hive.get_hive(id)
    elif request.method == 'PUT':
        """Updates selected hive with data provided"""
        header['message'] = "This endpoint updates hive with id {}.".format(id)
        result = hive.update_hive(id, request)
    elif request.method == 'DELETE':
        """Removes selected hive."""
        header['message'] = "This endpoint deletes hive with id {}.".format(id)
        result = hive.delete_hive(id)
    elif request.method == 'POST':
        """Adds new hive."""
        header['message'] = "This endpoint adds new hive."
        result = hive.add_hive(request)
    else:
        header['message'] = 'Incorrect call of endpoint.'

    response = {'header': header,
                'body': result}
    return response


@app.route("/hives")
def _hives():
    """Get all hives."""
    header = {'version': main.get_version()}
    header['message'] = "This endpoint lists all hivees."
    result = hive.get_hives()
    response = {'header': header,
                'body': result}
    return response


@app.route("/logs")
def logs():
    return jsonify(log.get_logs())

if __name__ == '__main__':
    app.run()
