# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.http import HttpResponse
from jsonschema import validate
import os
import json
from django.conf import settings
import discovery
from data101 import DumpdataProvider


# #helper which does some stuff that's always needed
# def initServeRequest(host):
#     import discovery
#     #setting the base uri - either localhost for developing/debugging or the real 101companies.org/resources url
#     discovery.base_uri = 'http://101companies.org/resources'

#     if 'localhost' in host:
#         discovery.base_uri = 'http://' + host + '/discovery'

# def renderJSON(kwargs):
#     response = kwargs['response']

#     return {
#         'text': json.dumps(response),
#         'content_type': 'text/json;charset=utf-8'
#     }

# def renderJSONP(kwargs):
#     callback = kwargs['callback']

#     return {
#         'text': callback + '(' + render('json', **kwargs)['text'] + ')',
#         'content_type': 'application/javascript'
#     }

# def renderHTML(kwargs):
#     response = kwargs['response']
#     request = kwargs['request']
#     template = kwargs['htmltemplate']


#     if 'content' in response:
#         from xml.sax.saxutils import escape
#         response['content'] = escape(response['content'])

#     import discovery

#     #base URI, needed for static urls
#     if 'localhost' in discovery.base_uri: response['static_uri'] = discovery.base_uri.replace('/discovery','', 1)
#     else: response['static_uri'] = 'http://worker.101companies.org/services'

#     response['uri'] = (discovery.base_uri + request.path_info.replace('/discovery', '', 1))#.decode('utf_8')
#     if response['uri'].endswith('/'):
#         response['uri'] = response['uri'][:-1]

#     return {
#         'text': str(template.render(response).encode('utf_8') ),
#         'content_type': 'text/html'
#     }

# def renderRDF(kwargs):
#     response = kwargs['response']
#     request = kwargs['request']
#     template = kwargs['rdftemplate']


#     response['about'] = 'http://101companies.org/resources' + request.path_info.replace('/discovery','', 1)

#     if 'content' in response:
#         from xml.sax.saxutils import escape
#         response['content'] = escape(response['content'])
#     if 'endpoint' in response:
#         response['endpoint'] = response['endpoint'].replace('&', '&amp;')

#     from templates import TemplateProvider
#     template = TemplateProvider.getTemplate(template)

#     return {
#         'text': str(template.render(response)),
#         'content_type': 'application/rdf+xml'
#     }

# def renderTurtle(kwargs):
#     #start_response = kwargs['start_response']
#     response = kwargs['response']
#     request = kwargs['request']
#     template = kwargs['ttltemplate']

#     response['about'] = 'http://101companies.org/resources' + request.path_info.replace('/discovery','', 1)

#     if 'content' in response:
#         from xml.sax.saxutils import escape
#         response['content'] = escape(response['content'])
#     if 'endpoint' in response:
#         response['endpoint'] = response['endpoint'].replace('&', '&amp;')

#     from templates import TemplateProvider
#     template = TemplateProvider.getTemplate(template)

#     return {
#         'text': str(template.render(response)),
#         'content_type': 'text/turtle;charset=utf-8'
#     }

# def render(f, **kwargs):
#     print f
#     m = {
#         'json' : renderJSON,
#         'jsonp': renderJSONP,
#         'html' : renderHTML,
#         'rdf'  : renderRDF,
#         'ttl'  : renderTurtle
#     }.get(f, renderJSON)
#     return m(kwargs)

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
