from __future__ import print_function

import requests
import bs4
import sys
import os

import pandas
import datetime

import rechtspraak

from settings import DATA_PATH

URL_RULING_PAGES = 'http://data.rechtspraak.nl/uitspraken/zoeken'
URL_RULING = ''
METADATA_FILEPATH = 'data/rulings_metadata.csv'

NUMBER_OF_ARTICLES_PAGE = 1000

def get_data(*args, **kwargs):

	rulings = pandas.read_csv(METADATA_FILEPATH, sep=';', index_col='id', encoding='utf-8')
	files = [os.path.splitext(name)[0] for path, subdirs, files in os.walk(DATA_PATH) for name in files if '.txt' in name]

	for index in set(rulings.index.unique()) - set(files):

		print("Fetching ruling with id", index)

		r = rechtspraak.Ruling()

		try:
			r.load(index)

			dirpath = os.path.join(DATA_PATH, str(datetime.datetime.strptime(r.date, "%Y-%m-%d").year)) # 2014-04-23

			if not os.path.isdir(dirpath):
			   os.makedirs(dirpath)

			with open(os.path.join(dirpath, '%s.txt' % index), "wb") as ruling_xml:
				ruling_xml.write(r.raw)

		except Exception as err:
			print('An error occured:', err)

def get_metadata(from_ruling=0, *args, **kwargs):

	terminate = False
	court_rulings = None

	while not terminate:

		# Start the process with fetching the folling block of rulings
		print('Load batch %s-%s.' % (from_ruling, from_ruling+NUMBER_OF_ARTICLES_PAGE-1))

		# Set parameters
		param_dict = {'from':from_ruling, 'max':NUMBER_OF_ARTICLES_PAGE, 'return':'DOC', 'type':'uitspraak'}

		try:
			r = requests.get(URL_RULING_PAGES, params=param_dict)
			r.raise_for_status()
		except Expection:
			print('An error with the HTTP request.')
			continue

		soup = bs4.BeautifulSoup(r.text)
		list_of_articles = soup.find_all('entry')

		court_rulings_batch = pandas.DataFrame(
			[{tag.name:tag.text for tag in article.children} for article in list_of_articles]
			)
		
		try:
			court_rulings = court_rulings.append(court_rulings_batch)
		except Exception, err:
			court_rulings = court_rulings_batch

		from_ruling += NUMBER_OF_ARTICLES_PAGE

		if court_rulings_batch.empty:

			print('Terminate scraping of data.')
			terminate = True #False

			if not os.path.isdir(DATA_PATH):
			   os.makedirs(DATA_PATH)

			court_rulings.to_csv(METADATA_FILEPATH, sep=';', quoting=1, encoding='utf-8', index=False)

if __name__ == '__main__':

	try:
		method = sys.argv[1]
	except Exception, err:
		raise ValueError('No input arguments specified.')

	# Argument 'metadata' starts loading the metadata
	if method == 'metadata':
		get_metadata()

	# Argument 'data' starts loading the full data
	elif method == 'data':
		get_data()

	else:
		print('Unknown input argument.')


	