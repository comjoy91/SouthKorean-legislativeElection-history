#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.assembly.base import *
from utils import sanitize

def Crawler(nth):
	if 1 <= nth <= 16:
		crawler = CountCrawler_1_16(int(nth))
	elif nth == 17:
		crawler = CountCrawler17(int(nth))
	elif 18 <= nth <= 19:
		crawler = CountCrawler1819(int(nth))
	elif nth == 20:
		crawler = CountCrawler20(int(nth))
	else:
		raise InvalidCrawlerError('assembly', 'counting_vote', nth)
	return crawler



class CountCrawler_1_16(MultiCityCrawler):
	is_proportional = False

	_election_names = [None, '19480510', '19500530', '19540520', '19580502', '19600729',\
					'19631126', '19670608', '19710525', '19730227', '19781212', '19810325', '19850212',\
					'19880426', '19920324', '19960411', '20000413']

	_url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
			'selectbox_cityCodeBySgJson_GuOld.json?electionId=0000000000'\
			'&subElectionCode=2&electionCode='

	_url_list_base = 'http://info.nec.go.kr/electioninfo/'\
			'electionInfo_report.xhtml?electionId=0000000000'\
			'&requestURI=%2FWEB-INF%2Fjsp%2Felectioninfo%2F0000000000%2Fvc%2Fvccp09.jsp'\
			'&oldElectionType=1&electionType=2'\
			'&electionCode=2'\
			'&townCode=-1&sggCityCode=-1'\
			'&statementId=VCCP09_%2390'\
			'&electionName='

	@property
	def election_name(self):
		return self._election_names[self.nth]
	@property
	def url_city_codes_json(self):
		return self._url_city_codes_json + self.election_name
	@property
	def url_list_base(self):
		return self._url_list_base + self.election_name + '&cityCode='

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler_1_16, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth):
		self.nth = nth


class CountCrawler17(MultiCityCrawler):
	is_proportional = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
			'selectbox_cityCodeBySgJson_GuOld.json?electionId=0000000000'\
			'&subElectionCode=2&electionCode=20040415'

	url_list_base = 'http://info.nec.go.kr/electioninfo/'\
			'electionInfo_report.xhtml?electionId=0000000000'\
			'&requestURI=%2FWEB-INF%2Fjsp%2Felectioninfo%2F0000000000%2Fvc%2Fvccp09.jsp'\
			'&oldElectionType=1&electionType=2'\
			'&electionCode=2'\
			'&townCode=-1&sggCityCode=-1'\
			'&statementId=VCCP09_%2390'\
			'&electionName=20040415&cityCode='

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler17, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth):
		self.nth = nth
		self.prop_crawler = CountCrawler17Proportional()
		self.prop_crawler.nth = nth


class CountCrawler1819(MultiCityCrawler):
	is_proportional = False

	_election_names = ['20080409', '20120411']

	_url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
			'selectbox_cityCodeBySgJson_Old.json?electionId=0000000000'\
			'&subElectionCode=2&electionCode='

	_url_list_base = 'http://info.nec.go.kr/electioninfo/'\
			'electionInfo_report.xhtml?electionId=0000000000'\
			'&requestURI=%2FWEB-INF%2Fjsp%2Felectioninfo%2F0000000000%2Fvc%2Fvccp09.jsp'\
			'&oldElectionType=1&electionType=2'\
			'&electionCode=2'\
			'&townCode=-1&sggCityCode=-1'\
			'&statementId=VCCP09_%232'\
			'&electionName='

	@property
	def election_name(self):
		return self._election_names[self.nth-18]
	@property
	def url_city_codes_json(self):
		return self._url_city_codes_json + self.election_name
	@property
	def url_list_base(self):
		return self._url_list_base + self.election_name + '&cityCode='

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler1819, self).parse_consti(consti, city_name)
		return consti

	def __init__(self, nth):
		self.nth = nth
		self.prop_crawler = CountCrawler1819Proportional()
		self.prop_crawler.nth = nth
		self.prop_crawler.election_name = self.election_name


class CountCrawler20(MultiCityCrawler):
	is_proportional = False

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
			'selectbox_cityCodeBySgJson.json?electionCode=2'\
			'&electionId=0020160413'

	url_list_base = 'http://info.nec.go.kr/electioninfo/'\
			'electionInfo_report.xhtml?'\
			'&requestURI=%2FWEB-INF%2Fjsp%2Felectioninfo%2F0020160413%2Fvc%2Fvccp09.jsp'\
			'&statementId=VCCP09_%232'\
			'&sggCityCode=0'\
			'&electionCode=2'\
			'&electionId=0020160413&cityCode='

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler20, self).parse_consti(consti, city_name)
		self.parse_consti_pledge(consti)
		return consti

	def parse_consti_pledge(self, consti):
		pass # TODO: implement

	def __init__(self, nth):
		self.nth = nth
		self.prop_crawler = CountCrawler20Proportional()
		self.prop_crawler.nth = nth


class CountCrawler17Proportional(MultiCityCrawler): #굳이 url_city_codes_json의 GuOld 때문에 따로 떼어놓음. 아오.
	is_proportional = True

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
			'selectbox_cityCodeBySgJson_GuOld.json?electionId=0000000000'\
			'&subElectionCode=7&electionCode=20040415'

	url_list_base = 'http://info.nec.go.kr/electioninfo/'\
			'electionInfo_report.xhtml?electionId=0000000000'\
			'&requestURI=%2FWEB-INF%2Fjsp%2Felectioninfo%2F0000000000%2Fvc%2Fvccp09.jsp'\
			'&oldElectionType=1&electionType=2'\
			'&electionCode=7'\
			'&townCode=-1&sggCityCode=-1'\
			'&statementId=VCCP09_%2390'\
			'&electionName=20040415&cityCode='

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler17Proportional, self).parse_consti(consti, city_name)
		return consti



class CountCrawler1819Proportional(MultiCityCrawler):
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
			'&statementId=VCCP09_%232'\
			'&electionName='

	@property
	def url_city_codes_json(self):
		return self._url_city_codes_json + self.election_name
	@property
	def url_list_base(self):
		return self._url_list_base + self.election_name + '&cityCode='

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler1819Proportional, self).parse_consti(consti, city_name)
		return consti



class CountCrawler20Proportional(MultiCityCrawler):
	is_proportional = True

	url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
			'selectbox_cityCodeBySgJson.json?electionCode=7'\
			'&electionId=0020160413'

	url_list_base = 'http://info.nec.go.kr/electioninfo/'\
			'electionInfo_report.xhtml?'\
			'&requestURI=%2FWEB-INF%2Fjsp%2Felectioninfo%2F0020160413%2Fvc%2Fvccp09.jsp'\
			'&statementId=VCCP09_%237'\
			'&sggCityCode=0'\
			'&electionCode=7'\
			'&electionId=0020160413&cityCode='

	def parse_consti(self, consti, city_name=None):
		consti = super(CountCrawler20Proportional, self).parse_consti(consti, city_name)
		self.parse_consti_party(consti)
		return consti

	def parse_consti_party(self, consti):
		pass # TODO: implement
		#consti['party'] = sanitize(consti['party'][0])
