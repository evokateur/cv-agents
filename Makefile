cv:
	python make-cv.py
	pdflatex --output-directory=output output/cv.tex
	open output/cv.pdf

cover-letter:
	python make-cover-letter.py
	cd output
	pdflatex --output-directory=output output/cover-letter.tex
	open output/cover-letter.pdf

clean:
	echo "Cleaning up pdflatex build artifacts..."
	rm -f output/*.aux
	rm -f output/*.fdb_latexmk
	rm -f output/*.fls
	rm -f output/*.log
	rm -f output/*.out
	rm -f output/*.synctex.gz
