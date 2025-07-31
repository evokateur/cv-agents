OPEN =
ifeq ($(shell uname), Darwin)
OPEN = open
else ifeq ($(shell uname), Linux)
OPEN = xdg-open
endif

cv:
	python make-cv.py
	pdflatex --output-directory=output output/cv.tex
	@if [ -n "$(OPEN)" ]; then $(OPEN) output/cv.pdf; fi

cover-letter:
	python make-cover-letter.py
	pdflatex --output-directory=output output/cover-letter.tex
	@if [ -n "$(OPEN)" ]; then $(OPEN) output/cover-letter.pdf; fi

clean:
	echo "Cleaning up pdflatex build artifacts..."
	rm -f output/*.aux
	rm -f output/*.fdb_latexmk
	rm -f output/*.fls
	rm -f output/*.log
	rm -f output/*.out
	rm -f output/*.synctex.gz
