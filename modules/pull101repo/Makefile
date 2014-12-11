run:
	./pull101repo

clean:
	rm -rf module.log TEST cover_db

test:
	prove

cover:
	cover -test -ignore_re \.t$$

install:
	cpan install Class::Tiny File::Slurp Git::Repository LWP::Simple JSON \
                 Test::Exception

.PHONY: run clean test install
