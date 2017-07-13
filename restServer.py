from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'internalBoss':
        return '1337Boss'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized Access'}), 401)

users = [
    {
        'id':1,
        'username':u'Dietcokke',
        'Date Created':u'7/11/17',
        'password':u'test123',
        'online':True
    },
    {
        'id':2,
        'username':u'Drebunny',
        'Date Created':u'7/11/17',
        'password':u'test123',
        'online':False
    }
]

def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'id':
            new_user['uri'] = url_for('get_user', user_id=user['id'], _external = True)
        else:
            new_user[field] = user[field]
    return new_user

@app.route('/projectdread/api/v1.0/users')
@auth.login_required
def get_users():
    return jsonify({'users': [make_public_user(user) for user in users]})

@app.route('/projectdread/api/v1.0/users', methods=['POST'])
@auth.login_required
def create_user():
    if not request.json or (not 'username' in request.json or not 'password' in request.json):
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'username': request.json['username'],
        'Date Created': datetime.date.today().strftime("%m/%d/%y"),
        'password': request.json['password'],
        'online': False
    }
    users.append(user)
    return jsonify({'user': user}), 201

@app.route('/projectdread/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})

@app.route('/projectdread/api/v1.0/users/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'username' in request.json and type(request.json['username']) != unicode:
        abort(400)
    if 'password' in request.json and type(request.json['password']) != unicode:
        abort(400)
    user[0]['username'] = request.json.get('username', user[0]['username'])
    user[0]['password'] = request.json.get('password', user[0]['password'])
    return jsonify({'user': user[0]})

@app.route('/projectdread/api/v1.0/users/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    users.remove(user[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)