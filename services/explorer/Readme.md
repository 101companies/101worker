# Headline

Resource discovery service

# Details

This webservice is intended to explore and discover the files and metadata produced by a 101worker production cycle.
The goal is that every file of the 101companies ecosystem is a resource, to which this discovery service can deliver
metadata.

Example: http://101companies.org/resources/contributions/haskellTree/src

# Output

Standard output is in JSON. By appending ?format=html to the URL, the discovery webservice will answer with complete
HTML documents.

# Requirements

* A working setup of 101worker and a completed production cycle
* The Jinja2 Python module, if responses in HTML are supposed to work