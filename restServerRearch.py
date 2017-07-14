import falcon
import json

class UserResource:
    def on_get(self, req, resp):
        """Handles Get Requests"""

        user = {
            'username': 'dietcokke',
            'password': 'admin1234',
            'email': 'yaks98682@yahoo.com'
        }

        resp.status = falcon.HTTP_200
        resp.body = json.encoder(user)

api = falcon.API()
users = UserResource()
api.add_route('/user', users)