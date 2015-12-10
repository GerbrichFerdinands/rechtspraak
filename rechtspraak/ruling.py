import pandas
import bs4
import requests

import os

class Ruling(object):

	def __init__(self, identifier=None):

		# Set parameters
		self.identifier = identifier
		self.modified = None
		self.issued = None
		self.publisher = None
		self.language = None
		self.creator = None
		self.date = None
		self.type = None
		self.procedure = None
		self.coverage = None
		self.spatial = None
		self.subject = None
		self.relation = None
		self.inhoudsindicatie = None
		self.parablock = None

		self.raw = None

	def load(self, path_or_id=None):

		if path_or_id is not None and os.path.exists(path_or_id):
			self._from_file(path_or_id)
			return

		self._from_web(path_or_id)
	
	def _from_file(self, path):

		with open(path, "wb") as ruling_xml:
			return ruling_xml.read()

	def _from_web(self, identifier=None):

		self.identifier = identifier if identifier is not None else self.identifier

		url = 'http://data.rechtspraak.nl/uitspraken/content'
		param_dict = {'id': self.identifier}

		r = requests.get(url, params=param_dict)
		r.raise_for_status()

		return self._parse(r.text.encode('utf-8'))

	def _parse(self,html):

		soup = bs4.BeautifulSoup(html)

		self.identifier = soup.find('dcterms:identifier').text
		# self.modified = soup.find('dcterms:modified').text
		# self.issued = soup.find('dcterms:issued').text
		# self.publisher = soup.find('dcterms:publisher').text
		# self.language = soup.find('dcterms:language').text
		# self.creator = soup.find('dcterms:creator').text
		self.date = soup.find('dcterms:date').text
		# self.type = soup.find('dcterms:type').text
		# self.procedure = soup.find('psi:procedure').text
		# self.coverage = soup.find('dcterms:coverage').text
		# self.spatial = soup.find('dcterms:spatial').text
		# self.subject = soup.find('dcterms:subject').text
		self.relation = soup.find('dcterms:relation').text
		self.inhoudsindicatie = soup.find('inhoudsindicatie').text
		self.parablock = soup.find('parablock').text

		# Raw data
		self.raw = html

# r = Ruling('ECLI:NL:HR:2011:BT7545')
# r.load()
# print r.raw



