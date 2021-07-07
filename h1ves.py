from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from hives import main
from hives import hive
from hives import log


app = Flask(__name__)
auth = HTTPBasicAuth()


def get_header_base(start_date):
    header = {'version': main.get_version(),
              'start_date': start_date,
              'end_date': main.get_time_with_millis()}
    return header


@auth.verify_password
def authenticate(username, password):
    _date = main.get_time_with_millis()
    _log = get_header_base(_date)
    if username and password:
        if main.authenticate(username, password):
            _date = main.get_time_with_millis()
            _log['end_date'] = _date
            _log['result'] = True
            _log['params'] = {'username': username, 'password': password}
            _log['status'] = 'ok'
            log.log(_log)
            return True
        else:
            _date = main.get_time_with_millis()
            _log['end_date'] = _date
            _log['result'] = False
            _log['status'] = 'error'
            _log['params'] = {'username': username, 'password': password}
            log.log(_log)
            return False


@app.route("/")
@auth.login_required
def start():
    _date = main.get_time_with_millis()
    header = {'header': get_header_base(_date),
              'message':
              'This endpoint is just to confirm that hives module wworks'}
    return {'header': header,
            'body': hive.start()}


@app.route("/version")
@auth.login_required
def get_version():
    header = get_header_base(main.get_time_with_millis())
    header['message'] = 'This endpoint returns hives version number.'
    return {'header': header,
            'version': main.get_version()}


@app.route("/license")
@auth.login_required
def get_license():
    header = get_header_base(main.get_time_with_millis())
    header['message'] = 'This endpoint returns license text.'
    return {'header': header,
            'license': main.get_license()}


@app.route("/hive")
@auth.login_required
def get_hive():
    header = get_header_base(main.get_time_with_millis())
    header['message'] = 'This endpoint returns details of selected hive.'
    return {'header': header,
            'body': hive.get_hive()}


@app.route("/hive/<int:id>", methods=['POST', 'GET', 'PUT', 'DELETE'])
@auth.login_required
def _hive(id):
    """CRUD operations on hive."""
    # Prepare header
    header = get_header_base(main.get_time_with_millis())
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

    header['end_date'] = main.get_time_with_millis()
    response = {'header': header,
                'body': result}
    return response


@app.route("/hives")
@auth.login_required
def _hives():
    """Get all hives."""
    header = get_header_base(main.get_time_with_millis())
    header['message'] = "This endpoint lists all hivees."
    result = hive.get_hives()
    header['end_date'] = main.get_time_with_millis()
    response = {'header': header,
                'body': result}
    return response


@app.route("/logs")
@auth.login_required
def logs():
    """Returns all logs"""
    header = get_header_base(main.get_time_with_millis())
    header['end_date'] = main.get_time_with_millis()
    return {'header': header,
            'body': log.get_logs()}

if __name__ == '__main__':
    app.run()
