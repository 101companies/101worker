
Adding a new service:
	- create a folder in services
	- create a service.py with a function called routes()
		- routes has to return a list of tupels
		- first parameter of these tupels is a regex describing a path
		- second is a function
	- carefull with importing stuff - you will be in your path when the function is executed, but not before!!!

Requirements:
	- matches.json
	- read/write rights in the FragmentLocators folder for building them
	- anything more?