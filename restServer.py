from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

users = [
    {
        'id':1,
        'username':u'Dietcokke',
        'race':u'Orcs',
        'gold':25000,
        'online':True
    },
    {
        'id':2,
        'username':u'Drebunny',
        'race':u'Elves',
        'gold':25000,
        'online':False
    }
]

@app.route('/projectdread/api/v1.0/users')
def get_users():
    return jsonify({'users': users})

@app.route('/projectdread/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})

@app.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/projectdread/api/v1.0/users', methods=['POST'])
def create_take():
    if not request.json or not 'username' in request.json:
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'username': request.json['username'],
        'race': request.json['race'],
        'gold': request.json['gold'],
        'online': False
    }
    users.append(user)
    return jsonify({'user': user}), 201

if __name__ == '__main__':
    app.run(debug=True)