from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls import url
import requests
import requests_cache
import os
import json

rcache=os.environ.get("CACHE", "sqlite")

requests_cache.install_cache('webseed_cache', backend=rcache)
DEBUG = True
ROOT_URLCONF = 'webseed'
ALLOWED_HOSTS = '*'
DATABASES = {'default': {}}
KEY=os.environ.get("KEY")
SECRET_KEY = "not so secret"
API_URL="https://api.1fichier.com/v1/download/get_token.cgi"


def index(request):
    id = request.GET.get("id")
    headers = {'Authorization': "Bearer {}".format(KEY)}
    data = {'url':"https://1fichier.com/?{}".format(id),'inline':1}
    res = requests.post(API_URL,json=data, headers=headers)
    res_json = res.json()
    url = res_json.get("url")
    if url:
        return HttpResponseRedirect(url)
    else:
        return HttpResponse(json.dumps(res_json),content_type="application/json")

urlpatterns = [
    url(r'^$', index)
]



# run with djagno dev server
# $ PYTHONPATH=. django-admin.py runserver 0.0.0.0:8000 --settings=pico_django

# for example run with uwsgi
# `$ uwsgi --http :8000 -M --pythonpath=. --env CACHE=REDIS --env DJANGO_SETTINGS_MODULE=webseed -w "django.core.handlers.wsgi:WSGIHandler()"`