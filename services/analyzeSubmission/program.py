from flask import Flask, request
import json
import sys
sys.path.append('../../modules')

app = Flask(__name__)


@app.route("/services/analyzeSubmission", methods=['POST'])
def index():

    input_data = request.json

    config = json.load(open('submission.json', 'r'))

    result = []

    app.logger.debug(input_data)

    for module in config:
        n = __import__(module)
        n.main(input_data)

    results = []

    return json.dumps(result, indent=4)

if __name__ == "__main__":
    app.run(debug=True)

   
