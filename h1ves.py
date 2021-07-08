from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from hives import main
from hives import hive
from hives import log


app = Flask(__name__)
auth = HTTPBasicAuth()


def get_header(start_date, end_date, status, message, start_date_obj,
               end_date_obj):
    if start_date_obj == '' or end_date_obj == '':
        duration = None
    else:
        duration = end_date_obj - start_date_obj
    header = {'version': main.get_version(),
              'start_date': start_date,
              'end_date': main.get_time_with_millis(),
              'status': status,
              'message': message,
              'duration': str(duration)}
    return header


@auth.verify_password
def authenticate(username, password):
    start_date = main.get_time_with_millis()['formatted']
    header_message = 'This function authenticates the user.'
    if username and password:
        if main.authenticate(username, password):
            end_date = main.get_time_with_millis()['formatted']
            params = {'username': username, 'password': password}
            _log = get_header(start_date, end_date, 'ok', header_message, 1, 1)
            _log['result'] = True
            _log['params'] = params
            log.log(_log)
            return True
        else:
            end_date = main.get_time_with_millis()['formatted']
            params = {'username': username, 'password': password}
            _log = get_header(start_date, end_date, 'error',
                              header_message)
            _log['result'] = False
            _log['params'] = params
            log.log(_log)
            return False


@app.route("/")
@auth.login_required
def start():
    start_date_resp = main.get_time_with_millis()
    start_date = start_date_resp['formatted']
    start_date_obj = start_date_resp['datetime']
    body = hive.start()
    message = 'This endpoint is just to confirm that hives module wworks'
    end_date_resp = main.get_time_with_millis()
    end_date = end_date_resp['formatted']
    end_date_obj = end_date_resp['datetime']
    header = get_header(start_date, end_date, 'ok', message, start_date_obj,
                        end_date_obj)

    return {'header': header,
            'body': body}


@app.route("/version")
@auth.login_required
def get_version():
    start_date_resp = main.get_time_with_millis()
    start_date = start_date_resp['formatted']
    start_date_obj = start_date_resp['datetime']
    body = main.get_version()
    message = 'This endpoint returns hives version number.'
    end_date_resp = main.get_time_with_millis()
    end_date = end_date_resp['formatted']
    end_date_obj = end_date_resp['datetime']
    header = get_header(start_date, end_date, 'ok', message, start_date_obj,
                        end_date_obj)
    return {'header': header,
            'version': body}


@app.route("/license")
@auth.login_required
def get_license():
    start_date_resp = main.get_time_with_millis()
    start_date = start_date_resp['formatted']
    start_date_obj = start_date_resp['datetime']
    body = main.get_license()
    end_date_resp = main.get_time_with_millis()
    end_date = end_date_resp['formatted']
    end_date_obj = end_date_resp['datetime']
    message = 'This endpoint returns license text.'
    header = get_header(start_date, end_date, 'ok', message, start_date_obj,
                        end_date_obj)
    return {'header': header,
            'license': body}


# @app.route("/hive")
# @auth.login_required
# def get_hive():
    # start_date = main.get_time_with_millis()
    # body = hive.get_hive()}
    # message = 'This endpoint returns details of selected hive.'
    # end_date = main.get_time_with_millis()
    # header = get_header(start_date, end_date, None, None, 'ok',
    #                     message)
    # return {'header': header,
    #        'body': body}


@app.route("/hive/<int:id>", methods=['POST', 'GET', 'PUT', 'DELETE'])
@auth.login_required
def _hive(id):
    """CRUD operations on hive."""
    start_date_resp = main.get_time_with_millis()
    start_date = start_date_resp['formatted']
    start_date_obj = start_date_resp['datetime']
    # Prepare header
    header = get_header(main.get_time_with_millis())
    if request.method == 'GET':
        """Returns selected hive details."""
        message = "This endpoint adds new hive with id {}.".format(id)
        body = hive.get_hive(id)
    elif request.method == 'PUT':
        """Updates selected hive with data provided"""
        message = "This endpoint updates hive with id {}.".format(id)
        body = hive.update_hive(id, request)
    elif request.method == 'DELETE':
        """Removes selected hive."""
        message = "This endpoint deletes hive with id {}.".format(id)
        body = hive.delete_hive(id)
    elif request.method == 'POST':
        """Adds new hive."""
        message = "This endpoint adds new hive."
        body = hive.add_hive(request)
    else:
        message = 'Incorrect call of endpoint.'

    end_date_resp = main.get_time_with_millis()
    end_date = end_date_resp['formatted']
    end_date_obj = end_date_resp['datetime']
    header = get_header(start_date, end_date, 'ok', message, start_date_obj,
                        end_date_obj)
    response = {'header': header,
                'body': body}
    return response


@app.route("/hives")
@auth.login_required
def hives():
    """Get all hives."""
    start_date_resp = main.get_time_with_millis()
    start_date = start_date_resp['formatted']
    start_date_obj = start_date_resp['datetime']
    message = "This endpoint lists all hivees."
    body = hive.get_hives()
    end_date_resp = main.get_time_with_millis()
    end_date = end_date_resp['formatted']
    end_date_obj = end_date_resp['datetime']
    header = get_header(start_date, end_date, 'ok', message, start_date_obj,
                        end_date_obj)
    response = {'header': header,
                'body': body}
    return response


@app.route("/logs")
@auth.login_required
def logs():
    """Returns all logs"""
    message = 'This endpoint returns all logs'
    start_date_resp = main.get_time_with_millis()
    start_date = start_date_resp['formatted']
    start_date_obj = start_date_resp['datetime']
    body = log.get_logs()
    end_date_resp = main.get_time_with_millis()
    end_date = end_date_resp['formatted']
    end_date_obj = end_date_resp['datetime']
    header = get_header(start_date, end_date, 'ok', message, start_date_obj,
                        end_date_obj)
    return {'header': header,
            'body': body}

if __name__ == '__main__':
    app.run()
