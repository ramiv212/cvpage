from flask import Flask,render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')


PORT = os.environ["PORT"]
app.run(debug=True,host="0.0.0.0", port=PORT)


# TODO
# get my age to auto update on the page. Using jinya and python.