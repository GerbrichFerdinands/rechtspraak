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

		self.x = 't'

	def __setattr__(self, name, value):

		# print name
		# print value
		# self.__dict__[name] = value
		super(Ruling, self).__setattr__(name, value)

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

		tags = {
			'identifier':'dcterms:identifier',
			'modified':'dcterms:modified',
			'issued':'dcterms:issued',
			'publisher':'dcterms:publisher',
			'language':'dcterms:language',
			'creator':'dcterms:creator',
			'date':'dcterms:date',
			'type':'dcterms:type',
			'procedure':'psi:procedure',
			'coverage':'dcterms:coverage',
			'spatial':'dcterms:spatial',
			'subject':'dcterms:subject',
			'relation':'dcterms:relation',
			'inhoudsindicatie':'inhoudsindicatie',
			'parablock':'parablock'
		}

		for key, value in tags.iteritems():

			soup_value = soup.find(value)

			if soup_value is not None:
				self.__dict__[key] = soup_value.text

		# Raw data
		self.raw = html

# r = Ruling('ECLI:NL:HR:2011:BT7545')
# r.load()
# print r.raw
# print r.issued



