package:
	ant -lib ant4eclipse/org.ant4eclipse_1.0.0.M4.jar -lib ant4eclipse/libs
	cp build/jar/* dist

execute:
	cd dist;
	java -jar igraph.jar

dot:
	cd dist; dot -Tps Haskell.dot > Haskell.eps; dot -Tpng Haskell.dot > Haskell.png

