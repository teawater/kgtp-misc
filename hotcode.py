#!/usr/bin/python

# This script is used to find the hotcode in some tasks
# GPL
# Copyright(C) Hui Zhu (teawater@gmail.com), 2012

import gdb
import tempfile
import os
import signal

debug_dir = "/usr/lib/debug/"

from operator import itemgetter
def dict_sort(d, reverse=False):
	#proposed in PEP 265, using  the itemgetter
	return sorted(d.iteritems(), key=itemgetter(1), reverse=True)

def sigint_handler(num, e):
	hotcode_show()
	try:
		s = raw_input('Continue? (yes)')
	except:
		s = 'y'
	finally:
		if s[0:1] != 'n' and s[0:1] != 'N':
			return;
	#gdb.execute("inferior 1")
	try:
		gdb.execute("tfind -1", True, False)
		gdb.execute("target remote /sys/kernel/debug/gtp", True, False)
		gdb.execute("set disconnected-tracing off", True, False)
	except:
		print "Try to stop GTP got error, please use command \"sudo rmmod gtp.ko\" stop it."
	exit(1);

def add_inferior():
	fid = gdb.execute("add-inferior", False, True)
	if fid.find("Added inferior ") != 0:
		return -1
	fid = int(fid[len("Added inferior "):])
	return fid

def get_addr_range_list(fun):
	buf = gdb.execute("info line "+fun, False, True)
	line_list = buf.split(os.linesep)
	ret = []
	begin = -1
	end = -1
	for line in line_list:
		addr_begin = line.find("starts at address ")
		if addr_begin >= 0:
			line = line[addr_begin + len("starts at address "):]
			addr_end = line.find(" <"+fun)
			if addr_end >= 0:
				begin = int(line[:addr_end], 0)
				line = line[addr_end + len(" <"+fun):]
		addr_begin = line.find("ends at ")
		if addr_begin >= 0:
			line = line[addr_begin + len("ends at "):]
			addr_end = line.find(" <"+fun)
			if addr_end > 0:
				end = int(line[:addr_end], 0)
				if begin != -1:
					ret.append([begin, end])
				begin = -1
				end = -1

	if len(ret) > 0:
		buf = gdb.execute("disassemble "+fun, False, True)
		line_list = buf.split(os.linesep)
		line_list.reverse()
		end = 0
		for line in line_list:
			addr_begin = line.find("0x")
			if addr_begin >= 0:
				line = line[addr_begin:]
				addr_end = line.find(" <+")
				if addr_end > 0:
					end = int(line[:addr_end], 0) + 1
					break
		if end != 0:
			offset = 0
			for c in ret:
				if c[1] < end:
					if offset == 0 or offset > (end - c[1]):
						offset = end - c[1]
			for c in ret:
				c[1] += offset

	return ret

#0 inferior_id  1 dir_name 2 kernel_list 3 user_list
task_list = {}
no_task = False
kernel_hotcode_list = {}

def task_list_add_function(is_user, pid, name):
	if no_task:
		if name in kernel_hotcode_list:
			kernel_hotcode_list[name] += 1
		else:
			kernel_hotcode_list[name] = 1
	else:
		if is_user:
			if name in task_list[pid][3]:
				task_list[pid][3][name] += 1
			else:
				task_list[pid][3][name] = 1
		else:
			if name in task_list[pid][2]:
				task_list[pid][2][name] += 1
			else:
				task_list[pid][2][name] = 1

show_line_number = 20
def hotcode_show():
	if no_task:
		print "Kernel hotcode:"
		i = 1
		for c in dict_sort(kernel_hotcode_list):
			print c[0], "\t\t", c[1]
			i += 1
			if i > show_line_number:
				break
	else:
		for pid in task_list:
			print "task", str(pid), task_list[pid][1]
			print "Kernel hotcode:"
			i = 1
			for c in dict_sort(task_list[pid][2]):
				print c[0], "\t\t", c[1]
				i += 1
				if i > show_line_number:
					break
			print "User hotcode:"
			i = 1
			for c in dict_sort(task_list[pid][3]):
				print c[0], "\t\t", c[1]
				i += 1
				if i > show_line_number:
					break
			print

gdb.execute("set target-async on", True, False)
gdb.execute("set pagination off", True, False)
gdb.execute("set confirm off", True, False)
gdb.execute("set circular-trace-buffer on", True, False)
gdb.execute("set debug-file-directory "+debug_dir, True, False)
try:
	gdb.execute("kill", True, False)
except:
	pass

trace_user = True
trace_kernel = True
while 1:
	tmp = "Both"
	try:
		tmp = raw_input('Which part of code you want trace?(User/Kernel/[Both])')
	except:
		continue
	if tmp[0:1] == 'U' or tmp[0:1] == 'u':
		trace_kernel = False
	elif tmp[0:1] == 'K' or tmp[0:1] == 'k':
		trace_user = False
	break

