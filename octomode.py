import os
import json
from flask import Flask, request, render_template, redirect, url_for
from urllib.request import urlopen
from urllib.parse import urlencode

# To sanitize Flask input fields
from markupsafe import Markup, escape

# To sanitize Markdown input
import pypandoc
# import bleach

# To read the Markdown metadat
import markdown

APP = Flask(__name__)
APP.config.from_pyfile('settings.py')

# ---

def get_pad_content(pad_name, ext=""):
    if ext:
        pad_name = f'{ pad_name }{ ext }'

    print(pad_name)

    arguments = { 
        'padID' : pad_name,
        'apikey' : APP.config['PAD_API_KEY']
    }
    api_call = 'getText'
    response = json.load(urlopen(f"{ APP.config['PAD_API_URL'] }/{ api_call }", data=urlencode(arguments).encode()))

    # create pad in case it does not yet exist
    if response['code'] == 1 and 'padID does not exist' == response['message']:
        api_call = 'createPad'
        urlopen(f"{ APP.config['PAD_API_URL'] }/{ api_call }", data=urlencode(arguments).encode())
        api_call = 'getText'
        response = json.load(urlopen(f"{ APP.config['PAD_API_URL'] }/{ api_call }", data=urlencode(arguments).encode()))

    content = response['data']['text']
    return content

def all_pads():
    arguments = { 
        'apikey' : APP.config['PAD_API_KEY'],
    }
    api_call = 'listAllPads'
    response = json.load(urlopen(f"{ APP.config['PAD_API_URL'] }/{ api_call }", data=urlencode(arguments).encode()))

    return response

def create_pad_on_first_run(name, ext):
    pads = all_pads()
    pad = name+ext

    if pad not in pads['data']['padIDs']:

        # Select default template
        if 'md' in ext:
            default_template = 'templates/default.md'
        elif 'css' in ext:
            default_template = 'templates/default.css'
        default_template = open(default_template).read()

        # Create pad and add the default template
        arguments = { 
            'padID' : pad,
            'apikey' : APP.config['PAD_API_KEY'],
            'text' : default_template
        }
        api_call = 'createPad'
        json.load(urlopen(f"{ APP.config['PAD_API_URL'] }/{ api_call }", data=urlencode(arguments).encode()))

def md_to_html(md_pad_content):
    # Convert Markdown to HTML
    # html = markdown.markdown(md_pad_content, extensions=['meta', 'attr_list']) # attr_list does not work
    html = pypandoc.convert_text(md_pad_content, 'html', format='md')

    # Sanitize the Markdown
    # html = bleach.clean(html)

    # Another built-in Flask way to sanitize
    # html = escape(html) 
    html = Markup(html)

    return html

def get_md_metadata(md_pad_content):
    # Read the metadata from the Markdown
    md = markdown.Markdown(extensions=['meta'])
    md.convert(md_pad_content)
    metadata = md.Meta

    return metadata

# ---

@APP.route('/', methods=['GET', 'POST'])
def index():
    name = False
    if request.values.get('name'):
        name = escape(request.values.get('name')) # Returns a Markup() object, which is "None" when False
    if name: 
        # This is when the environment is "created"
        # The pads are filled with the default templates (pad, stylesheet, template)
        exts = ['.md', '.css']
        for ext in exts:
            create_pad_on_first_run(name, ext)
        return redirect(url_for("pad", name=name))
    else:
        return render_template('start.html', pad_url=APP.config['PAD_URL'])

@APP.route('/<name>/')
def main(name):
    return redirect(url_for("pad", name=name))

@APP.route('/<name>/pad/')
def pad(name):
    url = f"{ APP.config['PAD_URL'] }/{ name }.md"
    return render_template('iframe.html', url=url, name=name.strip(), pad_url=APP.config['PAD_URL'])

@APP.route('/<name>/stylesheet/')
def stylesheet(name):
    url = f"{ APP.config['PAD_URL'] }/{ name }.css"
    return render_template('iframe.html', url=url, name=name.strip(), pad_url=APP.config['PAD_URL'])

@APP.route('/<name>/html/')
def html(name):
    # only here we need application root to make all the URLs work.....
    if APP.config['APPLICATION_ROOT'] == '/':
        app_root = ''
    elif APP.config['APPLICATION_ROOT'].endswith('/'):
        app_root = APP.config['APPLICATION_ROOT'][:-1]
    else:
        app_root = APP.config['APPLICATION_ROOT']
    url = f"{ app_root }/{ name }/preview.html"
    return render_template('iframe.html', url=url, name=name.strip(), pad_url=APP.config['PAD_URL'])

@APP.route('/<name>/pdf/')
def pdf(name):
    # only here we need application root to make all the URLs work.....
    if APP.config['APPLICATION_ROOT'] == '/':
        app_root = ''
    elif APP.config['APPLICATION_ROOT'].endswith('/'):
        app_root = APP.config['APPLICATION_ROOT'][:-1]
    else:
        app_root = APP.config['APPLICATION_ROOT']
    url = f"{ app_root }/{name}/pagedjs.html"
    return render_template('pdf.html', url=url, name=name.strip(), pad_url=APP.config['PAD_URL'])

# //////////////////
# RENDERED RESOURCES 
# //////////////////
# (These are not saved as a file on the server)

@APP.route('/<name>/stylesheet.css')
def css(name):
    css = get_pad_content(name, '.css')
    # Insert CSS sanitizer here.

    return css, 200, {'Content-Type': 'text/css; charset=utf-8'}

@APP.route('/<name>/preview.html')
def preview(name):
    # TO GENERATE THE PREVIEW WEBPAGE
    md_pad_content = get_pad_content(name, ext='.md')
    html = md_to_html(md_pad_content)
    metadata = get_md_metadata(md_pad_content)
    if metadata:
        lang = metadata['language'][0]
        title = metadata['title'][0]
    else:
        lang = "en"
        title = "No title"

    return render_template('preview.html', name=name.strip(), pad_content=html, lang=lang, title=title)

@APP.route('/<name>/pagedjs.html')
def pagedjs(name):
    # TO GENERATE THE PAGED.JS WEBPAGE
    md_pad_content = get_pad_content(name, ext='.md')
    html = md_to_html(md_pad_content)
    metadata = get_md_metadata(md_pad_content)
    lang = metadata['language'][0]
    title = metadata['title'][0]

    return render_template('pagedjs.html', name=name.strip(), pad_content=html, lang=lang, title=title)

# //////////////////

if __name__ == '__main__':
    APP.debug = True
    APP.env = "development"
    APP.run(host="0.0.0.0", port=APP.config["PORTNUMBER"], threaded=True)