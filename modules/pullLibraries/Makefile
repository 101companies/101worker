include ../Makefile.vars

run:
	mkdir -p "$$results101dir/libraries"
	mkdir -p "$$web101dir/libraries"
	php pullLibraries.php "$$worker101dir/configs/all.libraries.json" "$$results101dir/libraries" "$$web101dir/libraries" "$$output101dir"

clean:
	rm -f -r "$$results101dir/libraries" "$$web101dir/libraries"
