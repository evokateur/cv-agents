OPEN =
ifeq ($(shell uname), Darwin)
OPEN = open
else ifeq ($(shell uname), Linux)
OPEN = xdg-open
endif

.PHONY: vector_db cv_agents cv_structuring job_analysis cv_alignment cv_optimization test clean

cv_agents:
	python -m scripts.cv_agents

cv_structuring:
	python -m scripts.cv_structuring

job_analysis:
	python -m scripts.job_analysis

cv_alignment:
	python -m scripts.cv_alignment

cv_optimization:
	python -m scripts.cv_optimization

vector_db:
	python -m scripts.embed_kb

cv:
	python make-cv.py data/cv.yaml output/cv.tex
	pdflatex --output-directory=output output/cv.tex
	@if [ -n "$(OPEN)" ]; then $(OPEN) output/cv.pdf; fi

cover-letter:
	python make-cover-letter.py data/cover-letter.json output/cover-letter.tex
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

test:
	pytest --tb=short
