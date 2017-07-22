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
def creation_handler():
    #Handles name creation

    try:
        # parse input data
        try:
            data = request.json
        except:
            raise SyntaxError("Bad Json Format")

        if data is None:
            raise ValueError("Data was nothing")

        username = data['username']

        for user in USERS:
            if user['username'] == username:
                raise KeyError("Duplicate Username")

        user = {
            'username': data['username'],
            'password': data['password'],
            'id': USERS[-1]['id'] + 1,
            'date-created': datetime.date.today().strftime("%m/%d/%y"),
            'online': False
        }

    except ValueError as ve:
        # if bad request data, return 400 Bad Request
        response.headers['Content-Type'] = 'application/json'
        response.status = 400
        return json.dumps({'error': ve.args[0]})
    
    except KeyError as ke:
        # if name already exists, return 409 Conflict
        response.headers['Content-Type'] = 'application/json'
        response.status = 409
        return json.dumps({'error': ke.args[0]})

    except SyntaxError as se:
        response.status = 400
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({'error': se.args[0]})

    # add name
    USERS.append(user)
    
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'name': user})


@get('/users')
def get_users():
    response.status = 200
    response.headers['Content-Type'] = 'appication/JSON'
    return json.dumps({'users': USERS})

@put('/users/<username>')
def update_user(username):
    try:
        userToEdit = None
        
        for user in USERS:
            #this for needs to be replaced with something more performant. An O(n) is a little slow here
            if user['username'] == username:
                originalUser = user
                userToEdit = user
                break

        if userToEdit is None:
            raise ValueError("User could not be found.")

        try:
            data = request.json
        except:
            raise SyntaxError("Invalid Json Format / No Json to Parse.")

        if data is None:
            raise ValueError("No data to use.")
        
        if 'username' in data:
            userToEdit['username'] = data['username']

        if 'password' in data:
            userToEdit['password'] = data['password']

    except ValueError as ve:
        response.status = 400
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({'error': ve.args[0]})

    except SyntaxError as se:
        response.status = 400
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({'error': se.args[0]})

    USERS.remove(originalUser)
    USERS.append(userToEdit)

    response.status = 200
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'user': userToEdit})

@delete('/users/<username>')
def delete_user(username):
    for user in USERS:
        if user['username'] == username:
            USERS.remove(user)
            response.status = 200
            response.headers['Content-Type'] = 'appication/JSON'
            return
    
    response.status = 404
    response.headers['Content-Type'] = 'appication/JSON'
    return json.dumps({'error': "User not found"})