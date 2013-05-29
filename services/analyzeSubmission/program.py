from flask import Flask, request
import json
import sys
import os
import pipes
sys.path.append('../../modules')

app = Flask(__name__)


@app.route("/services/analyzeSubmission", methods=['POST'])
def index():

    input_data = request.json

    config = json.load(open('submission.json', 'r'))

    result = []

    app.logger.debug(input_data)

    path = os.path.join('/tmp', os.path.basename(input_data['name']), input_data['folder'])
    
    output_path = os.path.join('/tmp', os.path.basename(input_data['name']))
    
    if os.path.exists(output_path):
        os.system('rm -rf {}'.format(output_path))
    
    os.system('git clone {0} {1}'.format(pipes.quote(input_data['url']), output_path)) 

    data = {
        'type': 'folders',
        'data': [path]
    }
    
    app.logger.debug(data)

    for module in config:
        app.logger.debug(module)
        n = __import__(module)
        n.main(data)

    results = []

    return json.dumps(result, indent=4)

if __name__ == "__main__":
    app.run(debug=True)

   
