import json
import sys
import os
from django.shortcuts import redirect, render

os.chdir(os.path.dirname(__file__))

import requests
from django.http import HttpResponse, HttpResponseNotAllowed

def index(request):
    with open(os.path.abspath('../../../101logs/worker.log')) as f:
        data = json.load(f)

    return render(request, 'index.html', { 'errors': data })
