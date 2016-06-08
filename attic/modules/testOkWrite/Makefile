include ../Makefile.vars
r = testResult1.txt
temp = ${tempsdir}/${r}
result = ${resultsdir}/${r}

run:
	@rm -f ${temp}
	@python program.py ${temp}
	@mv ${temp} ${result}

clean:
	@rm -f ${temp} ${result}
