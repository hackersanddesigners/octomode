import flask
from flask import request
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import os
import pypandoc
from jinja2 import Template

APP = flask.Flask(__name__)
APP.config.from_object("config.Config")

# ---

def get_pad_content(pad):
	arguments = { 
		'padID' : pad,
		'apikey' : APP.config['PAD_API_KEY']
	}
	api_call = 'getText'
	response = json.load(urlopen(f"{ APP.config['PAD_API_URL'] }{ api_call }", data=urlencode(arguments).encode()))
	
	# create pad in case it does not yet exist
	if response['code'] == 1 and 'padID does not exist' == response['message']:
		api_call = 'createPad'
		urlopen(f"{ APP.config['PAD_API_URL'] }{ api_call }", data=urlencode(arguments).encode())
		api_call = 'getText'
		response = json.load(urlopen(f"{ APP.config['PAD_API_URL'] }{ api_call }", data=urlencode(arguments).encode()))

	# print(response)
	content = response['data']['text']
	return content

def all_pads():
	arguments = { 
		'apikey' : APP.config['PAD_API_KEY'],
	}
	api_call = 'listAllPads'
	response = json.load(urlopen(f"{ APP.config['PAD_API_URL'] }{ api_call }", data=urlencode(arguments).encode()))

	return response

def create_pad_on_first_run(name, ext):
	pads = all_pads()
	pad = name+ext

	if 'md' in ext:
		default_template = 'templates/default.md'
	elif 'css' in ext:
		default_template = 'templates/default.css'
	elif 'template' in ext:
		default_template = 'templates/default-pandoc-template.html'

	if 'template' in ext:
		default_template = open(default_template).read()
		jinja_template = Template(default_template)
		default_template = jinja_template.render(name=name.strip())
	else:
		default_template = open(default_template).read()

	if pad not in pads['data']['padIDs']:
		arguments = { 
			'padID' : pad,
			'apikey' : APP.config['PAD_API_KEY'],
			'text' : default_template
		}
		api_call = 'createPad'
		response = json.load(urlopen(f"{ APP.config['PAD_API_URL'] }{ api_call }", data=urlencode(arguments).encode()))

def update_pad_contents(name):
	# download the md pad + stylesheet + template pad
	md_pad = f'{ name }.md'
	css_pad = f'{ name }.css'
	template_pad = f'{ name }.template'
	md = get_pad_content(md_pad)
	css = get_pad_content(css_pad)
	template = get_pad_content(template_pad)
	# !!! this breaks the whole idea that this application can be shared by multiple projects at the same time
	# !!! but py_pandoc needs to run with files........ hmmm
	with open('templates/pandoc-template.html', 'w') as f:
		f.write(template)

	return md, css, template

# ---

@APP.route('/', methods=['GET', 'POST'])
def index():
	name = request.values.get('name')
	if name: 
		# This is when the environment is "created"
		# The pads are filled with the default templates (pad, stylesheet, template)
		exts = ['.md', '.css', '.template']
		for ext in exts:
			create_pad_on_first_run(name, ext)
		return flask.redirect(f'/{ name }/')
	else:
		return flask.render_template('start.html')

@APP.route('/<name>/', methods=['GET'])
def main(name):
	# !!! Add a if/else here to check if the environment is "created" already
	ext = '.md'
	create_pad_on_first_run(name, ext)
	return flask.render_template('pad.html', name=name.strip(), ext=ext)

@APP.route('/<name>/pad/')
def pad(name):
	ext = '.md'
	create_pad_on_first_run(name, ext)
	return flask.render_template('pad.html', name=name.strip(), ext=ext)

@APP.route('/<name>/stylesheet/', methods=['GET'])
def stylesheet(name):
	ext = '.css'
	create_pad_on_first_run(name, ext)
	return flask.render_template('pad.html', name=name.strip(), ext=ext)

@APP.route('/<name>/template/', methods=['GET'])
def template(name):
	ext = '.template'
	create_pad_on_first_run(name, ext)
	return flask.render_template('pad.html', name=name.strip(), ext=ext)

# @APP.route('/<name>/html/')
# def html(name):
# 	# update pad contents
# 	md, css, template = update_pad_contents(name)
# 	# generate html page
# 	pandoc_args = [
# 		# '--css=static/print.css',
# 		'--toc',
# 		'--toc-depth=1',
# 		'--template=templates/pandoc-template.html',
# 		'--standalone'
# 	]
# 	html = pypandoc.convert_text(md, 'html', format='md', extra_args=pandoc_args)

# 	return flask.render_template('html.html', html=html, name=name.strip())

@APP.route('/<name>/pdf/')
def pdf(name):
	# In case the URL is edited directly with a new name
	exts = ['.md', '.css', '.template']
	for ext in exts:
		create_pad_on_first_run(name, ext)
	return flask.render_template('pdf.html', name=name.strip())

# //////////////
# rendered resources (not saved as a file on the server)

@APP.route('/<name>/print.css')
def css(name):
	x, css, x = update_pad_contents(name)
	
	return css, 200, {'Content-Type': 'text/css; charset=utf-8'}

@APP.route('/<name>/pandoc-template.html')
def pandoc_template(name):
	x, x, template = update_pad_contents(name)
	
	return template, 200, {'Content-Type': 'text/html; charset=utf-8'}

@APP.route('/<name>/pagedjs.html')
def pagedjs(name):
	# update pad contents
	md, css, template = update_pad_contents(name)
	# generate html page with the pandoc template (with paged.js inserted in the header)
	pandoc_args = [
		'--toc',
		'--toc-depth=1',
		'--template=templates/pandoc-template.html',
		'--standalone'
	]
	html = pypandoc.convert_text(md, 'html', format='md', extra_args=pandoc_args)

	return html, 200, {'Content-Type': 'text/html; charset=utf-8'}

# //////////////

def flask_logger():
	# creates logging information
	# https://www.vantage-ai.com/en/blog/adding-on-screen-logging-in-a-few-steps-using-a-flask-application
	
	from io import StringIO
	import logging
	from time import sleep 
	
	log_stream = StringIO()
	handler = logging.StreamHandler(log_stream)
	log = logging.getLogger('werkzeug')
	log.setLevel(logging.DEBUG)
	log.addHandler(handler)

	while True:	
		yield log_stream.getvalue()
		# "flush" the stream, move the seek/truncate points to 0
		log_stream.seek(0)
		log_stream.truncate(0)

		sleep(0.1)

@APP.route('/log/', methods=['GET'])
def log():
	# returns logging information
	return flask.Response(flask_logger(), mimetype="text/plain", content_type="text/event-stream")

# /////////////


if __name__ == '__main__':
	APP.debug=True
	APP.run(host="0.0.0.0", port=f'{ APP.config["PORTNUMBER"] }', threaded=True)
