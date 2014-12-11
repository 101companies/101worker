run:
	./pull101repo

clean:
	rm -rf module.log TEST

test:
	prove

install:
	cpan install Class::Tiny File::Slurp Git::Repository LWP::Simple JSON \
                 Test::Exception

.PHONY: run clean test install
