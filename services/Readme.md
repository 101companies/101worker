# The notion of a service

A (web-)service in the 101worker sense is offering some piece of data through a web interface.

# The serverInterface script

The serverInterface.py script is accepting incoming requests and is routing it to more specific services, based on the incoming URI.

# Requirements
The Services Interface need a working Apache with the libapache2-mod-wsgi module installed. Then a script alias needs to be defined in the Apache Configuration and the services directory needs proper rights.
An example looks like this:
```bash
	WSGIScriptAlias /services /somepath/101worker/services/serverInterface.py

	<Directory /somepath/101worker/services/*>
		AllowOverride None
		Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
		Order allow,deny
		Allow from all
	</Directory>
```
The services offered through this interface might have more specific requirements.

Services that can serve complex HTML content should use the Jinja Template language. Therefore, the Python module for Jinja2 can also be seen as an requirement.

# Adding a new service

Several steps are necessary to add a new service:
* create a folder in services
* create the serves as an entrypoint for the script. This function takes a variable describing the environment, a variable that serves as a callback for starting the answer and a variable that will contain all groups of the regex describing your URL.
* create a service.py in that newly created folder with a function called routes()
* the routes() has to return a list of tupels. An example would be: ('/hello/(?P<name>[^/]+)', helloName)
* the first parameter of these tupels is a regex describing a path, the second is a function that will be called when a appropriate request is coming in

an example is helloWorldService.

importing of other python scripts is possible, but it should be done when the function is executed. This is because the serverInterface will switch into the directory of the service right before the function is executed.

# Useful regular expressions

* /(?P<segment>[^/]+) for a segment of a URL (e.g. /mysegment)
* /(?P<digits>\d+) for a digit
* /(?P<number>\d*.?\d+) for a number
* /(?P<fileName>.*\.[^/]+) for a filename (e.g. /Company.java)