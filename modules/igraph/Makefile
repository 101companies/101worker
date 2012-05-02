include ../Makefile.vars

run:
	make package 
	make execute
	make dot

package:
	ant -lib ant4eclipse/org.ant4eclipse_1.0.0.M4.jar -lib ant4eclipse/libs
	cp build/jar/* dist

execute:
	cd dist; java -jar igraph.jar

dot:
	mkdir ${webdir}/igraphs
	cp dist/*.dot ${webdir}/igraphs
