import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import requests
from werkzeug.utils import secure_filename

from helper import *
from pipeline import pdf2text

app = Flask(__name__,static_folder='static')
UPLOAD_FOLDER = "UPLOAD_FOLDER"
app.config[UPLOAD_FOLDER] = 'uploaded_contracts'
ML_MODEL1_URL = 'http://dc2f3f9e-db88-472e-9189-37a7296041f0.westeurope.azurecontainer.io/score'
ML_MODEL2_URL = 'https://api.ai21.com/studio/v1/j1-large/complete'
YOUR_API_KEY = os.environ['API_KEY']


@app.route("/")
def home():
    return app.send_static_file('application.html')


@app.route('/contracts/<name>')
def download_contract(name):
    # return render_template(os.path.join(app.config['UPLOAD_FOLDER'], name))
    return send_from_directory(app.config[UPLOAD_FOLDER], name)


@app.route('/main_model/<name>')
def call_main_model(name):
    txt_path = os.path.join(app.config[UPLOAD_FOLDER], name)
    print(txt_path)
    with open(txt_path, 'r') as f:
        data = ''.join(f.readlines())
    dummy_data = {'data': data}
    response = requests.post(url=ML_MODEL1_URL, data=dummy_data)
    print(response)
    return response.json()


@app.route('/secondary_model/<query>')
def call_secondary_model(query):
    prompt = "My second grader asked me what this passage means:\n"\
             f"\"{query}\"\n"\
             "I rephrased it for him, in plain language a second grader can understand:\n\""
    json = {
        "prompt": prompt,
        "numResults": 1,
        "maxTokens": 64,
        "stopSequences": ["\"\"\"", "\n"],
        "topKReturn": 0,
        "temperature": 0.0
    }
    response = requests.post(url=ML_MODEL2_URL, headers={"Authorization": f"Bearer {YOUR_API_KEY}"}, json=json)
    if response.status_code == 200:
        data = response.json()
        return data['completions'][0]['data']['text'][:-1]
    return ''


@app.route('/process', methods=['POST'])
def upload_contract():
    contract = request.files['contract']
    filename = secure_filename(contract.filename)
    input_filename = os.path.join(app.config[UPLOAD_FOLDER], filename)
    contract.save(input_filename)
    print('a')
    model_input_text = pdf2text.convert_pdf(input=input_filename, output=app.config[UPLOAD_FOLDER], mode=pdf2text.TXT)
    print('b')
    output_filename = pdf2text.convert_pdf(input=input_filename, output=app.config[UPLOAD_FOLDER], mode=pdf2text.HTML)
    print('c')
    return redirect(url_for('download_contract', name=output_filename))  # TODO: replace by calling the ML model and then returning the analyzed document


if __name__ == '__main__':
    app.run(debug=True)
