all:
	python3 Start.py
	pdflatex output.tex output.pdf
	xdg-open output.pdf
	rm output.aux
	rm output.log
	rm output.out