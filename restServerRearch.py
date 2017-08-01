import bottle
import pymongo
import api_users
 
app = APPLICATION = bottle.default_app()

print('test test 1234')

if __name__ == '__main__':
    bottle.debug = True
    bottle.run(server='gunicorn',host='127.0.0.1', port=8000)