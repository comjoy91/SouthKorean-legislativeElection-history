#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

import html5lib
import itertools
import json
import os
import re
import urllib.request
import requests
from time import sleep
from lxml import etree

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) "\
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"

schars_re = re.compile('[/\(\)]')
ws_re = re.compile('\s')

class InvalidCrawlerError(Exception):
    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return ' '.join(self.args)

def check_dir(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

def flatten(rarray):
    return list(itertools.chain.from_iterable(rarray))

def get_json(url):
    """
    request = urllib.request.Request(url)
    request.add_header("User-Agent", USER_AGENT)
    f = urllib.request.urlopen(request)
    txt = f.read().decode('UTF-8')
    return json.loads(txt)
    """
    sleep(0.05)
    r = requests.get(url, timeout = 10)
    txt = r.text
    return json.loads(txt)

def get_xpath(url, xpath):
    """
    htmlparser = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)
    """
    """
    request = urllib.request.Request(url)
    request.add_header("User-Agent", USER_AGENT)
    f = urllib.request.urlopen(request)

    page = htmlparser.parse(f)
    return page.xpath(xpath)
    """
    """
    sleep(0.08)
    r = requests.get(url, timeout=30)
    page = htmlparser.parse(r.content)
    return page.xpath(xpath)
    """
    sleep(0.075)
    htmlparser = etree.HTMLParser()
    page = etree.parse(url, htmlparser)
    return page.xpath(xpath)


def parse_cell(node):
    arr = _parse_cell(node)
    if not arr:
        return ''
    elif len(arr) == 1:
        return arr[0]
    else:
        return arr

def _parse_cell(node):
    parts = ([node.text] +
			 flatten(_parse_cell(c) for c in node.getchildren()) +
			 [node.tail])
    # filter removes possible Nones in texts and tails
    filtered = filter(None, parts)
    stringified = ((''+x).strip() for x in filtered)
    strings = [x for x in stringified if len(x)]
    return strings

def sanitize(txt):
    return schars_re.sub('', txt)

def split(txt):
    splitted = schars_re.split(txt)
    concatenated = [ws_re.sub('', s) for s in splitted]
    return concatenated
