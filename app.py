import os
import requests
import time
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "UPLOAD_FOLDER"
ML_MODEL1_URL = 'http://dc2f3f9e-db88-472e-9189-37a7296041f0.westeurope.azurecontainer.io/score'
mode = 'j1-large'
mode = 'j1-jumbo'
ML_MODEL2_URL = f'https://api.ai21.com/studio/v1/{mode}/complete'
YOUR_API_KEY = os.environ['API_KEY']
TEMPLATE_Q = 'Highlight the parts (if any) of this contract related to "{}" that should be reviewed by a lawyer.'
DUTIES_QUESTION = TEMPLATE_Q.format('Duties')
RIGHTS_QUESTION = TEMPLATE_Q.format('Rights')
app = Flask(__name__, static_folder='static')
app.config[UPLOAD_FOLDER] = 'uploaded_contracts'

@app.route("/")
def home():
    return app.send_static_file('application.html')


@app.route('/main_model/<name>')
def call_main_model(name):
    txt_path = os.path.join(app.config[UPLOAD_FOLDER], name)
    print(txt_path)
    with open(txt_path, 'r') as f:
        data = ''.join(f.readlines())
    rights_json = {'text': data, 'question': RIGHTS_QUESTION}
    rights_response = requests.post(url=ML_MODEL1_URL, json=rights_json)
    print(rights_response.status_code)  # , rights_response.json())
    duties_json = {'text': data, 'question': DUTIES_QUESTION}
    duties_response = requests.post(url=ML_MODEL1_URL, json=duties_json)
    print(duties_response.status_code)  # , duties_response.json())
    d = {}
    if rights_response.status_code == 200 and duties_response.status_code == 200:
        d['rights'] = rights_response.json()[:2]
        d['duties'] = duties_response.json()[:2]
        return d
    return ''


@app.route('/secondary_model_form')
def secondary_model_form():
    return app.send_static_file('query_secondary_model.html')


@app.route('/secondary_model_form_output', methods=['POST'])
def secondary_model_form_output():
    print(request.form)
    comment = request.form['comment']
    print(comment)
    x = call_secondary_model(query=comment)
    return render_template('query_output.html', query=x['query'], reply=x['reply'])


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
        return {'query': query, 'reply': data['completions'][0]['data']['text'][:-1]}
    return ''


@app.route('/contracts/<name>')
def download_contract(name):
    # TODO implement model-based analysis
    return app.send_static_file('hardcoded_analysis.html')
    #return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/process', methods=['POST'])
def upload_contract():
    contract = request.files['contract']
    filename = secure_filename(contract.filename)
    contract.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    time.sleep(7)
    return redirect(url_for('download_contract', name=filename))  # TODO: replace by calling the ML model and then returning the analyzed document


if __name__ == '__main__':
    app.run(debug=True)