#Get which task pid why want to trace
print("Please input the pid of tasks that you want to trace - one per line (use empty to end input).")
print("If not set any task, will trace all code in the Kernel.")
while 1:
	pid = -1
	try:
		pid = input('id:')
	except:
		pass
	if pid <= 0:
		break
	if pid in task_list:
		print("This pid already in the list.")
		continue
	user_dir = ""
	fid = 0
	if trace_user:
		try:
			orig_user_dir = user_dir = os.path.realpath("/proc/"+str(pid)+"/exe")
		except:
			#maybe this is the kernel task
			print "Cannot get the user code info of this pid, will not parse the user level code symbol"
			task_list[pid] = (fid, user_dir, {}, {})
			continue
		if os.path.exists(debug_dir+user_dir):
			user_dir = debug_dir+user_dir
		while 1:
			tmp = ""
			try:
				tmp = raw_input('Please input the debug binary of task if you want to change it:['+user_dir+']')
			except:
				continue
			if tmp != "":
				user_dir = os.path.realpath(tmp)
			break
		if not os.path.exists(user_dir):
			print "Cannot get the user code info of this pid, will not parse the user level code symbol"
			task_list[pid] = (fid, user_dir, {}, {})
			continue
		print "Use "+user_dir+" as debug binary."
		fid = add_inferior()
		if fid < 0:
			print "Try to load task got error."
			continue
		gdb.execute("inferior "+str(fid))
		pfile = open("/proc/"+str(pid)+"/maps", "r")
		tmplist = pfile.read().split(os.linesep)
		pfile.close()
		for c in tmplist:
			c_list = c.split(" ")
			filename = c_list[-1].strip()
			if filename != orig_user_dir and os.path.exists(filename) and len(c_list) > 2 and len(c_list[1]) > 3 and c_list[1][2] == 'x':
				addr = "0x"+c_list[0][0:c.find('-')]
				gdb.execute("file "+filename)
				info_files = gdb.execute("info files", True, True)
				info_files_list = info_files.split(os.linesep)
				text_offset = "0x0"
				for line in info_files_list:
					line_list = line.split(" is ")
					if len(line_list) == 2 and line_list[1].strip() == ".text":
						line_list[0] = line_list[0].strip()
						text_offset = line_list[0][0:line_list[0].find(' - ')]
				print ("add-symbol-file "+filename+" ("+addr+"+"+text_offset+")")
				gdb.execute("add-symbol-file "+filename+" ("+addr+"+"+text_offset+")")
		gdb.execute("file "+user_dir)
		gdb.execute("inferior 1")
	task_list[pid] = (fid, user_dir, {}, {})

def get_ignore_str(function):
	ret = ""
	try:
		s = raw_input('Do you want to ignore function \"'+function+'\"? (yes)')
	except:
		s = 'y'
	if s[0:1] != 'n' and s[0:1] != 'N':
		r_list = get_addr_range_list(function)
		for r in r_list:
			if ret != "":
				ret += " && "
			else:
				ret += "&& ("
			#(regs->ip < r[0] || regs->ip > r[1])
			ret += "($pc_ip0 < "+str(r[0])+" || $pc_ip0 > "+str(r[1])+")"
		if ret != "":
			ret += ")"
	return ret

ignore_str = ""
if len(task_list) == 0:
	trace_user = False
	trace_kernel = True
	no_task = True

try:
	show_line_number = input('Show line number (0 meas all)?['+str(show_line_number)+']')
except:
	show_line_number = 20

#Set tracepoint
gdb.execute("target remote /sys/kernel/debug/gtp", True, False)

try:
	gdb.execute("tstop", True, False)
	gdb.execute("delete", True, False)
except:
	pass


