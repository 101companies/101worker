import json
import operator
import sys
import os
import re
import copy
import commands
<<<<<<< HEAD
sys.path.append('../../libraries/101meta')
import const101
import tools101

from asq.initiators import query


def match_file(file, rules, filter_function, append):
=======
from asq.initiators import query


def match_file(file, rules, filter_function, append=False):
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
    rules = filter(filter_function, rules)
    matches = []

    for rule in rules:
        rule = rule['rule']
<<<<<<< HEAD
=======

        if rule['level'] > level:
            continue
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
        
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
<<<<<<< HEAD
            cmd = os.path.join(const101.sRoot, predicate)
            for arg in args:
                cmd += " \"" + arg + "\""
            cmd += " \"" + os.path.join(const101.sRoot, file) + "\""
            (status, output) = commands.getstatusoutput(cmd)
            if status != 0:
                #print 'failed:', cmd, output
=======
            cmd = os.path.join(predicate)
            for arg in args:
                cmd += " \"" + arg + "\""
            cmd += " \"" + os.path.join(const101.sRoot, filename) + "\""
            (status, output) = commands.getstatusoutput(cmd)
            if status != 0:
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
                continue

        matches.append({
            'id': -1,
            'metadata': rule.get('metadata', {})
        })
    
    if append:
<<<<<<< HEAD
        if not matches:
            return
        f = open(file + '.metadata.json', 'r')
        data = json.load(f)
        f.close()
        data.extend(matches)
        f = open(file + '.metadata.json', 'w')
        data = json.dump(data, f, indent=4, sort_keys=True)
=======
        f = open(file + '.metadata.json', 'r')
        data = json.load(f)
        f.close()
        data.append(matches)
        f = open(file + '.metadata.json', 'a')
        data = json.dump(data, f)
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
        f.close()
        
    else:
        f = open(file + '.metadata.json', 'w')
<<<<<<< HEAD
        json.dump(matches, f, indent=4, sort_keys=True)
        f.close()

def apply_rules(files, rules, filter_function, append):
    rules = rules['results']['rules']
    map(lambda file: match_file(file, rules, filter_function, append), files)
=======
        json.dump(matches, f)
        f.close()

def apply_rules(files, rules, filter_function):
    rules = rules['results']['rules']
    map(lambda file: match_file(file, rules, filter_function), files)
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
    
def group_fast_predicates(rules):
    rules = rules['results']['rules']
    fpredicate_rules = query(rules).where(lambda rule: rule['rule'].has_key('fpredicate')).select(lambda rule: rule['rule']).to_list()

    groups = []
    used = []

    for rule in fpredicate_rules:
        if rule in used:
            continue
    
        same_predicate = query(fpredicate_rules).where(lambda r: r['fpredicate'] == rule['fpredicate']).to_list()
        groups.append([rule])
        used.append(rule)

        tmp_rule = copy.copy(rule)
        del tmp_rule['args']
        del tmp_rule['metadata']
        
        for p in same_predicate:
            tmp_p = copy.copy(p)
            del tmp_p['args']
            del tmp_p['metadata']

            if tmp_p == tmp_rule and p != rule:
                used.append(p)
                groups[-1].append(p)


    result = []
    for group in groups:
        i = group[0]
        i['args'] = [i['args']] + query(group[1:]).select(lambda rule: rule['args']).to_list()
        i['metadata'] = [i['metadata']] + query(group[1:]).select(lambda rule: rule['metadata']).to_list()
        result.append(i)

<<<<<<< HEAD
    return {'results': {'rules': result } }
=======
    return result
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
    
    
if __name__ == '__main__':
    print group_fast_predicates(json.load(open('rules.json')))


 
