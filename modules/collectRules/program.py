import os
import json

# Normalize rule
def normalizeRule(rule):
    if not isinstance(rule['metadata'], list):
        rule['metadata'] = [ rule['metadata'] ]

# add filename to module for incremental approach
def handleRule(rule, filename):
    normalizeRule(rule)
    return {
        'filename' : filename,
        'rule'     : rule
    }

def handleFileCreation(context, change, rules_dump):
    data = json.loads(context.get_primary_resource(change['file']))

    # .101meta can be list or objects
    if isinstance(data, list):
        for rule in data:
            rules_dump['results']['rules'].append(handleRule(rule, change['file']))
    else:
        rules_dump['results']['rules'].append(handleRule(data, change['file']))

    context.write_dump('rules101dump', rules_dump)

def handleFileRemoved(context, change, rules_dump):
    # filter rules from the removed file
    rules_dump['results']['rules'] = filter(lambda rule: rule['filename'] != change['file'], rules_dump['results']['rules'])

    context.write_dump('rules101dump', rules_dump)

def handleFileChanged(context, change, rules_dump):
    # filter rules from the changed file ...
    rules_dump['results']['rules'] = filter(lambda rule: rule['filename'] != change['file'], rules_dump['results']['rules'])

    # ... and later add them again
    handleFileCreation(context, change, rules_dump)

def run(context, change):
    rules_dump = context.read_dump('rules101dump')

    # initialize a default dump
    if not rules_dump:
        rules_dump = {
            'results': {
                'rules': []
            }
        }

    # This only handles .101meta files
    if os.path.basename(change['file']) == '.101meta':
        if change['type'] == 'NEW_FILE':
            handleFileCreation(context, change, rules_dump)
        elif change['type'] == 'FILE_CHANGED':
            handleFileChanged(context, change, rules_dump)
        else:
            handleFileRemoved(context, change, rules_dump)
