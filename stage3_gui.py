from flask import Flask
from flask import render_template
import json

app = Flask(__name__)

with open('devices.json', 'r') as infile:
    mydata = json.load(infile)

     

@app.route('/')
def hello_world(name = None, data = mydata):
    return render_template('index.html', name=name, data=data)

