include ../Makefile.vars
a = testResult1.txt
r = testResult2.txt
arg = ${resultsdir}/${a}
temp = ${tempsdir}/${r}
result = ${resultsdir}/${r}

run: ${arg}
	@rm -f ${temp}
	@python program.py ${arg} ${temp}
	@mv ${temp} ${result}

clean:
	@rm -f ${temp} ${result}
