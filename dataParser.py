import config 
import requests
from bs4 import BeautifulSoup as bs
import re


def reformate(value):
	value = str(value)
	if len(value) > 9:
		return value[0:len(value) - 9] + '.' + value[len(value) - 9:len(value) - 6] + '.' + value[len(value) - 6:len(value) - 3] + '.' + value[len(value) - 3: len(value)]
	elif len(value) > 6:
		return value[0:len(value) - 6] + '.' + value[len(value) - 6:len(value) - 3] + '.' + value[len(value) - 3:len(value)]
	elif len(value) > 3:
		return value[0:len(value) - 3] + '.' + value[len(value) - 3:len(value)]
	elif len(value) > 0:
		return value


def check_dollar_value():
	dollarFullPage = requests.get(config.DOLLAR_RUB, headers=config.headers)
	dollarSoup = bs(dollarFullPage.content, 'html.parser')
	dollarConvert = dollarSoup.findAll('span', {'class': 'pid-2186-last'})
	if __name__ == '__main__':
		print(dollarConvert)
	return dollarConvert[0].text.replace(',','.')


def check_euro_value():
	euroFullPage = requests.get(config.EURO_RUB, headers=config.headers)
	euroSoup = bs(euroFullPage.content, 'html.parser')
	euroConvert = euroSoup.findAll('span', {'class': 'pid-1691-last'})
	return euroConvert[0].text.replace(',','.')


def check_corona_russia():
	coronaRusiiaFullPage = requests.get(config.CORONA_RUSSIA, headers=config.headers)
	coronaRussiaSoup = bs(coronaRusiiaFullPage.content, 'html.parser')
	coronaRussiaConvert = coronaRussiaSoup.findAll('b')
	# if __name__ == '__main__':
	# 	print(coronaRussiaConvert)
	return {'all': reformate(coronaRussiaConvert[0].text), 
			'recovered': reformate(coronaRussiaConvert[2].text), 
			'dies': reformate(coronaRussiaConvert[3].text),
			'plus': reformate(int(get_corona_ru_per_day()[50]) - int(get_corona_ru_per_day()[49]))}


def check_corona_world():
	coronaWorldFullPage = requests.get(config.CORONA_WORLD, headers=config.headers)
	coronaWorldSoup = bs(coronaWorldFullPage.content, 'html.parser')
	coronaWorldConvert = coronaWorldSoup.findAll('div', {'class': 'maincounter-number'})
	# if __name__ == '__main__':
		# print(coronaWorldConvert[0].text.replace('\n',''))
	return {'all': reformate(coronaWorldConvert[0].text.replace(' ','').replace('\n','').replace(',','')), 
			'recovered': reformate(coronaWorldConvert[2].text.replace(' ','').replace('\n','').replace(',','')), 
			'dies': reformate(coronaWorldConvert[1].text.replace(' ','').replace('\n','').replace(',',''))}

def get_corona_ru_per_day():
	finalDict = dict()
	a = requests.get(config.CORONA_RUSSIA_PER_DAYS).text
	b = re.findall(r'<p>\d+ ?\d+(?:\w+|&| |;)+<span', a, re.IGNORECASE)
	data = re.findall(r'\d+ ?\d+ ?\d+', str(b), re.IGNORECASE)
	j = 1
	for i in range(len(data)-50,len(data)):
		data[i] = int(data[i].replace(' ',''))
		finalDict[j] = data[i]
		j += 1
	return finalDict


if __name__ == '__main__':
	# print(check_dollar_value())
	# print(check_euro_value())
	# print(checkCoronaWorld())
	print(check_corona_russia())
	# while True:
		# print(reformate(input()))
	# print(get_corona_ru_per_day())