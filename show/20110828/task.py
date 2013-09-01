#!/usr/bin/python

import signal;
import gdb;

pid_list = [];
all_clock = [];
all_count = [];
keep_running = 1;

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

def print_top(comm, cpu_id, num):
	for e in comm:
		if e[1]["clock"] == 0:
			continue;
		print e[0], e[1]["comm"], ":", e[1]["clock"],"(%",float(e[1]["clock"])/float(all_clock[cpu_id])*100,")", float(e[1]["count"]),"(%",float(e[1]["count"])/float(all_count[cpu_id])*100,")";
		if num > 0:
			num -= 1;
			if num <= 0:
				break;

def print_pid():
	global pid_list;
	global all_clock;
	global all_count;
	try:
		for i in range(0, len(pid_list)):
			print "CPU"+str(i);
			print "Pass", all_clock[i], "Switch", all_count[i], "times";
			print_top (sorted(pid_list[i].items(), key=lambda d:d[1]["clock"], reverse=True), i, 0);
	except:
		print "Get something wrong."

def sigint_handler(num, e):
	global keep_running;

	print_pid();

	try:
		s = raw_input('Continue? (yes)')
	except:
		s = 'y'
	if s[0:1] == 'n' or s[0:1] == 'N':
		keep_running = 0;

def increase_list(num):
	for i in range(0, num):
		pid_list.append({});
		all_clock.append(0);
		all_count.append(0);

gdb.execute("set pagination off", True, True);

signal.signal(signal.SIGINT, sigint_handler);
signal.siginterrupt(signal.SIGINT, False);

schedule_id = 2;
do_exit_id = 3;

#Make sure this is connect gdbframe or not, if not, gtpframe_pipe = 1
gtpframe_pipe = 0;
if str(gdb.selected_thread()) == "None":
	gtpframe_pipe = 1
	gdb.execute("target tfile /sys/kernel/debug/gtpframe_pipe");

exit_count = 0;
increase_list(1);

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

		if tid == schedule_id or tid == do_exit_id:
			cpu_id = int(gdb.parse_and_eval("$cpu_id"));
			if cpu_id >= len(pid_list):
				increase_list(cpu_id + 1 - len(pid_list));
			pid = long(gdb.parse_and_eval("$pc_pid_"+str(cpu_id)));
			clock = long(gdb.parse_and_eval("$pc_begin_"+str(cpu_id)));
			if pid in pid_list[cpu_id]:
				pid_list[cpu_id][pid]["clock"] += clock;
				pid_list[cpu_id][pid]["count"] += 1;
			else:
				pid_list[cpu_id][pid]={};
				pid_list[cpu_id][pid]["clock"] = clock;
				pid_list[cpu_id][pid]["count"] = 1;
				pid_list[cpu_id][pid]["comm"] = str(gdb.parse_and_eval("((struct task_struct *)$current_task)->comm"));
			all_clock[cpu_id] += clock;
			all_count[cpu_id] += 1;
			if tid == do_exit_id:
				exit_pid = "exited " + str(exit_count) + " " + str(pid);
				exit_count += 1;
				pid_list[cpu_id][exit_pid]={};
				pid_list[cpu_id][exit_pid]["clock"] = pid_list[cpu_id][pid]["clock"];
				pid_list[cpu_id][exit_pid]["count"] = pid_list[cpu_id][pid]["count"];
				pid_list[cpu_id][exit_pid]["comm"] = pid_list[cpu_id][pid]["comm"];
				pid_list[cpu_id][pid]["clock"] = 0;
				pid_list[cpu_id][pid]["count"] = 0;
				pid_list[cpu_id][pid]["comm"] = "";
		else:
			raise gdb.error ("Trace id error.");

	except gdb.error, x:
		print("Drop one entry because", x);
	except gdb.MemoryError, x:
		print("Drop one entry because", x);
	except RuntimeError, x:
		print("Drop one entry because", x);

	if gtpframe_pipe and tfind_done:
		gdb.execute("tfind", False, True);

if keep_running:
	print_pid();
