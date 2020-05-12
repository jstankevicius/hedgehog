from IEXTools import Parser, messages
from pathlib import Path
#k = Path('20200507_IEXTP1_TOPS1.6.pcap').resolve()
dictionary = {}
p = Parser(r'C:\Users\alexz\Downloads\20200507_IEXTP1_TOPS1.6.pcap')

print(Parser('C:\\Users\\alexz\\Downloads\\20200507_IEXTP1_TOPS1.6.pcap', tops=True, deep=False))

with Parser(r'C:\Users\alexz\\Downloads\20200507_IEXTP1_TOPS1.6.pcap') as iex_messages:
    for message in iex_messages:
        print(message)