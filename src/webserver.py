
from flask import Flask
from functools import partial
import os

app = Flask(__name__)
port = int(os.environ.get("PORT", 3000))


@app.route('/')
def hello():
    return "Hello World !"


partial_run = partial(app.run, host="0.0.0.0", port=port, debug=False, use_reloader=False)
