all:
	make build

build:
	xbuild XSDValidator.csproj

run:
	make build
	./validator $(file)

test:
	./validator example/Company.xsd

clean:
	cd bin; rm -r *.*	