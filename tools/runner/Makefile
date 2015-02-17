run:
	perl runner

clean:
	rm -rf cover_db

test:
	prove

cover:
	cover -test -ignore_re \.t$$

doc:
	rm -rf doc
	mkdir doc
	perl -e 'for (glob "Runner101/*.pm")'                              \
	     -e '{'                                                        \
	     -e '    m{Runner101/(.+)\.pm$$};'                             \
	     -e '    system "pod2markdown", $$_, "doc/Runner101::$$1.md";' \
	     -e '}'

install:
	@type timeout >/dev/null 2>&1 || {                                  \
	    echo >&2 WARNING: timeout command is required, please install it; \
	}
	cpan install Capture::Tiny File::Slurp IPC::Run JSON JSON::Schema \
                 List::MoreUtils Proc::ChildError Test::Most Try::Tiny URI::URL

.PHONY: run clean test cover doc install
