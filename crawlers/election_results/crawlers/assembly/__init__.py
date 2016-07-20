#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from . import counting_vote
from utils import InvalidCrawlerError

def Crawler(_type, nth):
    if _type == 'electorates':
        raise NotImplementedError('Assembly electorates crawler')
    elif _type == 'counting_vote':
        return counting_vote.Crawler(nth)
    else:
        raise InvalidCrawlerError('assembly', _type, nth)
