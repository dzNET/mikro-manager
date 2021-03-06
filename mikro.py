#!/usr/bin/env python
import sys, os
from RosAPI import Core

print "##########################################\n# Welcome to the Mikrotik manager script #\n##########################################\n\n"

try:
	if len(sys.argv) == 4:
		
		ip = sys.argv[1]
		user = sys.argv[2]
		pwd = sys.argv[3]
	
	else:
		
		print "\n#\nIncorrect argumanets! Example: mikro.py 192.168.88.1 admin passwd\n#"
	
	if (os.system("ping -c 1 -w2 " + ip + " > /dev/null")) == 0:
		
		print "Try to connect..... wait\n"
		mk = Core(ip)
		mk.login(user, pwd)
		print "Connected successfuly!\n"
		
		res = mk.talk(["/system/resource/print"])
		res = res[0][1]
		
		print 'Your board: %s\nUptime is: %s' % (res["=board-name"], res["=uptime"])
		print "\n\nYou are in an interactive menu\n-\nExample for change SSID: 'set ssid new_ssid'\n-\
		\nShow all command example: 'help'\n-\nEnter 'quit' for Exit\n"
		
		def menu():
			while True:				
				word = raw_input("\n\tYour choise: ").split()
				if word[0] == "quit":
					break
				elif word[0] == "set":
					if word[1] == "ssid" and len(word) > 2:
						res = mk.talk(["/interface/wireless/set", "=.id=wlan2", "=ssid=" + word[2]])
						print '\nResult: %s' % (res[0][0])
						for key in mk.talk(["/interface/wireless/print"]):
							if key[0] == "!re":
								print '\nYour %s SSID are: %s' % (key[1]["=name"], key[1]["=ssid"])
					elif word[1] == "limit":
						print "\ntimeOut Menu"
					else:
						print "\nwrong ithem"
				elif word[0] == "print":
					if word[1] == "res":
						res = mk.talk(["/system/resource/print"])
						res = res[0][1]
						print '\nBoard: %s\nUptime: %s\nCPU load: %s\nFree memory: %.2f Mb\nFree space: %.2f Mb\nFirmware: %s\n' %\
						(res["=board-name"], res["=uptime"], res["=cpu-load"], float(res["=free-memory"])/1024/1024, \
						float(res["=free-hdd-space"])/1024/1024, res["=version"])
					elif word[1] == "ssid":
						for key in mk.talk(["/interface/wireless/print"]):
							if key[0] == "!re":
								print '\nYour %s SSID are: %s' % (key[1]["=name"], key[1]["=ssid"])
					elif word[1] == "limit":
						print "\ntimeOut Menu"
					elif word[1] == "users":
						for key in mk.talk(["/ip/hotspot/user/print"]):
							if key[0] == "!re":
								if key[1]["=.id"] != "*0":
									print '\nUser: %s\nUptime: %s\nUptime limit: %s\nMAC-address: %s\nByte IN: %f\nByte OUT: %f\n' %\
									(key[1]["=.id"], key[1]["=uptime"], key[1]["=limit-uptime"], key[1]["=mac-address"],\
									key[1]["=bytes-in"], key[1]["=bytes-out"])
					elif word[1] == "host":
						for key in mk.talk(["/ip/hotspot/host/print"]):
							if key[0] == "!re":
								print '\nHost: %s\nUptime: %s\nMAC-address: %s\nIP-address: %s\nAuth: %s\nDead time: %s\n' %\
								(key[1]["=.id"], key[1]["=uptime"], key[1]["=mac-address"], key[1]["=address"],\
								key[1]["=authorized"], key[1]["=host-dead-time"])
				elif word[0] == "help":
					print "\n# Setting\n\tset ssid new_ssid\n\tset limit 12:00:00  # 12 hours\
					\n# Printing\n\tprint res\n\tprint ssid\n\tprint limit\n\tprint users\n\tprint host\nhelp\nquit"
				else:
					print "\nwrong ithem"
		menu()

	else:
		print ip, 'is down! Check router internet connection!\n'	
except:
	print "\nException:\n\t Oooops.... \n"
else:
	print "\nHave a nice day!\n"
