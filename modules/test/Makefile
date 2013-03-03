build:
	make test-discovery


test-discovery:
	curl -o tests/discovery_dir/dir.json http://worker.101companies.org/services/discovery/contributions/haskellTree/src?format=json
	diff tests/discovery_dir/dir.baseline tests/discovery_dir/dir.json
	@rm -f tests/discovery_dir/dir.json
	
	curl -o tests/discovery_file/file.json http://worker.101companies.org/services/discovery/contributions/haskellTree/src/Main.hs?format=json
	diff tests/discovery_file/file.baseline tests/discovery_file/file.json
	@rm -f tests/discovery_file/file.json

	curl -o tests/discovery_fragment/fragment.json http://worker.101companies.org/services/discovery/contributions/haskellTree/src/Main.hs/pattern/main?format=json
	diff tests/discovery_fragment/fragment.baseline tests/discovery_fragment/fragment.json
	@rm -f tests/discovery_fragment/fragment.json
