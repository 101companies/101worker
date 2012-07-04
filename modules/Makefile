include ../configs/current.config

# Main target; run all modules

run:
	@make $(patsubst %, %.run, ${modules}) -s

# Comprehensive clean target

clean:
	@make $(patsubst %, %.clean, ${modules}) -s

# Invoke runner and cleaner per module

%.run:
	if test -d $*; then python ../tools/runner.py $*; else echo 'No module dir found. Please check the config file'; fi

%.clean:
	echo 'Cleaning ' $*
	if test -d $*; then python ../tools/cleaner.py $*; else echo 'No module dir found. Please check the config file'; fi
