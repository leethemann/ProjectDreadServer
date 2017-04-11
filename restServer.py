from flask import Flask, jsonify, abort

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

if __name__ == '__main__':
    app.run(debug=True)