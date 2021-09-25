import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from waitress import serve

from helper import *


app = Flask(__name__,static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploaded_contracts'

@app.route("/")
def home():
    return app.send_static_file('application.html')

@app.route("/team")
def team_web():
	return "<h1>This is our team! :) </h1>"

@app.route('/contracts/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/process', methods=['POST'])
def upload_contract():
    contract = request.files['contract']
    filename = secure_filename(contract.filename)
    contract.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('download_file', name=filename)) #TODO: replace by calling the ML model and then returning the analyzed document



if __name__=='__main__':
    serve(app, host='127.0.0.1', port=8080)