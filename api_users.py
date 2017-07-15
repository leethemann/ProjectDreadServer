import datetime
import json
from bottle import request, response
from bottle import post, get, put, delete

USERS = [
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

@post('/users')
def create_user():
    try:
        try:
            data = request.json()
            print 'parsed json correctly.'
        except:
            """"request.json parsed bad json, kick it back"""
            raise ValueError()

        if data is None:
            """"Request body was either empty or not json, kick it back"""
            print 'data was nothing.'
            raise ValueError()

        print 'data was something.'
        if 'username' not in data or 'password' not in data:
            raise ValueError()

        username = data['username']

        for user in USERS:
            if user['username'] == username:
                print 'duplicate username'
                raise KeyError('Duplicate Username')

        print('no duplicates found.')

        user = {
            'username': data['username'],
            'password': data['password'],
            'id': USERS[-1]['id'] + 1,
            'date-created': datetime.date.today().strftime("%m/%d/%y"),
            'online': False
        }

    except ValueError():
        response.headers['Content-Type'] = 'application/JSON'
        response.status = 400
        response.body = json.dumps({'error': 'Bad Request'})
        return

    except KeyError():
        response.headers['Content-Type'] = 'application/JSON'
        response.status = 409
        response.body = json.dumps({'error': 'Duplicate Username'})
        return

    except Exception as e:
        print e
        response.headers['Content-Type'] = 'application/JSON'
        response.status = 500
        response.body = json.dumps({'error': 'Internal Error. Probably that bad python string I havne\'t fixed yet...'})
        return

    if user:
        USERS.append(user)

    response.headers['Content-Type'] = 'application/JSON'
    return json.dumps({'user': user})

@get('/users')
def get_users():
    pass

@put('/users/<id>')
def update_user():
    pass

@delete('/users/<id>')
def delete_user():
    pass