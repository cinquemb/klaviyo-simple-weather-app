from bs4 import BeautifulSoup as bs
import re
from localflavor.us.us_states import STATE_CHOICES

def filter_ish(ish,header=False):
	filt = ish.strip().replace('  ','').replace('\n','').strip()
	if header:
		filt1 = re.sub('[0-9]+', '', filt).replace('-','')
		return filt1
	return filt

f = open('top_us_cities_by_population.html','r+')
html_data = f.read()
f.close()

soup = bs(html_data,'lxml')
rows = soup.find_all('tr')
headers = [filter_ish(x.get_text(), True) for x in rows[0].find_all('th')]
h_map = {x:i for i,x in enumerate(headers)}

for x in range(1,len(rows)):
	node = [filter_ish(x.get_text()) for x in rows[x].find_all('td')]
	for key, value in h_map.iteritems():
		print key.strip(), node[value].split('~')[0]
	print '\n\n\n\n\n'
