#! make

include .env
export

default: local

setup:
	@if [ ! -d ".venv" ]; then python3 -m venv .venv && .venv/bin/pip install -r requirements.txt; fi

local:
	@.venv/bin/python octomode.py

action:
	@SCRIPT_NAME=${OCTOMODE_APPLICATION_ROOT} .venv/bin/gunicorn -b localhost:${OCTOMODE_PORTNUMBER} --reload octomode:APP
