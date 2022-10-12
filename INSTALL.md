# Install octomode

## Step 1

Download the octomode code from the Varia git.

First go to the location where you want to install octomode. This should be outside of the public webserver folders, as we will have to save an API key of the etherpad at some point, and you don't want to share that key in public. Also, switch to the root user for this step.

`$ cd /srv/`
`$ sudo su`
`# git clone https://git.vvvvvvaria.org/varia/octomode.git`

## Step 2

We will make an "octomode" user on the server to run octomode with this user. In this way we can restrict the access of this user to the rest of the server. It's a way to make sure that the pads in octomode cannot be used to write code in a specific way, that it can be executed on the server.
Make a system user called "octomode".

`# useradd --system --no-create-home --shell=/sbin/nologin octomode`

Give read and write access + ownership to the `/srv/octomode` folder to the octomode user.

`# chown -R octomode:octomode /srv/octomode`
`# chmod -R u+rw /srv/octomode`

To handle the limited folder access, i'm not sure what to do. 
Maybe a so called `chroot` can be used? 
Asking for advice here: https://git.vvvvvvaria.org/varia/octomode/issues/2#issuecomment-757

## Step 3

Install the dependencies that octomode uses.
First make sure that `pip3` and `pandoc` is installed. On debian you can install it by running: 

`$ sudo apt install python3-venv pandoc`

There is a Makefile in the octomode folder, which can be used to install the dependencies. First navigate to the octomode folder and then run `make setup`.

`# cd /srv/octomode`
`# make setup`

Change the ownership of the installed dependencies to octomode.

`# chown -R octomode:octomode .venv`

## Step 4

Get the API key of the etherpad you want to use. This can be a local one which is running on the same server, or an etherpad that is running somewhere else.

`# cat /srv/etherpad-lite/APIKEY.txt`

Copy the key and save it in the file `/srv/octomode/config.py` as "PAD_API_KEY".

`# cd /srv/octomode/`
`# nano config.py`

Also change the "PAD_URL" and "PAD_API_URL".

You can also change the "PORTNUMBER", this is the port at which octomode will be running. You can change it to any port number that is not used yet on the server.

Close and save the `config.py` file with `[CTRL+X]`, `[Y]`, `[ENTER]`.

## Step 5

Try to run octomode, to see if it works!

`# make run`

If you are currently in the same local network as rosa, you can visit rosa's ip address on port 5001. http://192.168.178.58:5001

Try to visit all the different "modes": `pad`, `stylesheet`, `html` and `pdf`, to make sure that they all work.

You can stop the application with `[CTRL+C]`.

## Step 6

Run octomode as a background service.

Octomode is written in Flask, a python library to make web applications. It needs to run all the time in order to be available for people to use.

We will make a system d `.service` file for this.

https://blog.miguelgrinberg.com/post/running-a-flask-application-as-a-service-with-systemd

Make a `.service` file for octomode:

`# nano /etc/systemd/system/octomode.service`

Paste the following configurations in the file:

```
    [Unit]
    Description=Collective PDF rendering environment
    After=network.target
    
    [Service]
    User=octomode  
    WorkingDirectory=/srv/octomode     
    ExecStart=/srv/octomode/.venv/bin/python octomode.py
    Restart=always    

    [Install]
    WantedBy=multi-user.target
```

Reload the systemd daemon:

`# systemctl daemon-reload`

And start the octomode service.

`# systemctl start octomode`

Check if it works by visiting http://192.168.178.58:5001/ again!

## Step 7

Connect octomode to an URL.

To access octomode through an URL, like https://rosa.vvvvvvaria.org/octomode/, a mapping is needed to route octomode's port 5001 to the URL that will be used.

In nginx, we can use a proxy_jump for this.

Open the nginx configuration file.

`# cd /etc/nginx/sites-enabled`
`# nano default`

Add the following setting to the nginx file.

```
    location /octomode { 
        proxy_pass         http://127.0.0.1:5001;
    }
    # Serve the /static/ folder nginx (instead of Flask)
    # as this Flask installation runs outside the root URL
    location ^~ /static/  {
        alias /srv/octomode/static/;
    }
```

Change the permissions of the `/srv/octomode/static/` folder, as this folder will be served by nginx.

`# chown -R www-data:www-data /srv/octomode/static/`
`# chmod -R g+w /srv/octomode/static/`

Check if you configuarion is oke.

`# nginx -t`

If so, then reload nginx.

`# service nginx reload`

See if it works by visiting <http://192.168.178.58/octomode/>.