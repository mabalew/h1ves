"""Module to operate on hives."""
from hives import main
from hives import log


db = []


def get_log(function, result, param, status):
    _log = {}
    _log['function'] = function
    _log['result'] = result
    _log['params'] = param
    _log['status'] = status
    return _log


def start():
    _date = main.get_time_with_millis()
    _log = get_log('hive.start', '', '', 'ok')
    _log['start_date'] = _date
    result = {'status': 'ok',
              'version': main.get_version(),
              'datetime': _date}
    _log['end_date'] = _date
    log.log(_log)
    return result


def get_hives():
    _date = main.get_time_with_millis()
    _log = get_log('hive.get_hives', '', '', 'ok')
    _log['start_date'] = _date
    if len(db) > 0:
        _log['result'] = db
        log.log(_log)
        _date = main.get_time_with_millis()
        _log['end_date'] = _date
        return db
    else:
        _log['result'] = None
        _log['status'] = 'error'
        _log['end_date'] = _date
        _date = main.get_time_with_millis()
        log.log(_log)
        return {'error': 'no hives found'}


def get_hive(id):
    _date = main.get_time_with_millis()
    _log = get_log('hive.get_hive', '', id, 'ok')
    _log['start_date'] = _date
    if len(db) > 0:
        for i in range(len(db)):
            if db[i]['id'] == id:
                _log['result'] = db[i]
                _date = main.get_time_with_millis()
                _log['end_date'] = _date
                log.log(_log)
                return db[i]
    result = {'error': 'hive not found'}
    _log['status'] = 'error'
    _log['result'] = result
    _date = main.get_time_with_millis()
    _log['end_date'] = _date
    log.log(_log)
    return result


def add_hive(req):
    _date = main.get_time_with_millis()
    _log = get_log('hive.add_hive', '', '', 'ok')
    _log['start_date'] = _date
    if req is not None:
        _log['params'] = req.get_json()
        hive_json = req.get_json()
        if hive_json is not None and hive_json['id'] is not None:
            db[hive_json['id']] = hive_json
            _log['result'] = hive_json
            _date = main.get_time_with_millis()
            _log['end_date'] = _date
            log.log(_log)
            return hive_json
    result = {'error': 'no input data provided'}
    _log['status'] = 'error'
    _log['result'] = result
    _date = main.get_time_with_millis()
    _log['end_date'] = _date
    log.log(_log)
    return result


def update_hive(id, req):
    _date = main.get_time_with_millis()
    _log = get_log('hive.update_hive', '', '', 'ok')
    _log['start_date'] = _date
    if req is not None:
        _log['params'] = req.get_json()
        hive_json = req.get_json()
        for i in range(len(db)):
            if db[i]['id'] == id:
                db[i] = hive_json
                _date = main.get_time_with_millis()
                _log['end_date'] = _date
                _log['result'] = hive_json
                log.log(_log)
                return hive_json
            result = {'error': 'hive not found'}
            _log['status'] = 'error'
            _log['result'] = result
            _date = main.get_time_with_millis()
            _log['end_date'] = _date
            log.log(_log)
            return result
    result = {'error': 'no input data provided'}
    _log['result'] = result
    _log['status'] = 'error'
    _date = main.get_time_with_millis()
    _log['end_date'] = _date
    log.log(_log)
    return result


def delete_hive(id):
    _date = main.get_time_with_millis()
    _log = get_log('hive.delete_hive', '', '', 'ok')
    _log['start_date'] = _date
    for i in range(len(db)):
        _log['params'] = id
        if db[i]['id'] == id:
            deleted = db[i]
            del(db[i])
            _log['result'] = deleted
            _date = main.get_time_with_millis()
            _log['start_date'] = _date
            log.log(_log)
            return deleted
    result = {'error': 'hive not found'}
    _log['status'] = 'error'
    _log['result'] = result
    _date = main.get_time_with_millis()
    _log['start_date'] = _date
    log.log(_log)
    return result
