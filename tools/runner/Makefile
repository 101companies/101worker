run:
	perl runner

clean:
	rm -rf TEST cover_db

test:
	prove

cover:
	cover -test -ignore_re \.t$$

doc:
	rm -rf doc
	mkdir doc
	pod2markdown Repo101/Env.pm doc/Repo101::Env.md

install:
	cpan install File::Slurp JSON JSON::Schema Test::Exception URI::URL

.PHONY: run clean test cover doc install
