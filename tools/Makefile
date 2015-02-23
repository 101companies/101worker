%-graphviz:
	@./depend ../configs/$*.json

%-pdf:
	@./depend ../configs/$*.json | dot -Tpdf >$*.pdf

%-png:
	@./depend ../configs/$*.json | dot -Tpng >$*.png

%-svg:
	@./depend ../configs/$*.json | dot -Tsvg >$*.svg
