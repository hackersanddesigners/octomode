SHELL := /bin/bash

default: run

setup:
	@if [ ! -d ".venv" ]; then python3 -m venv .venv && .venv/bin/pip install -r requirements.txt; fi

config:
	@set -a
	@source config.env
	@set +a

run: config
	@.venv/bin/python octomode.py
