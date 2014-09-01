ssh-user = softlang@linux.uni-koblenz.de
www-dir = /home/softlang/www/solasote

all:
	pdflatex doc
	bibtex doc
	pdflatex doc
	pdflatex doc

clean:
	rm -f *.aux *.bbl *.blg *.toc *.log *.log *.dvi *.out *.bak doc.pdf *.tmp temp.*

upload:
	ssh ${ssh-user} mkdir -p ${www-dir}
	scp -r -p index.html doc.pdf ${ssh-user}:${www-dir}

upload-index:
	scp -r -p index.html ${ssh-user}:${www-dir}
