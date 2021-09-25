from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<p>Hello, World!! <a href="team">Test link</a></p>'

@app.route("/team")
def team_web():
	return "this is our team"

