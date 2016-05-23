install-debian-pkgs:
	sudo apt-get install git
	sudo apt-get install python3-pip

install-pip-pkgs:
	sudo pip3 install gitpython
	sudo pip3 install jinja2
	sudo pip3 install pymongo
	sudo pip3 install inflection
	sudo pip3 install networkx

# Remove ALL derived files
full-reset:
	rm -rf ../101web ../101logs ../101temps ../101results ../101diffs ../101test

init:
	mkdir -p ../101web/data/dumps
	mkdir -p ../101web/data/resources
	mkdir -p ../101web/data/views
	mkdir -p ../101logs
	mkdir -p ../101temps
	mkdir -p ../101results
	mkdir -p ../101diffs

download:
	bin/download_resources
