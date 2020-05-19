from alpha_vantage.cryptocurrencies import CryptoCurrencies

cc = CryptoCurrencies(key='J4XLT1RK0S2QK5X0', output_format='pandas')
btc_data = cc.get_digital_currency_daily(symbol='BTC', market='USD')[0]
eth_data = cc.get_digital_currency_daily(symbol='ETH', market='USD')[0]

btc_list = []
eth_list = []

for index, row in btc_data.iterrows():
    btc_list.append(row["1a. open (USD)"])

for index, row in eth_data.iterrows():
    eth_list.append(row["1a. open (USD)"])

btc_deltas = []
eth_deltas = []

for i in range(1, len(btc_list)):
    btc_deltas.append((btc_list[i] - btc_list[i-1])/btc_list[i-1])
    eth_deltas.append((eth_list[i] - eth_list[i-1])/eth_list[i-1])

print("BTC\t\tETH")
for i in range(50):
    print(str(round(btc_deltas[i], 6)) + "\t" + str(round(eth_deltas[i], 6)))