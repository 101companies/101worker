import os
import json

# Normalize rule
def normalizeRule(rule):
    if not isinstance(rule["metadata"], list):
        rule["metadata"] = [ rule["metadata"] ]
#
# Gather metrics.
# Check validity upfront.
# Qualify rule with origin information.
#
def handleRule(rule, filename):
    normalizeRule(rule)
    return {
        "filename" : filename,
        "rule"     : rule,
    }

def handleFileCreation(context, change, rules_dump):
    data = json.loads(context.get_primary_resource(change['file']))
    if isinstance(data, list):
        for rule in data:
            rules_dump['results']['rules'].append(handleRule(rule, change['file']))
    else:
        rules_dump['results']['rules'].append(handleRule(data, change['file']))

    context.write_dump('rules101dump', rules_dump)

def handleFileRemoved(context, change, rules_dump):
    rules_dump['results']['rules'] = filter(lambda rule: rule['filename'] != change['filename'], rules_dump['results']['rules'])

    context.write_dump('rules101dump', rules_dump)

def handleFileChanged(context, change, rules_dump):
    rules_dump['results']['rules'] = filter(lambda rule: rule['filename'] != change['filename'], rules_dump['results']['rules'])

    handleFileCreation(context, change, rules_dump)

def run(context, change):
    '''
    This only handles .101meta files
    '''
    rules_dump = context.read_dump('rules101dump')
    if not rules_dump:
        rules_dump = {
            'results': {
                'rules': []
            }
        }

    if os.path.basename(change['file']) == '.101meta':
        if change['type'] == 'NEW_FILE':
            handleFileCreation(context, change, rules_dump)
        elif change['type'] == 'FILE_CHANGED':
            handleFileChanged(context, change, rules_dump)
        else:
            handleFileRemoved(context, change, rules_dump)
