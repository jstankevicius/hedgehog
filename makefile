test:
	python3 -m unittest discover -s tests -p "*_test.py" -v

init:
	pip3 install -r requirements.txt

intraday:
	python3 -m scripts.fetch_intraday

daily:
	python3 -m scripts.fetch_daily

backtest:
	python3 -m scripts.backtesting