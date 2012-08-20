#!/bin/bash
uwsgi --http :9090 --pythonpath $(pwd)/starfishd/ --wsgi-file starfishd/starfishd.py
