cv:
	python fill-cv-template.py
	pdflatex cv.tex
	open cv.pdf

cover-letter:
	python fill-cover-letter-template.py
	pdflatex cover-letter.tex
	open cover-letter.pdf

clean:
	echo "Cleaning up pdflatex build artifacts..."
	rm -f ./*.aux
	rm -f ./*.fdb_latexmk
	rm -f ./*.fls
	rm -f ./*.log
	rm -f ./*.out
	rm -f ./*.synctex.gz
