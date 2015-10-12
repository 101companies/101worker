all:
	make build

build:
	xbuild CSharpValidator.csproj

run:
	make build
	./validator $(file)

test:
	./validator example/Program.cs

clean:
	cd bin; rm -r *.*	