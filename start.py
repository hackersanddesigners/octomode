import flask
from flask import request
import urllib, json
import os

# Create the application.
APP = flask.Flask(__name__)

# ---

#The following three lines are the variables that need to be changed when making a new project.

PROJECTNAME = 'dsn'
DIR_PATH = '/home/systers/dsn-documentation'                                                                                                                                                                       │··························
PORTNUMBER = 5599

# ---


pads = [
		f'{ PROJECTNAME }.md',
		f'{ PROJECTNAME }.css'
	]

def download(pads):
	# using etherpump
	for pad in pads:
		os.system(f'{ DIR_PATH }/venv/bin/etherpump gettext { pad } > { DIR_PATH }/static/{ pad }')

@APP.route('/', methods=['GET'])
def pad():
	return flask.render_template('pad.html')

@APP.route('/pagedjs/', methods=['GET', 'POST'])
def pagedjs():
        # download the main post-script pad + stylesheet pad
	download(pads)
	# generate html page with the pandoc template (with paged.js inserted in the header)
	os.system(f'pandoc -f markdown -t html -c { PROJECTNAME }.css --toc --toc-depth=1 --template { DIR_PATH }/templates/pandoc-template-pagedjs.html --standalone { DIR_PATH }/static/{ PROJECTNAME }.md -o { DIR_PATH }/static/{ PROJECTNAME }.pagedjs.html')

	return open('static/{ PROJECTNAME }.pagedjs.html', 'r').read()

@APP.route('/html/', methods=['GET', 'POST'])
def html():
	# download the main post-script pad + stylesheet pad
	download(pads)
	# generate html page
	os.system(f'pandoc -f markdown -t html -c { PROJECTNAME }.css --toc --toc-depth=1 --standalone { DIR_PATH }/static/{ PROJECTNAME }.md -o { DIR_PATH }/static/{ PROJECTNAME }.html')

	return flask.render_template('html.html')

@APP.route('/stylesheet/', methods=['GET'])
def stylesheet():
	return flask.render_template('stylesheet.html')

if __name__ == '__main__':
	APP.debug=True
	APP.run(port={ PORTNUMBER })
