run:
	perl pull101repo

clean:
	rm -rf module.log cover_db

test:
	prove

cover:
	cover -test -ignore_re \.t$$

doc:
	rm -rf doc
	mkdir doc
	pod2markdown Repo101/Git.pm  doc/Repo101::Git.md
	pod2markdown Repo101/Pull.pm doc/Repo101::Pull.md

install:
	cpan install Class::Tiny File::Slurp Git::Repository LWP::Simple JSON \
                 Try::Tiny Test::Most

.PHONY: run clean test cover doc install
