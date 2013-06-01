from flask import Flask, request
import json
import sys
import os
import pipes
import requests
from multiprocessing import Process
sys.path.append('../../modules')

app = Flask(__name__)

def handle_request(input_data):
    config = json.load(open('submission.json', 'r'))

    result = []

    path = os.path.join('/tmp', os.path.basename(input_data['name']), input_data['folder'])
    
    output_path = os.path.join('/tmp', os.path.basename(input_data['name']))
    
    if os.path.exists(output_path):
        os.system('rm -rf {}'.format(pipes.quote(output_path)))
    
    os.system('git clone {0} {1}'.format(pipes.quote(input_data['url']), pipes.quote(output_path))) 

    data = {
        'type': 'folders',
        'data': [path]
    }

    for module in config:
        app.logger.debug(module)
        n = __import__(module)
        n.main(data)

    result = open(os.path.join(path, 'summary.json'), 'r').read()

    # make request
    headers = {'content-type': 'application/json'}

    r = requests.post(input_data['backping'], data=result, headers=headers)
    

@app.route("/services/analyzeSubmission", methods=['POST'])
def index():
    
    input_data = request.json
    
    p = Process(target=handle_request, args=(input_data, ))
    p.start() 

    # error other than 0, message contains description of error
    return json.dumps({
        'errorcode': 0,
        'error': None
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

   
