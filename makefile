test:
	python3 -m unittest discover -s tests -p "*_test.py" -v

init:
	pip3 install -r requirements.txt

intraday:
	python3 hedgehog/tests/fetch_intraday.py