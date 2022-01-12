# Octomode 

*work-in-process*

Octomode is a collective editing space for PDF making, using Etherpad, Etherdump, Paged.js and Flask. 

## Install octomode

`git clone https://git.vvvvvvaria.org/mb/octomode.git`

`cd octomode`

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install -r requirements.txt`

Then: 

* init etherpump (`etherpump init`)
* configure the webserver to listen to the port of the flask application, for example with a subdomain
* expand the current https certificate for this subdomain
* restart nginx (`sudo service reload nginx`)
* to keep the flask application running in the background: add a new config to supervisor (`cp /etc/supervisor/conf.d/previousexample.conf new.conf`)
* restart supervisor (`sudo service reload supervisor`)

# Refs

* Ethertoff http://osp.kitchen/tools/ethertoff/ by OSP
* Etherbox https://networksofonesown.constantvzw.org/ by Michael Murtaugh/Constant
* Etherdump https://gitlab.constantvzw.org/aa/etherdump by Michael Murtaugh/Constant
* Pad2Print https://gitlab.com/Luuse/pad2print by Luuse
* JupyterPi https://git.xpub.nl/XPUB/jupyterpi by Michael Murtaugh/XPUB