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

def update_pad_contents(name, ext):
	# download the md pad + stylesheet + template pad
	pad_name = f'{ name }{ ext }'
	pad_content = get_pad_content(pad_name)

	return pad_content

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
	return flask.render_template('pad.html', pad_url=APP.config['PAD_URL'], name=name.strip(), ext=ext)

@APP.route('/<name>/pad/')
def pad(name):
	ext = '.md'
	create_pad_on_first_run(name, ext)
	return flask.render_template('pad.html', pad_url=APP.config['PAD_URL'], name=name.strip(), ext=ext)

@APP.route('/<name>/stylesheet/', methods=['GET'])
def stylesheet(name):
	ext = '.css'
	create_pad_on_first_run(name, ext)
	return flask.render_template('pad.html', pad_url=APP.config['PAD_URL'], name=name.strip(), ext=ext)

@APP.route('/<name>/template/', methods=['GET'])
def template(name):
	ext = '.template'
	create_pad_on_first_run(name, ext)
	return flask.render_template('pad.html', pad_url=APP.config['PAD_URL'], name=name.strip(), ext=ext)

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
	css = update_pad_contents(name, '.css')
	
	return css, 200, {'Content-Type': 'text/css; charset=utf-8'}

@APP.route('/<name>/pandoc-template.html')
def pandoc_template(name):
	template = update_pad_contents(name, '.template')
	
	return template, 200, {'Content-Type': 'text/html; charset=utf-8'}

@APP.route('/<name>/pagedjs.html')
def pagedjs(name):
	# update pad contents
	md = update_pad_contents(name, '.md')
	# generate html page with the pandoc template (with paged.js inserted in the header)
	# the pandoc template is loaded dynamically from /<name>/pandoc-template.html
	# Needs pandoc >2.2.2 for this!
	# https://github.com/jgm/pandoc/issues/5246
	pandoc_args = [
		'--toc',
		'--toc-depth=1',
		f'--template=http://localhost:5001/{ name }/pandoc-template.html',
		'--standalone'
	]
	html = pypandoc.convert_text(md, 'html', format='md', extra_args=pandoc_args)

	return html, 200, {'Content-Type': 'text/html; charset=utf-8'}

# /////////////


if __name__ == '__main__':
	APP.debug=True
	APP.run(host="0.0.0.0", port=f'{ APP.config["PORTNUMBER"] }', threaded=True)
