from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restx import Api, Resource
from hives import main, hive, log


app = Flask(__name__)
api = Api(app=app, description="Hives API", title="Hives API")
auth = HTTPBasicAuth()
authorizations = {
    'basicAuth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    }
}
#    'apikey': {
#        'type': 'apiKey',
#        'in': 'header',
#        'name': 'X-API-KEY'
#
#    }
ns = api.namespace('hive', description='Operations on hives',
                   security='basicAuth', authorizations=authorizations)
api.add_namespace(ns)


def get_header(start_date, end_date, status, message, start_date_obj=None,
               end_date_obj=None):
    if start_date_obj is None or end_date_obj is None:
        duration = None
    else:
        duration = end_date_obj - start_date_obj
    version = main.get_version()
    credits = main.get_credits()
    header = {'version': version,
              'start_date': start_date,
              'end_date': end_date,
              'status': status,
              'message': message,
              'credits': credits,
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
            _log = get_header(start_date, end_date, 'ok', header_message)
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


@ns.route("/v1/info")
class Info(Resource):
    @api.doc(security='basicAuth')
    @auth.login_required
    def patch(self):
        """
        Get hives app version number.
        @return: json containings hives app version number in the body.
        """
        start_date_resp = main.get_time_with_millis()
        start_date = start_date_resp['formatted']
        start_date_obj = start_date_resp['datetime']
        body = main.get_version()
        message = 'This endpoint returns hives app version number.'
        end_date_resp = main.get_time_with_millis()
        end_date = end_date_resp['formatted']
        end_date_obj = end_date_resp['datetime']
        header = get_header(start_date, end_date, 'ok', message, start_date_obj,
                            end_date_obj)
        return {'header': header,
                'version': body}

    @api.doc(security='basicAuth')
    @auth.login_required
    def post(self):
        """
        Get license text.
        @return: json containings license text
        """
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

    @api.doc(security='basicAuth')
    @auth.login_required
    def get(self):
        """
        Returns all logs of hives
        @return: json containings all the logs of hive app
        """
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


@ns.route("/v1")
class HiveList(Resource):
    """
    List all hives, get selected hive and adds new one.
    """
    @api.doc(security='basicAuth')
    @auth.login_required
    def put(self):
        """
        Get confirmation that hives module works.
        @return: small json confirming application to be ready to work
        """
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

    @api.doc(security='basicAuth')
    @auth.login_required
    def get(self):
        """
        Get all hives.
        @return: json containings list of all hives
        """
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

    @api.doc(security='basicAuth')
    @api.param('json', 'Hive JSON representation')
    @auth.login_required
    def post(self):
        """
        Adds new hive.
        @param: int - hive identifier
        @param: json representing new hive
        @return: body of new hive with identifier
        """
        start_date_resp = main.get_time_with_millis()
        start_date = start_date_resp['formatted']
        start_date_obj = start_date_resp['datetime']
        message = "This endpoint adds new hive."
        json = request.args.get('json')
        body = hive.add_hive(jsonify(json))
        end_date_resp = main.get_time_with_millis()
        end_date = end_date_resp['formatted']
        end_date_obj = end_date_resp['datetime']
        header = get_header(start_date, end_date, 'ok', message, start_date_obj,
                            end_date_obj)
        response = {'header': header,
                    'body': body}
        return response


@api.param('id', 'Identifier of hive')
@ns.route("/v1/<int:id>")
@ns.param('id', 'Hive identifier')
class Hive(Resource):
    """
    Updates, deletes and retrieve existing hive.
    """
    @api.doc(security='basicAuth')
    @auth.login_required
    def patch(self, id):
        """
        Updates selected hive with data provided
        @param: int - hive identifier
        @return json containing updated hive in body
        """
        start_date_resp = main.get_time_with_millis()
        start_date = start_date_resp['formatted']
        start_date_obj = start_date_resp['datetime']
        message = "This endpoint updates hive with id {}.".format(id)
        body = hive.update_hive(id, request)
        end_date_resp = main.get_time_with_millis()
        end_date = end_date_resp['formatted']
        end_date_obj = end_date_resp['datetime']
        header = get_header(start_date, end_date, 'ok', message, start_date_obj,
                            end_date_obj)
        response = {'header': header,
                    'body': body}
        return response

    @api.doc(security='basicAuth')
    @auth.login_required
    def delete(self, id):
        """
        Removes selected hive.
        @param: int - hive identifier
        @return: json containing delete hive in body
        """
        start_date_resp = main.get_time_with_millis()
        start_date = start_date_resp['formatted']
        start_date_obj = start_date_resp['datetime']
        message = "This endpoint deletes hive with id {}.".format(id)
        body = hive.delete_hive(id)
        end_date_resp = main.get_time_with_millis()
        end_date = end_date_resp['formatted']
        end_date_obj = end_date_resp['datetime']
        header = get_header(start_date, end_date, 'ok', message, start_date_obj,
                            end_date_obj)
        response = {'header': header,
                    'body': body}
        return response

    @api.doc(responses={400: 'No hive id provided',
                        401: 'Not authorized',
                        200: 'ok'},
             )
    @api.doc(security='basicAuth')
    @auth.login_required
    def get(self, id):
        """
        Returns selected hive details.
        @param: int - hive identifier
        @return: json containing hive details in body
        """
        start_date_resp = main.get_time_with_millis()
        start_date = start_date_resp['formatted']
        start_date_obj = start_date_resp['datetime']
        # id = flask.request.args.get('id')
        message = "This endpoint retrives hive with id {}.".format(id)
        if id is None:
            end_date_resp = main.get_time_with_millis()
            end_date = end_date_resp['formatted']
            end_date_obj = end_date_resp['datetime']
            header = get_header(start_date, end_date, 'error', message,
                                start_date_obj, end_date_obj)
            body = {'error': {'code': 400, 'message': 'no hive id provided'}}
        else:
            body = hive.get_hive(id)
            end_date_resp = main.get_time_with_millis()
            end_date = end_date_resp['formatted']
            end_date_obj = end_date_resp['datetime']
            header = get_header(start_date, end_date, 'ok', message,
                                start_date_obj, end_date_obj)
        response = {'header': header,
                    'body': body}
        return response


api.add_resource(HiveList, '/hive/v1')
api.add_resource(Hive, '/hive/v1/<int:id>')
api.add_resource(Info, '/hive/v1/info')

if __name__ == '__main__':
    app.run()
