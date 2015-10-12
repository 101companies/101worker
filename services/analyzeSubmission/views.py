import json
import sys
import os

os.chdir(os.path.dirname(__file__))

import pipes
import requests
from multiprocessing import Process
from django.http import HttpResponse, HttpResponseNotAllowed
sys.path.append('../../modules')

def handle_request(input_data):
    config = json.load(open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'submission.json')), 'r'))

    result = []

    path = '/tmp/' + os.path.basename(input_data['name']) + '/' + input_data['folder']
    
    output_path = '/tmp/' + os.path.basename(input_data['name'])
    
    if os.path.exists(output_path):
        os.system('rm -rf {}'.format(pipes.quote(output_path)))
    
    os.system('git clone {0} {1}'.format(pipes.quote(input_data['url']), pipes.quote(output_path))) 

    data = {
        'type': 'folders',
        'data': [path]
    }
    
    error = None

    for module in config:
        try:
            n = __import__(module)
            n.main(data)
        except Exception, e:
            error = e

    if error:
        result = {
            'concepts': [],
            'features': [],
            'languages': [],
            'technologies': []
    }
    else:
        result = json.load(open(os.path.join(path, 'summary.json'), 'r'))

    result['error'] = str(error)

    # make request
    headers = {'content-type': 'application/json'}

    r = requests.post(input_data['backping'], data=json.dumps(result), headers=headers)
    

def analyze(request):
    
    if request.method != 'POST':
        return HttpResponseNotAllowed('Only get allowed')
    
    input_data = json.loads(request.body)
    
    p = Process(target=handle_request, args=(input_data, ))
    p.start() 

    # error other than 0, message contains description of error
    return HttpResponse(json.dumps({
        'errorcode': 0,
        'error': None
    }), content_type='application/json')


   




