heroku buildpacks:clear
heroku buildpacks:add --index heroku/python
heroku buildpacks:add --index 1 heroku-community/apt
heroku ps:scale web=1

web:python app.py