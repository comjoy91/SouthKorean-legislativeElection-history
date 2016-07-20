#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from hanja import name_cn_re
import re

__all__ = ['validate']

name_kr_re = re.compile(r'[\sㄱ-ㅎ가-힣]+$', re.UNICODE)
party_re = re.compile(r'[\s!·0-9ㄱ-ㅎ가-힣]+$', re.UNICODE)

def is_name_kr(txt):
    return 2 <= len(txt) and name_kr_re.match(txt)

def is_name_cn(txt):
    return name_cn_re.match(txt)

def is_party(txt):
    return party_re.match(txt)

def is_digit(txt):
    return txt.isdigit()

validators = {
        'name_kr': is_name_kr,
        'name_cn': is_name_cn,
        'party': is_party,
        'cand_no': is_digit
    }

class InvalidPersonDataException(Exception):

    def __init__(self, obj, field):
        self.obj = obj
        self.field = field

    def __str__(self):
        return "'%s'의 '%s'가 잘못되었습니다: %s" % (
                self.obj['name_kr'], self.field, self.obj[self.field])

def validate(data):
    try:
        for datum in data:
            validate_one(datum)

    except InvalidPersonDataException as e:
        print(e)

def validate_one(d):
    for fieldname, validator in validators.items():
        if fieldname in d and not validator(d[fieldname]):
            raise InvalidPersonDataException(d, fieldname)


def main(argv):
    if not argv:
        print('[ERROR] filename not specified')
        print('Usage: validator.py [<file>]+')
        print('  file: json file that contains a list of people data')
        return 1

    import json
    for filename in argv:
        print('validating %s' % (filename))
        with open(filename, 'r') as f:
            data = json.load(f, encoding='UTF-8')
            validate(data)

if __name__ == '__main__':
    import sys
    code = main(sys.argv[1:]) or 0
    sys.exit(code)
