# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.http import HttpResponse
from jsonschema import validate
import os
import json
from django.conf import settings
import discovery
from data101 import DumpdataProvider

def getTemplateLink(name, request):
  return name + '.' + request.GET.get('format', 'json')

def format_render(request, response, template):
  format = request.GET.get('format', 'json')

  content_types = {
    'html': 'text/html',
    'ttl': 'text/turtle;charset=utf-8',
    'rdf': 'application/rdf+xml'
  }

  path_uri = request.path_info
  if path_uri == '/discovery':
      path_uri += '/'
  path_uri = path_uri.replace('/discovery/', '', 1)

  response['uri'] = (discovery.base_uri + path_uri).decode('utf_8')
  if response['uri'].endswith('/'):
    response['uri'] = response['uri'][:-1]

  if format == 'json':
    return HttpResponse(json.dumps(response), content_type='application/json')

  elif format == 'jsonp':
    callback = request.GET.get('callback', 'callback')
    return HttpResponse(callback + '(' + json.dumps(response) + ')')

  else:
    return render(request, "{0}.{1}".format(template, format), response, content_type=content_types[format])


#possible entry points
def serveFileFragment(request, namespace, member, path, file, fragment):
    if path is None:
        path = ''

    print namespace, member, path, file, fragment

    response = discovery.discoverFileFragment(namespace, member,
                                          path, file, fragment)

    if request.GET.get('validate', None):
        validate(response, json.load(open(os.path.abspath('../../schemas/101repo_fragment.json'), 'r')))

    return format_render(request, response, 'fragment')


def serveMemberFile(request, namespace, member, path, file):

    if path is None:
        path = ''

    response = discovery.discoverMemberFile(namespace, member,
                                            path, file)

    if request.GET.get('validate', None):
        validate(response, json.load(open(os.path.abspath('../../schemas/101repo_file.json'), 'r')))

    return format_render(request, response, 'folder')

def serveMemberPath(request, namespace, member, path):

    #needed for strange files, that have no . ! e.g. "Makefile"
    #This is also the reason why serveMemberPath doesn't need a check if a path exists, because non existing paths will
    #be classified as files first!!!
    if not DumpdataProvider.isDir(os.path.join(namespace, member, path)):
        path = os.path.dirname(path)
        file = os.path.basename(path)
        return serveMemberFile(request, namespace, member, path, file)

    response = discovery.discoverMemberPath(namespace, member,
                                            path)

    if request.GET.get('validate', None):
        validate(response, json.load(open(os.path.abspath('../../schemas/101repo_folder.json'), 'r')))

    return format_render(request, response, 'folder')


def serveNamespaceMember(request, namespace, member):
    response = discovery.discoverNamespaceMember(namespace, member)

    return format_render(request, response, 'folder')

def serveNamespace(request, namespace):
    response = discovery.discoverNamespace(namespace)

    if request.GET.get('validate', None):
        validate(response, json.load(open(os.path.abspath('../../schemas/101repo_namespace.json'), 'r')))

    return format_render(request, response, 'namespace')

def serveAllNamespaces(request):
    if 'wikititle' in request.GET.keys():
        redirectUrl = discovery.createRedirectUrl(request.GET['wikititle'])
        if 'format' in request.GET.keys():
            redirectUrl += '?format=' + request.GET['format']
            if request.GET.get('callback', ''):
                redirectUrl += '&callback=' + request.GET['callback']
        return redirect(redirectUrl)


    response = discovery.discoverAllNamespaces()

    if request.GET.get('validate', False):
        validate(response, json.load(open(os.path.abspath('../../schemas/101repo_namespace.json'), 'r')))

    return format_render(request, response, 'root')
