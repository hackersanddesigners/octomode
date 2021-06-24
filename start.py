# https://github.com/python-escpos/python-escpos
# https://python-escpos.readthedocs.io/en/latest/

import flask
from flask import request
# import flask_apscheduler
import urllib, json
import os

# Create the application.
APP = flask.Flask(__name__)

# Recurrent actions
# scheduler = flask_apscheduler.APScheduler()
# scheduler.api_enabled = False
# scheduler.init_app(APP)
# scheduler.start()

# @scheduler.task('interval', id='check', minutes=1)
# def action():
# 	print('Do something recurrent')

pads = [
		'post-script.md',
		'post-script.css'
	]
DIR_PATH = '/home/mb/post-script-interface'

def download(pads):
	# using etherpump
	for pad in pads:
		os.system(f'{ DIR_PATH }/venv/bin/etherpump gettext { pad } > { DIR_PATH }/static/{ pad }')

@APP.route('/', methods=['GET'])
def pad():
	return flask.render_template('pad.html')

@APP.route('/html/', methods=['GET', 'POST'])
def html():
	# download the main post-script pad + stylesheet pad
	download(pads)
	# generate html page
	os.system(f'pandoc -f markdown -t html -c post-script.css --toc --toc-depth=1 --standalone { DIR_PATH }/static/post-script.md -o { DIR_PATH }/static/post-script.html')

	return flask.render_template('html.html')

@APP.route('/pdf/', methods=['GET'])
def pdf():
	# download the main post-script pad + stylesheet pad
	download(pads)
	# generate html page
	os.system(f'pandoc -f markdown -t html -c post-script.css --toc --toc-depth=1 --standalone { DIR_PATH }/static/post-script.md -o { DIR_PATH }/static/post-script.html')
	# generate pdf
	os.system(f'{ DIR_PATH }/venv/bin/weasyprint -s { DIR_PATH }/static/post-script.css { DIR_PATH }/static/post-script.html { DIR_PATH }/static/post-script.pdf')

	return flask.render_template('pdf.html')

@APP.route('/stylesheet/', methods=['GET'])
def stylesheet():
	return flask.render_template('stylesheet.html')

if __name__ == '__main__':
	APP.debug=True
	APP.run(port=5577)
