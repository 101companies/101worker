
def noParam(environ, start_response, params):
	status = '200 OK'
	response_headers = [('Content-Type', 'text/plain')]
	response_body = 'FragmentService: Please specify some parameters'
	start_response(status, response_headers)
	return response_body


def findFragment(environ, start_response, params):
	import fragments

	try:
		status = '200 OK'
		response_headers = [('Content-Type', 'text/json')]
		start_response(status, response_headers)
		return fragments.findFragment(params['filePath'], params['fileName'], params['fragment'])
	except Exception, error:
		status = '500 Internal Server Error'
		response_headers = [('Content-Type', 'text/plain')]
		start_response(status, response_headers)
		return str(error)


def routes():
	return [
		( '/fragment/(?P<filePath>.+)/(?P<fileName>.*\.[^/]+)(/(?P<fragment>.+))?', findFragment ),
		( '/fragment', noParam )
	]
#/fragment/(?P<name>[^/]+)