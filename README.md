# pad2pdf 

work-in-progressssss


work-in-process, collaborative editing space for PDF making using pads (<> Ethertoff project http://osp.kitchen/tools/ethertoff/ <> JupyterPi https://git.xpub.nl/XPUB/jupyterpi)


## Install a new instance on the server

`git clone https://git.vvvvvvaria.org/mb/pad2pdf.git`

`cd pad2pdf`

`python3 -m venv venvfolder`

`source ./venvfolder/bin/activate`

`pip install -r requirements.txt`

`python3 start.py`

Then: configure the webserver to listen to the port of the flask application, for example with a subdomain.
