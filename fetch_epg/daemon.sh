#!/bin/bash
uwsgi --http :9100 --pythonpath $(pwd) --wsgi-file fetch_epgd.py
