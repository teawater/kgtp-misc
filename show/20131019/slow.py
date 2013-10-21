#!/usr/bin/python

import gdb
import re

gdb.execute("tfind -1", False, True)
cpu_number = int(gdb.parse_and_eval("$cpu_number"))
slow = []
for i in range(0, cpu_number):
	#p_cc, $trace_frame, unlock_function_name
	slow.append([0, -1, ""])
get_cpu = cpu_number

frame_count = gdb.execute("tstatus", False, True)
frame_count = re.findall("Collected \d+ trace frames", frame_count)
frame_count = re.findall("\d+", frame_count[0])
frame_count = int(frame_count[0])

for i in range(frame_count - 1, -1, -1):
	try:
		gdb.execute("tfind "+str(i), False, True)
		cpu_id = int(gdb.parse_and_eval("$cpu_id"))
		if (slow[cpu_id][1] < 0):
			slow[cpu_id][0] = int(gdb.parse_and_eval("$p_cc"))
			slow[cpu_id][1] = i
			slow[cpu_id][2] = str(gdb.execute("p $rip", False, True))
			get_cpu -= 1
	except:
		pass
	if get_cpu <= 0:
		break

for i in range(0, cpu_number):
	if slow[i][1] >= 0:
		print "CPU"+str(i)+"\tframe "+str(slow[i][1])+"\ttime "+str(slow[i][0])+"\tfunction "+str(slow[i][2])
