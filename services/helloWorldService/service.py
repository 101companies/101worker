__author__ = 'martin'

def myFunc(environ, start_response, params):
	status = '200 OK'
	response_headers = [('Content-Type', 'text/plain')]
	response_body = 'test'
	start_response(status, response_headers)
	return response_body

def routes():
	return [('/hello', myFunc)]