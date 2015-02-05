orig = ${repo101dir}/technologies/geshi
result = ${results101dir}/geshi/src/geshi

run: ${repo101dir} ${orig}
	@make clean
	@cp -r ${orig} ${results101dir}
	@python program.py ${repo101dir} ${result}

clean:	
	@#no-op
