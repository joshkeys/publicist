from functools import wraps
from flask import Flask, request, current_app
from flask.ext.restful import Api, Resource

app = Flask(__name__, static_url_path="")
api = Api(app)


def type_formatter(func):
    """Send back proper format"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        format_type = request.args.get('format')
        callback = request.args.get('callback', 'callback')
        data = str(func(*args, **kwargs)['data']['ip'])
        if format_type == 'jsonp':
            content = str(callback) + '({"ip":"' + str(data) + '"});'
            return current_app.response_class(content, mimetype='application/javascript')
        elif format_type == 'text':
            content = str(data)
            return current_app.response_class(content, mimetype='text/plan')
        else:
            return func(*args, **kwargs)
    return decorated_function


class GetIP(Resource):
    @type_formatter
    def get(self):
        payload = {}
        remote_addy = request.remote_addr
        x_forward_info = request.headers.get('X-Forwarded-For')
        payload['meta'] = {'X-Forwarded-For': x_forward_info, 'remote_ip': remote_addy}
        if x_forward_info:
            client_addy = x_forward_info.split(',')[0]
        else:
            client_addy = remote_addy
        payload['data'] = {"ip": client_addy}
        return payload

api.add_resource(GetIP, '/', endpoint='getip')

if __name__ == '__main__':
    app.run(debug=True)
