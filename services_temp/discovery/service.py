# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse

#helper which does some stuff that's always needed
def initServeRequest(host):
    import discovery
    #setting the base uri - either localhost for developing/debugging or the real 101companies.org/resources url
    discovery.base_uri = 'http://101companies.org/resources'

    if 'localhost' in host:
        discovery.base_uri = 'http://' + host + '/discovery'

def renderJSON(kwargs):
    response = kwargs['response']

    import json


    return {
        'text': json.dumps(response),
        'content_type': 'text/json;charset=utf-8'
    }

def renderJSONP(kwargs):
    callback = kwargs['callback']

    return {
        'text': callback + '(' + render('json', **kwargs)['text'] + ')',
        'content_type': 'application/javascript'
    }

def renderHTML(kwargs):
    response = kwargs['response']
    request = kwargs['request']
    template = kwargs['htmltemplate']


    if 'content' in response:
        from xml.sax.saxutils import escape
        response['content'] = escape(response['content'])

    import discovery

    #base URI, needed for static urls
    if 'localhost' in discovery.base_uri: response['static_uri'] = discovery.base_uri.replace('/discovery','', 1)
    else: response['static_uri'] = 'http://worker.101companies.org/services'

    response['uri'] = (discovery.base_uri + request.path_info.replace('/discovery', '', 1))#.decode('utf_8')
    if response['uri'].endswith('/'):
        response['uri'] = response['uri'][:-1]

    from templates import TemplateProvider
    template = TemplateProvider.getTemplate(template)

    return {
        'text': str( template.render( response ).encode('utf_8') ),
        'content_type': 'text/html'
    }

def renderRDF(kwargs):
    response = kwargs['response']
    request = kwargs['request']
    template = kwargs['rdftemplate']


    response['about'] = 'http://101companies.org/resources' + request.path_info.replace('/discovery','', 1)

    if 'content' in response:
        from xml.sax.saxutils import escape
        response['content'] = escape(response['content'])
    if 'endpoint' in response:
        response['endpoint'] = response['endpoint'].replace('&', '&amp;')

    from templates import TemplateProvider
    template = TemplateProvider.getTemplate(template)

    return {
        'text': str(template.render(response)),
        'content_type': 'application/rdf+xml'
    }

def renderTurtle(kwargs):
    #start_response = kwargs['start_response']
    response = kwargs['response']
    request = kwargs['request']
    template = kwargs['ttltemplate']

    response['about'] = 'http://101companies.org/resources' + request.path_info.replace('/discovery','', 1)

    if 'content' in response:
        from xml.sax.saxutils import escape
        response['content'] = escape(response['content'])
    if 'endpoint' in response:
        response['endpoint'] = response['endpoint'].replace('&', '&amp;')

    from templates import TemplateProvider
    template = TemplateProvider.getTemplate(template)

    return {
        'text': str(template.render(response)),
        'content_type': 'text/turtle;charset=utf-8'
    }

def render(f, **kwargs):
    print f
    m = {
        'json' : renderJSON,
        'jsonp': renderJSONP,
        'html' : renderHTML,
        'rdf'  : renderRDF,
        'ttl'  : renderTurtle
    }.get(f, renderJSON)
    return m(kwargs)

#possible entry points
def serveFileFragment(request, namespace, member, path, file, fragment):
    initServeRequest(request.META['HTTP_HOST'])
    import discovery
    
    if path is None:
        path = ''

    print namespace, member, path, file, fragment

    response = discovery.discoverFileFragment(namespace, member,
                                          path, file, fragment)

    result = render(request.GET.get('format', 'json'),
                   request = request,
                   response=response,
                   callback=request.GET.get('callback', 'callback'),
                   rdftemplate = 'fragment.rdf',
                   htmltemplate = 'fragment.html',
                   ttltemplate = "fragment.ttl"
    )
    return HttpResponse(result['text'], result['content_type'])