def getmod():
	#following code is get from ../getmod.py
	#use the code directly because sys.argv = [''] inside GDB
	def format_file(name):
		tmp = ""
		for c in name:
			if c == "_":
				c = "-"
			tmp += c
		return tmp

	#Check if the target is available
	if str(gdb.selected_thread()) == "None":
		raise gdb.error("Please connect to Linux Kernel before use the script.")

	#Output the help
	print "Use GDB command \"set $mod_search_dir=dir\" to set an directory for search the modules."

	ignore_gtp_ko = gdb.parse_and_eval("$ignore_gtp_ko")
	if ignore_gtp_ko.type.code == gdb.TYPE_CODE_INT:
		ignore_gtp_ko = int(ignore_gtp_ko)
	else:
		ignore_gtp_ko = 1

	#Get the mod_search_dir
	mod_search_dir_list = []
	#Get dir from $mod_search_dir
	tmp_dir = gdb.parse_and_eval("$mod_search_dir")
	if tmp_dir.type.code == gdb.TYPE_CODE_ARRAY:
		tmp_dir = str(tmp_dir)
		tmp_dir = tmp_dir[1:len(tmp_dir)]
		tmp_dir = tmp_dir[0:tmp_dir.index("\"")]
		mod_search_dir_list.append(tmp_dir)
	#Get dir that same with current vmlinux
	tmp_dir = str(gdb.execute("info files", False, True))
	tmp_dir = tmp_dir[tmp_dir.index("Symbols from \"")+len("Symbols from \""):len(tmp_dir)]
	tmp_dir = tmp_dir[0:tmp_dir.index("\"")]
	tmp_dir = tmp_dir[0:tmp_dir.rindex("/")]
	mod_search_dir_list.append(tmp_dir)
	#Get the dir of current Kernel
	tmp_dir = "/lib/modules/" + str(os.uname()[2])
	if os.path.isdir(tmp_dir):
		mod_search_dir_list.append(tmp_dir)
	#Let user choice dir
	mod_search_dir = ""
	while mod_search_dir == "":
		for i in range(0, len(mod_search_dir_list)):
			print str(i)+". "+mod_search_dir_list[i]
		try:
			s = input('Select a directory for search the modules [0]:')
		except SyntaxError:
			s = 0
		except:
			continue
		if s < 0 or s >= len(mod_search_dir_list):
			continue
		mod_search_dir = mod_search_dir_list[s]

	mod_list_offset = long(gdb.parse_and_eval("((size_t) &(((struct module *)0)->list))"))
	mod_list = long(gdb.parse_and_eval("(&modules)"))
	mod_list_current = mod_list

	while 1:
		mod_list_current = long(gdb.parse_and_eval("((struct list_head *) "+str(mod_list_current)+")->next"))

		#check if need break the loop
		if mod_list == mod_list_current:
			break

		mod = mod_list_current - mod_list_offset

		#get mod_name
		mod_name = str(gdb.parse_and_eval("((struct module *)"+str(mod)+")->name"))
		mod_name = mod_name[mod_name.index("\"")+1:len(mod_name)]
		mod_name = mod_name[0:mod_name.index("\"")]
		if mod_name == "fglrx":
			contiue
		mod_name += ".ko"
		mod_name = format_file(mod_name)

		#get mod_dir_name
		mod_dir_name = ""
		for root, dirs, files in os.walk(mod_search_dir):
			for afile in files:
				tmp_file = format_file(afile)
				if tmp_file == mod_name:
					mod_dir_name = os.path.join(root,afile)
					break
			if mod_dir_name != "":
				break

		command = " "

		#Add module_core to command
		command += str(gdb.parse_and_eval("((struct module *)"+str(mod)+")->module_core"))

		#Add each sect_attrs->attrs to command
		#get nsections
		nsections = int(gdb.parse_and_eval("((struct module *)"+str(mod)+")->sect_attrs->nsections"))
		sect_attrs = long(gdb.parse_and_eval("(u64)((struct module *)"+str(mod)+")->sect_attrs"))
		for i in range(0, nsections):
			command += " -s"
			tmp = str(gdb.parse_and_eval("((struct module_sect_attrs *)"+str(sect_attrs)+")->attrs["+str(i)+"].name"))
			tmp = tmp[tmp.index("\"")+1:len(tmp)]
			tmp = tmp[0:tmp.index("\"")]
			command += " "+tmp
			tmp = str(gdb.parse_and_eval("((struct module_sect_attrs *)"+str(sect_attrs)+")->attrs["+str(i)+"].address"))
			command += " "+tmp

		if mod_dir_name == "":
			print "Cannot find out",mod_name,"from directory."
			print "Please use following command load the symbols from it:"
			print "add-symbol-file some_dir/"+mod_name+command
		else:
			if ignore_gtp_ko and mod_name == "gtp.ko":
				pass
			else:
				#print "add-symbol-file "+mod_dir_name+command
				gdb.execute("add-symbol-file "+mod_dir_name+command, False, False)

if trace_kernel:
	try:
		s = raw_input('Do you load the symbol from LKM? [no]')
	except:
		s = 'n'
	if s[0:1] == 'y' or s[0:1] == 'Y':
		getmod()

