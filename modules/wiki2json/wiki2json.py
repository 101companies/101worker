#!/usr/bin/env python
# coding=utf-8

from pymongo import MongoClient
import json
import os

camelize = lambda words: ''.join(words[0].lower() + words[1:])

def extract_properties(internal_links):
  links = {}
  for link in internal_links:
    if not '::' in link: continue
    l = link.split('::')
    p = camelize(l[0]) #property
    n = l[1]
    if p in links: links[p].append(handle_page_name(n,{}))
    else: links[p] = [handle_page_name(n,{})]

  return links  

def handle_page_name(name, props):
  if name.startswith('http'):
    return name
  #print name
  n = name.split(':')
  if len(n) == 1:
    props['p'] = n[0]
    props['n'] = None
  else:
    props['p'] = n[0]
    props['n'] = n[1]
  return props

client = MongoClient('db.101companies.org', 27017)
db = client['wiki_production']

db.authenticate(os.environ['MONGODB_USER'], os.environ['MONGODB_PWD'])

allPages = []
for p in db.pages.find():
  if not p.has_key('page_title_namespace'):
      continue
  res = {'headline':'n/a'}
  handle_page_name(p['page_title_namespace'], res)

  if 'used_links' in p:
    res['internal_links'] = p['used_links']

    properties = extract_properties(res['internal_links']) 
    for k, v in properties.items():
      res[k] = v

  allPages.append(res)  

with open('dump.json', 'w') as f:
  f.write(json.dumps({'wiki':{'pageCount':len(allPages), 'pages':allPages}}, sort_keys=False))

#def url = 'http://101companies.org/endpoint/' + java.net.URLEncoder.encode(obj.label.replaceAll(' ', '_')) + '/summary'
#                        def json = getJSON(url)
#                        if (json != null){
#                            def sections = json.sections
#                            if ((sections != null) && (sections.size() > 0) && (sections[0].title == "Headline")){
#                                props['headline'] = sections[0].content.replaceAll("== Headline ==", "").replaceAll("==Headline==","")
#                            }
