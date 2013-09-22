import json

def create(environ, start_response, params):
    status = '200 OK'
    title = params.get('title', '')
    original = params.get('original', '')
    features = params.get('features', '').split(',')
    result =  {'title' : title, 'original': original, 'features': features}
    result = json.dumps(result)
    return result
