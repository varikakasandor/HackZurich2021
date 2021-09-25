import os
import time
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename


from helper import *


app = Flask(__name__,static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploaded_contracts'

@app.route("/")
def home():
    return app.send_static_file('application.html')

@app.route("/team")
def team_web():
	return "<h1>This is our team! :)</h1>"

@app.route('/contracts/<name>')
def download_contract(name):
    return app.send_static_file('hardcoded_analysis.html')
    #return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/process', methods=['POST'])
def upload_contract():
    contract = request.files['contract']
    filename = secure_filename(contract.filename)
    contract.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    time.sleep(3)
    return redirect(url_for('download_contract', name=filename)) #TODO: replace by calling the ML model and then returning the analyzed document



if __name__=='__main__':
    app.run(debug=True)