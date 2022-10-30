# Octomode

> *work-in-progress*

Octomode is a collective editing space for PDF making, using Etherpad, Paged.js and Flask.

## How to use Octomode?

If you want to work collectively on making a PDF, you can use octomode. There is an instance installed here: <https://octomode.vvvvvvaria.org/>. You can write any name of in the input field, this will create a new octomode environment.

Working in octomode includes:

* `pad`: all materials for the PDF are collected here. (written in Markdown)
* `stylesheet`: all CSS rules for the PDF are collected here (written in CSS)
* `html`: render the lay out as a HTML (rendered with PyPandoc)
* `pdf`: render the lay out as a PDF (rendered with Paged.js)

When creating a new environment, a few things happen:

* a pad is created for collecting the materials of your PDF. The name of the octomode environment will become the name of this pad. For example: `http://pad.vvvvvvaria.org/NAME.md`.
* another pad is created for writing the stylesheet of your PDF. The name of the octomode environment will become the name of this pad, followed by .css. For example: `https://pad.vvvvvvaria.org/NAME.css`
* If both pads were not created yet, a template is added to the pad. The main pad will get a Markdown template and the stylesheet pad a CSS template.

In case a pad was already made, you can copy the templates below and paste them at the top of your pads.

The PDFs are rendered using [Paged.js](https://pagedjs.org/), a free and open source JavaScript library "that paginates content in the browser to create PDF output from any HTML content. This means you can design works for print (eg. books) using HTML and CSS!" The project is maintained by the [Coko Foundation](https://coko.foundation/). Paged.js adds features to the CSS3 standards, expanding the possibilities to make lay outs for specific sections, place content in the margins of pages, and render indexes (amonst other things). The documentation is very ufesul and can be found here: <https://pagedjs.org/documentation/>.

### Octomode Markdown template

```
---
title: tentacular thinking
language: en
---

# tentacular thinking
```

### Octomode CSS template

```
@charset "utf-8";

@page{
    size: A5;
}

@page:first{
    background-color: pink;
}

body{
    color: green;
}

section#cover{
    page-break-after: always;
}
```

### Note

When working with multiple people on one PDF it is recommended to use the same browser. CSS rules are rendered slightly differently on different browsers.

## Continuums

Octomode resonates other software practices based on pad-to-PDF workflows or collective infrastructure, including:

* wiki-to-PDF http://titipi.org/wiki/index.php/Wiki-to-pdf by Martino Morandi/TITiPI
* Living Glossary Enviroment http://tool.attempt.press/ by Camilo Garcia/Attempt
* Ethertoff http://osp.kitchen/tools/ethertoff/ by OSP
* Etherbox https://networksofonesown.constantvzw.org/ by Michael Murtaugh/Constant
* Etherdump https://gitlab.constantvzw.org/aa/etherdump by Michael Murtaugh/Constant
* Pad2Print https://gitlab.com/Luuse/pad2print by Luuse

## Install octomode

You can clone this repository to run octomode on your own computer or server.

`git clone https://git.vvvvvvaria.org/varia/octomode.git`

`cd octomode`

`make setup` (sets up a virtual environment and install the requirements, you only need to do this once)

Then you can configure your environment.

You can do this in two ways:

* by editing the `config.env` file
* by storing the configuration settings as *environment variables* before running octomode:

```
$ export OCTOMODE_PORTNUMBER=XXX
$ export OCTOMODE_PAD_URL=XXX
$ export OCTOMODE_PAD_API_URL=XXX
$ export OCTOMODE_PAD_API_KEY=XXX
```

- **OCTOMODE_PORTNUMBER**: *optional*, default: `5001`
- **OCTOMODE_PAD_URL**: *optional*, default: `https://pad.vvvvvvaria.org/`
- **OCTOMODE_PAD_API_URL**: *optional*, default: `https://pad.vvvvvvaria.org/api/1.2.15/`
- **OCTOMODE_PAD_API_KEY**: *required*, **no default**

(Note: You must provide a value for `OCTOMODE_PAD_API_KEY`.)

`make run` (runs the Flask application)

Open the application at port `5001`, for example: <http://localhost:5001> or <http://111.111.111.111:5001>.

### Dependencies

`python` dependencies are listed in `requirements.txt`

To install them, you can run:

`make setup`

This creates a virtual environment at `.venv/` and installs all the dependencies here.

### Other configurations on the server

* Configure the webserver to listen to the port of the flask application, for example with a subdomain
* Expand the current https certificate for a subdomain
* Restart nginx (`sudo service reload nginx`)
* To keep the flask application running in the background: add a new config to supervisor (`cp /etc/supervisor/conf.d/previousexample.conf /etc/supervisor/conf.d/new.conf`)
* Restart supervisor (`sudo service reload supervisor`)

## Use octomode locally

It's recommended to use Firefox when working with octomode locally. Chrome or Chromium do not load external etherpads in iframes.

## Snapshots

![](snapshots/breakybreaky-in-octomode-1.png)
![](snapshots/breakybreaky-in-octomode-2.png)
![](snapshots/breakybreaky-in-octomode-3.png)
![](snapshots/breakybreaky-in-octomode-5.png)
