#!/usr/bin/env python
# coding=utf-8

import json
import os
from inflection import camelize
import re

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def run(context):
    with open(os.path.join(context.get_env('dumps101dir'), 'pages.json')) as f:
        allPages = json.load(f)['pages']


    wikilink_rx = re.compile(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]')
    result = []
    for p in allPages:
        content = p['raw_content']
        title = p['namespace'] + ':' + p['title']

        sections = re.split('== *([0-9 a-zA-Z]+) *==', content)

        page = {
            'title': title.strip(),
            'sections': {}
        }
        sections = list(filter(bool, sections))

        for data in chunks(sections, 2):
            if len(data) == 2:
                content = wikilink_rx.sub(r'\1', data[1])
                paragraphs = []
                while len(content) > 0:
                    pre = content.find('<pre>')
                    syntaxhighlight = content.find('<syntaxhighlight')

                    if pre != -1 and pre != 0:
                        paragraphs.append({
                            'classifier': 'text',
                            'content':  content[:content.find('<pre>') + len('<pre>')]
                        })

                    elif syntaxhighlight != -1 and syntaxhighlight > 0:
                        paragraphs.append({
                            'classifier': 'syntaxhighlight',
                            'content':  content[:content.find('<syntaxhighlight') + len('<syntaxhighlight')]
                        })

                    if pre != -1 and syntaxhighlight != -1:
                        if pre > syntaxhighlight:
                            paragraphs.append({
                                'classifier': 'pre',
                                'content': content[pre:content.find('</pre>') + len('</pre>')]
                            })
                            content = content[content.find('</pre>')+ len('</pre>'):]

                        else:
                            paragraphs.append({
                                'classifier': 'syntaxhighlight',
                                'content': content[syntaxhighlight:content.find('</syntaxhighlight>') +  + len('</syntaxhighlight>')]
                            })
                            content = content[content.find('</syntaxhighlight>')+ len('</syntaxhighlight>'):]

                    elif pre != -1:
                        paragraphs.append({
                            'classifier': 'pre',
                            'content': content[pre:content.find('</pre>') + len('</pre>')]
                        })
                        content = content[content.find('</pre>') + len('</pre>'):]

                    elif syntaxhighlight != - 1:
                        paragraphs.append({
                            'classifier': 'syntaxhighlight',
                            'content': content[syntaxhighlight:content.find('</syntaxhighlight>') + len('</syntaxhighlight>')]
                        })
                        content = content[content.find('</syntaxhighlight>') + len('</syntaxhighlight>'):]

                    else:
                        paragraphs.append({
                            'classifier': 'text',
                            'content': content
                        })
                        content = ''

                    content = content.strip()

                    # print(title)
                    # print(content)
                    # print(paragraphs)
                    # input()

                page['sections'][data[0].strip()] = paragraphs

        result.append(page)

    context.write_dump('wiki-content', result)
