all:
	make build

build:
	xbuild XMLValidator.csproj

run:
	make build
	./validator $(file)

test:
	./validator example/AcmeCorp.xml

clean:
	cd bin; rm -r *.*	