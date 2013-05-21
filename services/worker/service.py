from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/services/worker/contribution", methods=['POST'])
def index():

    input_data = request.json

    config = json.load(open('contribution.json', 'r'))

    result = []

    app.logger.debug(input_data)

    for module in config:
        n = __import__(module)
        r = n.main(input_data)
        result.append({
            'module': module,
            'result': r
        })

    return json.dumps(result, indent=4)

if __name__ == "__main__":
    app.run(debug=True)

   
