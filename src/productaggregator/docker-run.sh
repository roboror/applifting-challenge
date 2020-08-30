#!/usr/bin/env bash
set -ex

flask db upgrade
gunicorn  --workers 4 --bind="0.0.0.0:${PORT}" "${FLASK_APP}"
#flask run --host=0.0.0.0 --port="${PORT}"
