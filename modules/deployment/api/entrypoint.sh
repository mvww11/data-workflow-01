#!/bin/bash

cp -r /data-workflow-01/modules/ds/models/ /
pip install flask
python /data-workflow-01/modules/deployment/api/app.py
/bin/bash