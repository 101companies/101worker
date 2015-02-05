run:
	mkdir -p "$$results101dir/101results/libraries"
	mkdir -p "$$results101dir/101web/libraries"
	php pullLibraries.php "$$worker101dir/configs/all.libraries.json" "$$results101dir/101results/libraries" "$$results101dir/101web/libraries" "$$results101dir"

clean:
	rm -f -r "$$results101dir/101results/libraries" "$$results101dir/101web/libraries"
