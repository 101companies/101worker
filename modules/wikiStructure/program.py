def run(env):
    wiki_dump = env.read_dump('wiki-links')

    pages = wiki_dump['wiki']['pages']
    
    pagelist = ['Software language']
    result = [['Software language','']]

    while(pagelist):
        key = pagelist.pop(0)
    
        for p in pages:
            isA = p.get('IsA')
            if isA is not None:
                for x in isA:
                    if x['n'] == key:
                        ###                        
                        pagelist.append(p['n'])
                        ###                        
                        result.append([p['n'], key])

            instanceOf = p.get('InstanceOf')
            if instanceOf is not None:
                for x in instanceOf:
                    if x['n'] == key:
                        pagelist.append(p['n'])
                        result.append([p['n'], key])
 
    env.write_dump('wiki-structure', {"structure":result})


