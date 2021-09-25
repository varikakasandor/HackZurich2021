import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from helper import *
from pipeline import pdf2text

app = Flask(__name__,static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploaded_contracts'


@app.route("/")
def home():
    return app.send_static_file('application.html')


@app.route('/contracts/<name>')
def download_contract(name):
    # return render_template(os.path.join(app.config['UPLOAD_FOLDER'], name))
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/process', methods=['POST'])
def upload_contract():
    contract = request.files['contract']
    filename = secure_filename(contract.filename)
    input_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    contract.save(input_filename)
    model_input_text = pdf2text.convert_pdf(input=input_filename, output=app.config['UPLOAD_FOLDER'], mode=pdf2text.TXT)
    output_filename = pdf2text.convert_pdf(input=input_filename, output=app.config['UPLOAD_FOLDER'], mode=pdf2text.HTML)
    return redirect(url_for('download_contract', name=output_filename))  # TODO: replace by calling the ML model and then returning the analyzed document


if __name__ == '__main__':
    app.run(debug=True)
