build:
	make jvalidator/JValidator.class

jvalidator/JValidator.class: jvalidator/*.java Makefile
	javac \
		-Xlint \
		-classpath .:lib/javaparser-1.0.8.jar \
		jvalidator/*.java

test:
	./validator example/Serialization.java

clean:
	rm -f jvalidator/*.class

install:
	apt-get install openjdk-7-jdk
