import json

from flask import Flask, request
from flask.ext.restful import Api, Resource

app = Flask(__name__, static_url_path="")
api = Api(app)


class GetIP(Resource):
    def get(self):
        payload = {}
        remote_addy = request.remote_addr
        x_forward_info = request.headers.get('X-Forwarded-For')
        payload['data'] = {'X-Forwarded-For': x_forward_info, 'remote_ip': remote_addy}
        return payload

api.add_resource(GetIP, '/', endpoint='getip')

if __name__ == '__main__':
    app.run(debug=True)
