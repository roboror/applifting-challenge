#!/bin/bash
set +xe

HEROKU_APP_NAME="${HEROKU_APP_NAME:applifting-challenge-schonfeld}"

heroku login
heroku container:login

heroku container:push web --app="$HEROKU_APP_NAME"
heroku container:release web --app="$HEROKU_APP_NAME"

heroku open --app="$HEROKU_APP_NAME"
heroku logs --tail --app="$HEROKU_APP_NAME"