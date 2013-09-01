#!/usr/bin/python

import signal;
import gdb;

clock = 0;
time = 0;

def tfind_entry(num):
	signal.siginterrupt(signal.SIGINT, True);
	if num < 0:
		tid = gdb.execute("tfind", False, True);
	else:
		tid = gdb.execute("tfind "+str(num), False, True);
	signal.siginterrupt(signal.SIGINT, False);
	if tid.find(", tracepoint ") < 0:
		return -1;
	tid = tid[tid.find(", tracepoint ") + len(", tracepoint "):];
	return int(tid);

def sigalrm_handler(num, e):
	global clock, time;

	if time == 0:
		print time;
	else:
		print clock/time, time;
	clock = 0;
	time = 0;

def sigint_handler(num, e):
	global keep_running;

	signal.setitimer(signal.ITIMER_REAL, 0);
	try:
		s = raw_input('Continue? (yes)')
	except:
		s = 'y'
	if s[0:1] == 'n' or s[0:1] == 'N':
		keep_running = 0;
	else:
		signal.setitimer(signal.ITIMER_REAL, 1, 1);

gdb.execute("set pagination off", True, True);

signal.signal(signal.SIGALRM, sigalrm_handler);
signal.signal(signal.SIGINT, sigint_handler);
signal.siginterrupt(signal.SIGINT, False);

#Make sure this is connect gdbframe or not, if not, gtpframe_pipe = 1
gtpframe_pipe = 0;
if str(gdb.selected_thread()) == "None":
	gtpframe_pipe = 1
	gdb.execute("target tfile /sys/kernel/debug/gtpframe_pipe");

signal.setitimer(signal.ITIMER_REAL, 1, 1);

keep_running = 1;
while keep_running:
	try:
		tfind_done = 0;
		if gtpframe_pipe:
			tid = tfind_entry(0);
			if tid < 0:
				raise gdb.error("tfind");
		else:
			tid = tfind_entry(-1);
			if tid < 0:
				break;
		tfind_done = 1;

		cpu_id = str(gdb.parse_and_eval("$cpu_id"));
		clock += long(gdb.parse_and_eval("$pc_pe_val_00_"+cpu_id));
		time += 1;

	except gdb.error, x:
		#print("Drop one entry because", x);
		pass;
	except gdb.MemoryError, x:
		print("Drop one entry because", x);
	except RuntimeError, x:
		print("Drop one entry because", x);

	if gtpframe_pipe and tfind_done:
		gdb.execute("tfind", False, True);

if keep_running:
	print_pid();