cpu_number = int(gdb.parse_and_eval("$cpu_number"))
tempfilename = tempfile.mktemp()
tempfile = open(tempfilename, "w")
if no_task:
	#Setup first tracepoint
	ignore_str += get_ignore_str("arch_local_irq_enable")
	ignore_str += get_ignore_str("intel_idle")
	# GDB have bug with long conditon so close them
	#ignore_str += get_ignore_str("__do_softirq")
	#ignore_str += get_ignore_str("_raw_spin_unlock_irqrestore")
	
	for i in range(0, cpu_number):
		tempfile.write("tvariable $pc_ip"+str(i)+"\n")
		tempfile.write("tvariable $pc_cs"+str(i)+"\n")
	tempfile.write("trace handle_irq\n")
	tempfile.write("commands\n")
	tempfile.write("teval $pc_ip0=(u64)regs->ip\n")
	tempfile.write("teval $pc_cs0=(u64)regs->cs\n")
	tempfile.write("end\n")
	#Setup second tracepoint
	tempfile.write("trace handle_irq\n")
	cond_str = " (($pc_cs0 & 3) == 0)"
	tempfile.write("condition $bpnum "+cond_str+ignore_str+"\n")
	tempfile.write("commands\n")
	tempfile.write("collect $no_self_trace\n")
	tempfile.write("collect $pc_ip0\n")
else:
	tempfile.write("trace handle_irq\n")
	pid_str = ""
	for pid in task_list:
		if pid_str != "":
			pid_str += " || "
		else:
			pid_str += "("
		pid_str += "($current_task_pid == "+str(pid)+") "
	if pid_str != "":
		pid_str += ")"
	cond_str = ""
	if not trace_user:
		if pid_str != "":
			cond_str += " && "
		cond_str += " ((regs->cs & 3) == 0)"
	elif not trace_kernel:
		if pid_str != "":
			cond_str += "&&"
		cond_str += " ((regs->cs & 3) == 3)"
	tempfile.write("condition $bpnum "+pid_str+cond_str+"\n")
	tempfile.write("commands\n")
	tempfile.write("collect regs->ip\n")
	if trace_user and trace_kernel:
		tempfile.write("collect regs->cs\n")
	tempfile.write("collect $current_task_pid\n")
tempfile.write("end\n")
tempfile.close()
tempfile = open(tempfilename, "r")
print "Tracepoint command:"
print tempfile.read()
tempfile.close()
gdb.execute("source "+tempfilename, True, False)
os.remove(tempfilename)
gdb.execute("set disconnected-tracing on", True, False)
gdb.execute("tstart")
gdb.execute("kill", True, False)

signal.signal(signal.SIGINT, sigint_handler);
signal.siginterrupt(signal.SIGINT, False);

#Connect to pipe
gdb.execute("target tfile /sys/kernel/debug/gtpframe_pipe")

def get_function_from_sym(sym):
	sym = sym.rstrip(os.linesep)
	sym_end = sym.find(" in section")
	function = ""
	if sym_end > 0:
		function = sym[0:sym_end]
		function_list = function.split(' + ')
		function_list_len = len(function_list)
		if function_list_len >= 1:
			function = function_list[0]
			filename_offset = sym.find(" of ")
			if filename_offset > 0:
				function += sym[filename_offset:]
		else:
			function = ""
	if function == "":
		function = "Unknown address"
	return function

if no_task:
	while 1:
		try:
			gdb.execute("tfind 0", False, True)
			cpu_id = long(gdb.parse_and_eval("$cpu_id"));
			sym = gdb.execute("info symbol ($pc_ip"+str(cpu_id)+" - 1)", True, True)
			function = get_function_from_sym(sym)
			task_list_add_function(False, 0, function)
		except gdb.error, x:
			print("Drop one entry because", x)
		except gdb.MemoryError, x:
			print("Drop one entry because", x)
		try:
			gdb.execute("tfind 1", False, True)
		except:
			pass
else:
	while 1:
		try:
			gdb.execute("tfind 0", False, True)
			is_user = False
			pid = long(gdb.parse_and_eval("$current_task_pid"))
			if not pid in task_list:
				raise gdb.error ("Cannot find inferior for pid "+ str(pid) +", drop one entry.")
			if trace_user and long(gdb.parse_and_eval("regs->cs & 3")) == 3:
				is_user = True
				if task_list[pid][0] == 0:
					sym = ""
				else:
					ip = long(gdb.parse_and_eval("regs->ip - 1"))
					gdb.execute("inferior "+str(task_list[pid][0]), False, True)
					sym = gdb.execute("info symbol "+str(ip), True, True)
					gdb.execute("inferior 1", False, True)
			else:
				sym = gdb.execute("info symbol (regs->ip - 1)", True, True)
			function = get_function_from_sym(sym)
			task_list_add_function(is_user, pid, function)
		except gdb.error, x:
			print("Drop one entry because", x)
		except gdb.MemoryError, x:
			print("Drop one entry because", x)
		try:
			gdb.execute("tfind 1", False, True)
		except:
			pass
