cv:
	python fill-cv-template.py
	pdflatex cv.tex

clean:
	echo "Cleaning up miscellaneous pdflatex output files..."
	rm -f ./*.aux
	rm -f ./*.fdb_latexmk
	rm -f ./*.fls
	rm -f ./*.log
	rm -f ./*.out
	rm -f ./*.synctex.gz
