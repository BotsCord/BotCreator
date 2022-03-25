import flask

app = flask.Flask(__name__)

@app.route("/plugins")
def plugins():
    return flask.jsonify({"plugins": [{"name": "test", "url": "http://localhost:8080/list/test.py"}]})

@app.route("/list/<path>")
def send_plugin(path):
    return open(path).read()

app.run(port=8080)
