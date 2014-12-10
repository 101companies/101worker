run:
	./pull101repo

test:
	rm -rf TEST-*
	perl -E 'say, system("perl", $$_) && die $$! for sort glob "t/*"'

install:
	cpan install Class::Tiny File::Slurp Git::Repository LWP::Simple JSON \
                 Test::Exception

.PHONY: run test install
