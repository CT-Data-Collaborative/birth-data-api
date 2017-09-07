#!/usr/env/bin python
import os

from flask import Flask, jsonify, abort, make_response
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, JSONAttribute

app = Flask(__name__)

class Town(Model):
    class Meta:
        table_name = 'dev.birthapitowns'
    id = UnicodeAttribute(hash_key=True)
    data = JSONAttribute()


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
@app.errorhandler(Model.DoesNotExist)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'name': 'birth data api',
                    'version': os.environ.get('LAMBDA_VERSION', 'dev'),
                    'stage': os.environ.get('STAGE', 'dev')})

@app.route('/towns/<town_id>', methods=['GET'])
def get_town(town_id):
    try:
        town = Town.get(town_id)
    except Town.DoesNotExist:
        abort(400)
    return make_response(jsonify(town.data))


if __name__ == '__main__':
    app.run(debug=True)