all:
	make build

build:
	xbuild ./XMLValidator.csproj

run:
	make build
	./validator $(file)

test: test-positiv test-negativ test-positiv-html

test-positiv:
	./validator ./example/goodexample.xml

test-negativ:
	./validator ./example/badexample.xml -negativ

test-positiv-html:
	./validator ./example/goodexample.xml


clean:
	cd bin; rm -r *.*	
