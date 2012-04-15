include ../configs/current.config

# Main target; run all modules

run:
	@make $(patsubst %, %.run, ${modules}) -s

# Comprehensive clean target

clean:
	@make $(patsubst %, %.clean, ${modules}) -s

# Invoke runner and cleaner per module

%.run:
	@python ../tools/runner.py $*

%.clean:
	@python ../tools/cleaner.py $*