def serveMemberFile(request, namespace, member, path, file):
    initServeRequest(request.META['HTTP_HOST'])
    import discovery
    
    if path is None:
        path = ''

    response = discovery.discoverMemberFile(namespace, member,
                                            path, file)

    result = render(request.GET.get('format', 'json'),
                   response=response,
                   request=request,
                   callback=request.GET.get('callback', 'callback'),
                   rdftemplate = 'file.rdf',
                   htmltemplate = 'file.html',
                   ttltemplate = "file.ttl"
    )
    return HttpResponse(result['text'], content_type=result['content_type'])

def serveMemberPath(request, namespace, member, path):
    initServeRequest(request.META['HTTP_HOST'])
    import discovery
    from data101 import DumpdataProvider
    import os

    #needed for strange files, that have no . ! e.g. "Makefile"
    #This is also the reason why serveMemberPath doesn't need a check if a path exists, because non existing paths will
    #be classified as files first!!!
    if not DumpdataProvider.isDir(os.path.join(namespace, member, path)):
        path = os.path.dirname(path)
        file = os.path.basename(path)
        return serveMemberFile(request, namespace, member, path, file)

    response = discovery.discoverMemberPath(namespace, member,
                                            path)

    result = render(request.GET.get('format', 'json'),
                   request = request,
                   response=response,
                   callback=request.GET.get('callback', 'callback'),
                   rdftemplate = 'folder.rdf',
                   htmltemplate = 'folder.html',
                   ttltemplate = "folder.ttl"
    )
    
    return HttpResponse(result['text'], content_type=result['content_type'])


def serveNamespaceMember(request, namespace, member):
    initServeRequest(request.META['HTTP_HOST'])
    import discovery

    if '_' in member:
        member = member.replace('_', ' ')

    response = discovery.discoverNamespaceMember(namespace, member)

    result = render(request.GET.get('format', 'json'),
                   request=request,
                   response=response,
                   callback=request.GET.get('callback', 'callback'),
                   rdftemplate = 'folder.rdf',
                   htmltemplate = 'folder.html',
                   ttltemplate = "folder.ttl"
    )
    return HttpResponse(result['text'], content_type=result['content_type'])

def serveNamespace(request, namespace):
    initServeRequest(request.META['HTTP_HOST'])
    import discovery

    response = discovery.discoverNamespace(namespace)
    result = render(request.GET.get('format', 'json'),
                   request = request,
                   response=response,
                   callback=request.GET.get('callback', 'callback'),
                   rdftemplate = 'namespace.rdf',
                   htmltemplate = 'namespace.html',
                   ttltemplate = "namespace.ttl"
    )
    return HttpResponse(result['text'], content_type=result['content_type'])

def serveAllNamespaces(request):
    initServeRequest(request.META['HTTP_HOST'])
    import discovery

    if 'wikititle' in request.GET.keys():
        redirectUrl = discovery.createRedirectUrl(request.GET['wikititle'])
        if 'format' in params:
            redirectUrl += '?format=' + params['format']
            if params.get('callback', ''):
                redirectUrl += '&callback=' + params['callback']
        return redirect(redirectUrl)


    response = discovery.discoverAllNamespaces()
    
    f = request.GET.get('format', 'json')
    print f
    
    result = render(f,
                   request = request,
                   response=response,
                   callback=request.GET.get('callback', 'callback'),
                   rdftemplate = 'root.rdf',
                   htmltemplate = 'root.html',
                   ttltemplate = "root.ttl"
    )
    return HttpResponse(result['text'], content_type=result['content_type'])
    

#def routes():
#    return [
#        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)(/(?P<path>.*))?/(?P<file>.*\.[^/]+)/(?P<fragment>.+)', serveFileFragment),
#        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)(/(?P<path>.*))?/(?P<file>.*\.[^/]+)', serveMemberFile),
#        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)/(?P<path>.+)', serveMemberPath),
#        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)', serveNamespaceMember),
#        ( '/discovery/(?P<namespace>[^/]+)', serveNamespace),
#        ( '/discovery', serveAllNamespaces )
#    ]
