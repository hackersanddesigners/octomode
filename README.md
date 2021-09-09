# pad2pdf 

work-in-process, collaborative editing space for PDF making using pads (<> Ethertoff http://osp.kitchen/tools/ethertoff/ <> Etherbox https://networksofonesown.constantvzw.org/ <> JupyterPi https://git.xpub.nl/XPUB/jupyterpi)

## Install a new instance on the server

`git clone https://git.vvvvvvaria.org/mb/pad2pdf.git`

`cd pad2pdf`

`python3 -m venv venvfolder`

`source ./venvfolder/bin/activate`

`pip install -r requirements.txt`

update the pad links in the templates, see `templates/`

Then: 

* init etherpump (`etherpump init`)
* configure the webserver to listen to the port of the flask application, for example with a subdomain (`cp /etc/nginx/sites-enabled/previousexample.vvvvvvaria.org.conf /etc/nginx/sites-enabled/new.vvvvvvaria.org.conf`)
* expand the current https certificate for this subdomain, using Letsencrypt 
* restart nginx (`sudo service reload nginx`)
* to keep the flask application running in the background: add the new instance of pad2pdf to supervisor (`cp /etc/supervisor/conf.d/previousexample.conf new.conf`)
* restart supervisor (`sudo service reload supervisor`)

and then:

go to the URL in the browser!

# Refs

http://typotheque.le75.be/