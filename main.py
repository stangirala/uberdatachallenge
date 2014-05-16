import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from views import endpoint

if __name__ == '__main__':

    # Test
    #endpoint.run_app(debug=True)

    # Scale
    flask_app = endpoint.get_app()
    http_server = WSGIServer(('127.0.0.1', 5000), flask_app)
    http_server.serve_forever()
