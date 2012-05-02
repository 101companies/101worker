include ../Makefile.vars

DOT_FILES := $(wildcard dist/*.dot)
DOT_DIR   := dist

run:
	make package 
	make execute
	make dot
	make copy_png

package:
	ant -lib ant4eclipse/org.ant4eclipse_1.0.0.M4.jar -lib ant4eclipse/libs
	cp build/jar/* dist

execute:
	cd dist; java -jar igraph.jar
        
%.png: %.dot
	dot $< -Tpng -o $@

make_$(DOT_DIR)/%.dot:
	cd $(DOT_DIR); dot $*.dot -Tpng -o $*.png

dot: $(addprefix make_,$(DOT_FILES))
	
copy_png:
	mkdir -p ${webdir}/igraphs
	cp $(DOT_DIR)/*.dot ${webdir}/igraphs
	cp $(DOT_DIR)/*.png ${webdir}/igraphs	

        

	
