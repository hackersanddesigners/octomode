# Octomode 

*work-in-process*

Octomode is a collective editing space for PDF making, using Etherpad, Paged.js and Flask. 

## Use octomode locally

`make setup` (sets up a virtual environment and install the requirements)

`make run` (runs the Flask application)

Open the application at <http://localhost:5001>.

## Dependencies

`python` dependencies are listed in `requirements.txt`

`system` dependencies are:

* `pandoc` >= `2.2.2`

## Use octomode on a server

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

# snapshots

![](snapshots/breakybreaky-in-octomode-1.png)
![](snapshots/breakybreaky-in-octomode-2.png)
![](snapshots/breakybreaky-in-octomode-3.png)
![](snapshots/breakybreaky-in-octomode-4.png)