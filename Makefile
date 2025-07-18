cv:
	python fill-cv-template.py
	pdflatex cv.tex
	open cv.pdf

clean:
	echo "Cleaning up pdflatex build artifacts..."
	rm -f ./*.aux
	rm -f ./*.fdb_latexmk
	rm -f ./*.fls
	rm -f ./*.log
	rm -f ./*.out
	rm -f ./*.synctex.gz
