#!/bin/bash
uwsgi --http :9090 --pythonpath /home/simsun/starfish/src/starfishd/ --wsgi-file starfishd/starfishd.py
