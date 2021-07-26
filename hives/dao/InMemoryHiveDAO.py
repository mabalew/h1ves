from flask import jsonify
from flask_restx import Resource


class HiveDAO(Resource):
    db = []

    def __init__(self, **kwargs):
        pass

    def get_all(self):
        return self.db

    def get_hive(self, id):
        if len(self.db) > 0:
            for i in range(len(self.db)):
                if self.db[i]['id'] == id:
                    return self.db[i]
        else:
            return None


    def add_hive(self, json):
        self.db.append({})
        hive = jsonify(json)
        id = len(self.db)
        hive['id'] = id
        self.db[id] = json
        return json

