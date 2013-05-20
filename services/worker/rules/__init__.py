import json
import operator
import sys
import os
import re
import copy
import commands

def tag_rules(rules):
    rules = copy.copy(rules)
    for index, rule in enumerate(rules['results']['rules']):
        if rule['rule'].has_key('predicate'):
            rule['rule']['level'] = 10
     
        elif rule['rule'].has_key('fragment'):
            rule['rule']['level'] = 9   

        elif rule['rule'].has_key('content'):
            rule['rule']['level'] = 8   

        elif rule['rule'].has_key('basename'):
            rule['rule']['level'] = 5  

        elif rule['rule'].has_key('dirname'):
            rule['rule']['level'] = 1

        elif rule['rule'].has_key('suffix'):
            rule['rule']['level'] = 1

        elif rule['rule'].has_key('filename'):
            rule['rule']['level'] = 1

        else:
            rule['rule']['level'] = 11

        rules['results']['rules'][index] = rule
    
    return rules

def match_file(file, rules, level=99):
    matches = []

    for rule in rules:
        rule = rule['rule']

        if rule['level'] > level:
            continue
        
        if rule.has_key('basename'):
            if isinstance(rule['basename'], list):
                if not all([re.match(r, file) for r in rule['basename']]):
                    continue

            elif not re.match(rule['basename'], file):
                continue

        if rule.has_key('filename'):
            if not file.endswith(rule['filename']):
                continue

        if rule.has_key('suffix'):
            if not file.endswith(rule['suffix']):
                continue

        if rule.has_key('dirname'):
            if not file.startswith(rule['dirname']):
                continue

        if rule.has_key('content'):
            pattern = rule["content"]
            if pattern[0]=="#" and pattern[len(pattern)-1]=="#":
                pattern = pattern[1:len(pattern)-2]
            content = open(os.path.join(filename), 'r').read()
            searchResult = re.search(pattern, content)
            if not searchResult:
                continue

        if rule.has_key('predicate'):
            predicate = rule["predicate"]
            if "args" in rule:
                args = rule["args"]
                if not isinstance(args, list): args = [ args ]
            else:
                args = []
            cmd = os.path.join(predicate)
            for arg in args:
                cmd += " \"" + arg + "\""
            cmd += " \"" + os.path.join(const101.sRoot, filename) + "\""
            (status, output) = commands.getstatusoutput(cmd)
            if status != 0:
                continue

        matches.append({
            'id': -1,
            'metadata': rule.get('metadata', {})
        })

    result = {
        'units': matches,
        'filename': file
    }
    
    return result

def apply_rules(files, rules, level):
    rules = rules['results']['rules']
    return map(lambda file: match_file(file, rules, level), files)
    

def main(data):

    f = open(os.path.join(os.path.dirname(__file__), 'rules.json'))
    rules = json.load(f)
    f.close()

    if data['type'] == 'folders':
        data['data'] = reduce(operator.add, map(lambda folder: map(lambda file: os.path.join(folder, file), os.listdir(folder)), data['data']))

    rules = tag_rules(rules)

    return apply_rules(data['data'], rules, level=data['level'])
    

if __name__ == '__main__':
    main(sys.argv)
 
