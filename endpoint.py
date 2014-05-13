from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_word():
    return 'Hey there, try JSON!'

@app.route('/add', methods = ['POST'])
def add_transaction():
    if not request.json:
        abort(400)
    else:
        # DO construct json object and insert.
        print request.json
        return request.json, 201

def run_app(host=None, port=None):
    # DO argument checking.
    if host is None or port is None:
        app.run()
    else:
        app.run(host=host, port=port)
