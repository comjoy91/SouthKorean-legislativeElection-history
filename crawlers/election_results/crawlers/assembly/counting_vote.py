#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.assembly.base import *
from utils import sanitize

def Crawler(nth):
	if 1 <= nth <= 16:
		raise InvalidCrawlerError('assembly', 'counting_vote', nth)
		#crawler = CountCrawlerUntil6(int(nth))
	elif 17 <= nth <= 19:
		crawler = CountCrawler1719(int(nth))
	elif nth == 20:
		crawler = CountCrawler20()
	else:
		raise InvalidCrawlerError('assembly', 'counting_vote', nth)
	return crawler



class CountCrawler1719(MultiCityCrawler):
	is_proportional = False

	_election_names = ['20040415', '20080409', '20120411']
	_statement_Ids = ['VCCP09_%2390', 'VCCP09_%232', 'VCCP09_%232']

	_url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
			'selectbox_cityCodeBySgJson_Old.json?electionId=0000000000'\
			'&subElectionCode=2&electionCode='

	_url_list_base = 'http://info.nec.go.kr/electioninfo/'\
			'electionInfo_report.xhtml?electionId=0000000000'\
			'&requestURI=%2FWEB-INF%2Fjsp%2Felectioninfo%2F0000000000%2Fvc%2Fvccp09.jsp'\
			'&oldElectionType=1&electionType=2'\
			'&electionCode=2'\
			'&townCode=-1&sggCityCode=-1'\
			'&statementId='

	@property
	def election_name(self):
		return self._election_names[self.nth-17]
	@property
	def statement_Id(self):
		return self._statement_Ids[self.nth-17]
	@property
	def url_city_codes_json(self):
		return self._url_city_codes_json + self.election_name
	@property
	def url_list_base(self):
		return self._url_list_base + \
			self.statement_Id + '&electionName=' + self.election_name + '&cityCode='

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler1719, self).parse_consti(consti, city_name)
		self.parse_consti_pledge(consti)
		return consti

	def parse_consti_pledge(self, consti):
		pass # TODO: implement

	def __init__(self, nth):
		self.nth = nth
		self.prop_crawler = CountCrawler1719Proportional()
		self.prop_crawler.nth = nth
		self.prop_crawler.election_name = self.election_name
		self.prop_crawler.statement_Id = self.statement_Id


class CountCrawler20(MultiCityCrawler):
	nth = 20
	is_proportional = False

	"""
	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
			'selectbox_cityCodeBySgJson.json?electionId=0020160413&electionCode=2'
			### electionCode=7!!!!
	url_list_base = 'http://info.nec.go.kr/electioninfo/'\
			'electionInfo_report.xhtml?electionId=0020160413'\
			'&requestURI=%2Felectioninfo%2F0020120411%2Fcp%2Fcpri03.jsp'\
			###### 얘는 같을 수 있음 ㅇㅇㅇ
			'&statementId=CPRI03_%232'\
			##### 얘는 다를 수 있음 ㅇㅇㅇㅇㅇ
			'&electionCode=2'\
			### electionCode=7!!!!
			'&sggCityCode=0&cityCode='
			#####
	"""





class CountCrawler1719Proportional(MultiCityCrawler):
	is_proportional = True

	_url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
			'selectbox_cityCodeBySgJson_Old.json?electionId=0000000000'\
			'&subElectionCode=7&electionCode='
	_url_list_base = 'http://info.nec.go.kr/electioninfo/'\
			'electionInfo_report.xhtml?electionId=0000000000'\
			'&requestURI=%2FWEB-INF%2Fjsp%2Felectioninfo%2F0000000000%2Fvc%2Fvccp09.jsp'\
			'&oldElectionType=1&electionType=2'\
			'&electionCode=7'\
			'&townCode=-1&sggCityCode=-1'\
			'&statementId='


	@property
	def url_city_codes_json(self):
		return self._url_city_codes_json + self.election_name
	@property
	def url_list_base(self):
		return self._url_list_base + \
			self.statement_Id + '&electionName=' + self.election_name + '&cityCode='

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler1719Proportional, self).parse_consti(consti, city_name)
		self.parse_consti_party(consti)
		return consti

	def parse_consti_party(self, consti):
		pass # TODO: implement
		#consti['party'] = sanitize(consti['party'][0])



class CountCrawler20Proportional(MultiCityCrawler):
	is_proportional = True
