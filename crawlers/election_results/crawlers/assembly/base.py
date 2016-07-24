#!/usr/bin/env python3
# -*- coding=utf-8 -*-


############### is proportional in parse!


import gevent
from gevent import monkey
import itertools
from urllib.parse import urljoin

from utils import flatten, get_json, get_xpath, parse_cell, sanitize, split

monkey.patch_all()

class BaseCrawler(object):
	url_image_base = 'http://info.nec.go.kr'

	attrs = []
	attrs_district = ['district', 'electorates', 'counted_votes', 'cand_no', 'result', 'valid_votes', 'undervotes', 'blank_ballots']
	attrs_result = ['name', 'vote']
	attrs_exclude_parse_cell = ['image', 'cand_no', 'result']


	def parse_proportional(self, url, city_name=None): #지금 이건 비례대표만 해당하는 거임 ㅇㅇㅇㅇㅇ
		elems = get_xpath(url, '//td')
		th_list = get_xpath(url, '//th')
		for i in range(int(len(th_list))):
			if th_list[i].get('colspan') != None:
				num_ths_left = i
				max_candidate_num = int(th_list[i].get('colspan')) - 1
				break

		if th_list[0].get('rowspan') != None: #nth!=20
			party_name_list = th_list[6:(6+max_candidate_num)] #element: <th><strong>한나라당</strong></th>
			td_head = 0
			num_tds = 6 + max_candidate_num #저 6의 확장일반화 방법은 없는가.
			num_rows = int(len(elems) / num_tds)
		else: #nth == 20
			max_candidate_num = max_candidate_num + 1
			party_name_list = elems[num_ths_left:(num_ths_left+max_candidate_num)] #for n=20. element: <td><strong>한나라당</strong></td>
			td_head = 1
			num_tds = len(th_list) + max_candidate_num - 1
			num_rows = int(len(elems) / num_tds) - 1

		consti_list = []
		candidate_num = max_candidate_num

		for i in range(num_rows):
			index = i + td_head

			district = elems[index*num_tds]#.text # 여기 저장되는 district 이름은 '전체'(첫 줄)+기초자치단체명임 ㅇㅇ
			electorates = elems[index*num_tds + 1]#.text
			counted_vote = elems[index*num_tds + 2]#.text

			votes_num_percent = elems[index*num_tds + num_ths_left : index*num_tds + num_ths_left+candidate_num] #element: <td>1,940,259<br>(42.28)</td>
			cand_list = list(map(lambda x, y: dict(list(zip(self.attrs_result, [x, y]))), party_name_list, votes_num_percent)) #('name': <th><strong>한나라당</strong></th>, 'vote': <td>1,940,259<br>(42.28)</td>)

			valid_vote = elems[index*num_tds + num_ths_left + max_candidate_num+0]#.text
			undervote = elems[index*num_tds + num_ths_left + max_candidate_num+1]#.text
			blank_ballot = elems[index*num_tds + num_ths_left + max_candidate_num+2]#.text

			district_info = (district, electorates, counted_vote, candidate_num, cand_list, valid_vote, undervote, blank_ballot)
			district_info = dict(list(zip(self.attrs_district, district_info)))

			#if i==0: print(district_info['result'][0]['name'].find('strong').text)

			consti_list.append(district_info)

		consti_list = [self.parse_consti(consti, city_name=city_name) for consti in consti_list]
		print(('crawled #%d - %s, %s(%d)...' % (self.nth, '비례대표', city_name, len(consti_list))))
		return consti_list



	def parse_constituency(self, url, city_name=None): #지금 이건 지역구만 해당하는 거임 ㅇㅇㅇㅇㅇ
		tr_list = get_xpath(url, '//tr')
		thead_list = get_xpath(url, '//th')
		max_candidate_num = len(tr_list[2]) - len(thead_list)
		for i in range(len(thead_list)):
			if thead_list[i].get('colspan') != None:
				num_ths_left = i
				#max_candidate_num = int(thead_list[i].get('colspan')) - 1
				break

		consti_list = []

		for i in range(len(tr_list)):
			if len(tr_list[i]) < 2:
				pass
			elif tr_list[i][1].text == None: # 선거인수 칸이 blank인 줄을 찾으면, 그 칸 아래가 실득표수이므로...
				candidate_num = 0
				name_party_name = []
				votes_num_percent = []

				district = tr_list[i][0]#.text # 여기 저장되는 district 이름은 선거구 단위의 기초자치단체명임 ㅇㅇ
				electorates = tr_list[i+1][num_ths_left-2]#.text
				counted_vote = tr_list[i+1][num_ths_left-1]#.text

				for j in range(max_candidate_num):
					index = num_ths_left + j
					if (tr_list[i][index].findtext('strong') != None) \
								and (tr_list[i][index].findtext('strong') != '') \
								and (tr_list[i][index].text != '계'):
						candidate_num = candidate_num+1
						name_party_name.append(tr_list[i][index]) #element: <td><strong>한나라당<br>김광영</strong></td>
						votes_num_percent.append(tr_list[i+1][index]) #element: <td>3,050<br>(4.09)</td>

					cand_list = list(map(lambda x, y: dict(list(zip(self.attrs_result, [x, y]))), name_party_name, votes_num_percent)) #('name': <td><strong>한나라당<br>김광영</strong></td>, 'vote': <td>3,050<br>(4.09)</td>)

				valid_vote = tr_list[i+1][num_ths_left + max_candidate_num+0]#.text
				undervote = tr_list[i+1][num_ths_left + max_candidate_num+1]#.text
				blank_ballot = tr_list[i+1][num_ths_left + max_candidate_num+2]#.text

				district_info = (district, electorates, counted_vote, candidate_num, cand_list, valid_vote, undervote, blank_ballot)
				district_info = dict(list(zip(self.attrs_district, district_info)))
				consti_list.append(district_info)

		consti_list = [self.parse_consti(consti, city_name=city_name) for consti in consti_list]
		print('crawled #%d - %s, %s(%d)...' % (self.nth, '지역구', city_name, len(consti_list)))
		return consti_list



	def parse(self, url, is_proportional, city_name=None):
		if is_proportional: return self.parse_proportional(url, city_name)
		else: return self.parse_constituency(url, city_name)




	def parse_record(self, record, attr_list):
		for attr in attr_list:
			if attr not in self.attrs_exclude_parse_cell:
				record[attr] = parse_cell(record[attr])

	def parse_dict_record(self, record, attr_list): #parse_record와 비슷. 단, 받은 record(list type)의 element가 dict type.
		for element in record:
			for attr in attr_list:
				if attr not in self.attrs_exclude_parse_cell:
					element[attr] = parse_cell(element[attr])


	def parse_consti(self, consti, city_name=None):
		self.parse_record(consti, self.attrs_district)
		self.parse_dict_record(consti['result'], self.attrs_result)

		# never change the order
		consti['assembly_no'] = self.nth

		self.parse_district(consti, city_name)
		self.parse_electorate(consti)
		self.parse_counted_votes(consti)
		self.parse_result(consti)
		self.parse_valid_votes(consti)
		self.parse_undervotes(consti)
		self.parse_blank_ballots(consti)

		return consti


	def parse_district(self, consti, city_name):
		if city_name:
			consti['district'] = '%s %s' % (city_name, consti['district'])

	def parse_electorate(self, consti):
		if 'electorates' not in consti: return

		if type(consti['electorates']) == type([]): #nth != 20
			consti['electorates'] = sanitize(consti['electorates'][0])
		else:
			consti['electorates'] = sanitize(consti['electorates'])
		consti['electorates'] = consti['electorates'].replace(',', '')

	def parse_counted_votes(self, consti):
		if 'counted_votes' not in consti: return

		if type(consti['counted_votes']) == type([]): #nth != 20
			consti['counted_votes'] = sanitize(consti['counted_votes'][0])
		else:
			consti['counted_votes'] = sanitize(consti['counted_votes'])
		consti['counted_votes'] = consti['counted_votes'].replace(',', '')

	def parse_result(self, consti):
		if 'result' not in consti: return

		for candi in consti['result']:
			self.parse_candi(candi)

	def parse_valid_votes(self, consti):
		if 'valid_votes' not in consti: return

		consti['valid_votes'] = consti['valid_votes'].replace(',', '')

	def parse_undervotes(self, consti):
		if 'undervotes' not in consti: return

		consti['undervotes'] = consti['undervotes'].replace(',', '')

	def parse_blank_ballots(self, consti):
		if 'blank_ballots' not in consti: return

		consti['blank_ballots'] = consti['blank_ballots'].replace(',', '')

	def parse_candi(self, candi):
		if self.is_proportional: #is_proportional
			candi['party_name_kr'] = sanitize(candi['name'])
			del candi['name']

		else: #!is_proportional
			[candi['party_name_kr'], candi['name_kr']] = list(map(sanitize, candi['name'][:2]))
			del candi['name']

		[candi['votenum'], candi['voterate']] = list(map(sanitize, candi['vote'][:2]))
		candi['votenum'] = candi['votenum'].replace(',', '')
		del candi['vote']



class MultiCityCrawler(BaseCrawler):

	def city_codes(self):
		list_ = get_json(self.url_city_codes_json)['jsonResult']['body']
		return [(x['CODE'], x['NAME']) for x in list_]

	def url_list(self, city_code):
		return self.url_list_base + str(city_code)

	def crawl(self):
		# 지역구 대표
		jobs = []
		is_proportional = self.is_proportional
		if is_proportional:
			voting_system = "proportional"
		else:
			voting_system = "constituency"

		print("Waiting to connect http://info.nec.go.kr server (%s)..." % voting_system)
		for city_code, city_name in self.city_codes():
			req_url = self.url_list(city_code)
			job = gevent.spawn(self.parse, req_url, is_proportional, city_name)
			jobs.append(job)
		gevent.joinall(jobs)
		every_result = [{'voting_system':voting_system, 'results':flatten(job.get() for job in jobs)}]

		# 비례대표
		if hasattr(self, 'prop_crawler'):
			prop_result = self.prop_crawler.crawl()
			every_result.extend(prop_result)


		return every_result

class SinglePageCrawler(BaseCrawler):

	def crawl(self):
		people = self.parse(self.url_list)
		return people
