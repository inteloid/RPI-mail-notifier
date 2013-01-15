#!/usr/bin/env python

import RPi.GPIO as GPIO, imaplib, time, shlex

DEBUG = 1

USERNAME = "harut.martirosyan"     # just the part before the @ sign, add yours here
PASSWORD = "Zabr!sk!epo!nT"

MAIL_CHECK_FREQ = 1      # check mail every 60 seconds

GPIO.setmode(GPIO.BCM)
PIN_SPK = 18
PIN_RED_LED = 23
GPIO.setup(PIN_SPK, GPIO.OUT)
GPIO.setup(PIN_RED_LED, GPIO.OUT)

while True:
	try:
	        obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
	        obj.login(USERNAME, PASSWORD)
	        obj.select('Inbox', readonly=True)
	        res = obj.search(None,'UnSeen')
		if len(res) == 2:
			lusine = False
			nums = shlex.split(res[1][0])
			for num in nums:
				type, data = obj.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
				if "lusine.artenyan" in data[0][1]:
					lusine = True
					print lusine
					break
			if lusine:
				GPIO.output(PIN_SPK, True)
			else:	
				GPIO.output(PIN_SPK, False)
			unread_count = len(nums)
			if unread_count > 0:
				GPIO.output(PIN_RED_LED, True)
		        else:
		                GPIO.output(PIN_RED_LED, False)
	        
		if DEBUG:
			print(res)
	except:
		print "Exception"
	time.sleep(MAIL_CHECK_FREQ)
