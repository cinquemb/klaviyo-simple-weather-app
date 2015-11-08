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

REVERSE_STATE_CHOICES = {y:x for x,y in STATE_CHOICES}
#print REVERSE_STATE_CHOICES

data_cities = []
for x in range(1,len(rows)):
	node = [filter_ish(x.get_text()) for x in rows[x].find_all('td')]
	city_node = {}
	for key, value in h_map.iteritems():
		city_node['-'.join(key.strip().lower().split(' '))] = node[value].split('~')[0]
		if node[value].split('~')[0] in REVERSE_STATE_CHOICES:
			city_node[key.strip().lower() + '-short'] = REVERSE_STATE_CHOICES[node[value].split('~')[0]]
	data_cities.append(city_node)

print dict(STATE_CHOICES)['SD']
