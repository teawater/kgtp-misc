#!/usr/bin/python

import os

always_yes = False

have_quilt = True

while 1:
	try:
		n = raw_input("Want alway answer yes?[n]/y:")
		if n == 'y':
			always_yes = True
		elif n != '' and n != 'n':
			continue
	except:
		continue
	break

def query_continue():
	if not always_yes:
		while 1:
			try:
				n = raw_input("Continue?")
			except:
				continue
			if n == "y":
				break
			elif n == "n":
				exit(0)

def version_num (v_string):
	ret = 0

	if v_string[0:1] != 'v':
		return 9999999999999999999999
	else:
		v_string = v_string[1:]
	v_string = v_string.split(".")
	if len (v_string) == 2:
		v_string.append (0)
	if len (v_string) != 3:
		raise Exception("Version \""+v_string+"\" format error.")
	move = 0
	for v in reversed(v_string):
		ret += int(v) << move
		move += 8
	return ret

home = os.path.expandvars('$HOME')

srcdir = home+"/kernel/kgtp/"

#Get kernel_src and kernel_b
print("With directory you want to use?")
print("1 "+home+"/kernel/")
print("2 "+home+"/kernel2/")
kernel_dir = ""
while 1:
	try:
		n = input("select:")
		if n == 1:
			kernel_dir = home+"/kernel/"
		elif n == 2:
			kernel_dir = home+"/kernel2/"
		else:
			continue
	except:
		continue
	break
kernel_src = kernel_dir + "linux/"
kernel_b = kernel_dir + "b/"
kernel_barm = kernel_dir + "barm/"
kernel_taobao_src = home+"/taobao/ali_kernel/"
kernel_taobao_b = home+"/taobao/bk/"

#call command
def callcmd(cmd, arch="local"):
	if cmp(arch, "arm") == 0:
		cmd += ' ARCH=arm CROSS_COMPILE=arm-linux-gnueabi-'
	if os.system(cmd) != 0:
		raise Exception("Call \""+cmd+"\" got error.")

#Clear current patch dir
def clear_kernel_src():
	os.chdir(kernel_src)
	os.system("quilt refresh")
	os.system("quilt pop -a")
	callcmd("rm -rf .pc patches")

def quilt_add(name, add = False, src = ""):
	os.system("rm -rf "+name)
	if add:
		if have_quilt:
			os.system("quilt add "+name)
		callcmd("cp "+srcdir+src+" "+name)

#update patch
def update_patch(tag, patch, arch= "local"):
	vnum = version_num (tag)
	if tag == "taobao":
		#print "Make sure taobao kernel new and gtp_taobao.patch is deleted."
		#query_continue()
		os.chdir(kernel_taobao_src)
		#os.system("quilt pop -a")
		#callcmd("rm -rf .pc patches")
		callcmd("proxychains git pull https://github.com/alibaba/ali_kernel.git")
	else:
		os.chdir(kernel_src)
		callcmd("git checkout "+tag)

	if have_quilt:
		callcmd("quilt import "+srcdir+patch)
		callcmd("quilt push")
	#gtp.c
	os.system("mkdir -p lib/")
	if patch == "gtp_for_review.patch":
		os.system("kdiff3 lib/gtp.c "+srcdir+"gtp.c")
		query_continue()
	else:
		quilt_add("lib/gtp.c", True, "gtp.c")
		#Don't need this part because KGTP_API_VERSION
		#fd = open("lib/gtp.c", "r")
		#buf = fd.read()
		#fd.close()
		#buf = buf.replace("__gtp_perf_event_disable", "__perf_event_disable")
		#buf = buf.replace("__gtp_perf_event_enable", "__perf_event_enable")
		#buf = buf.replace("gtp_perf_event_enable", "perf_event_enable")
		#buf = buf.replace("gtp_perf_event_disable", "perf_event_disable")
		#buf = buf.replace("gtp_perf_event_set", "perf_event_set")
		#buf = buf.replace("#if (LINUX_VERSION_CODE < KERNEL_VERSION(3,3,0))\n\t\tif (enable)\n\t\t\tperf_event_enable(pts->event);\n\t\telse\n\t\t\tperf_event_disable(pts->event);\n#else\n\t\tif (enable)\n\t\t\tperf_event_enable(pts->event);\n\t\telse\n\t\t\tperf_event_disable(pts->event);\n#endif", "\t\tif (enable)\n\t\t\tperf_event_enable(pts->event);\n\t\telse\n\t\t\tperf_event_disable(pts->event);")
		#buf = buf.replace("#include \"perf_event.c\"\n\n","")
		#fd = open("lib/gtp.c", "w")
		#buf = fd.write(buf)
		#fd.close()
	if patch == "gtp_for_review.patch":
		os.system("kdiff3 lib/gtp_rb.c "+srcdir+"gtp_rb.c")
		query_continue()
	else:
		quilt_add("lib/gtp_rb.c", True, "gtp_rb.c")
	#doc
	if patch == "gtp_for_review.patch":
		callcmd("quilt import "+srcdir+"gtp_doc_for_review.patch")
		callcmd("quilt push")
	#os.system("mkdir -p Documentation/gtp/")
	#quilt_add("Documentation/trace/gtp.txt")
	#quilt_add("Documentation/trace/gtp_quickstart.txt")
	os.system("rm -rf Documentation/gtp/howto.txt")
	os.system("rm -rf Documentation/gtp/howtocn.txt")
	os.system("rm -rf Documentation/gtp/quickstart.txt")
	#quilt_add("Documentation/gtp/howto.txt", True, "howto.txt")
	#quilt_add("Documentation/gtp/howtocn.txt", True, "howtocn.txt")
	#quilt_add("Documentation/gtp/quickstart.txt", True, "quickstart.txt")
	#script
	if patch == "gtp_for_review.patch":
		callcmd("quilt import "+srcdir+"gtp_script_for_review.patch")
		callcmd("quilt push")
	os.system("mkdir -p scripts/gtp/add-ons/")
	quilt_add("scripts/getmod.py")
	quilt_add("scripts/getgtprsp.pl")
	quilt_add("scripts/gtp/getgtprsp.pl", True, "getgtprsp.pl")
	quilt_add("scripts/gtp/getmod.py", True, "getmod.py")
	quilt_add("scripts/gtp/add-ons/pe.py", True, "add-ons/pe.py")
	quilt_add("scripts/gtp/add-ons/hotcode.py", True, "add-ons/hotcode.py")
	quilt_add("lib/gtp.h", True, "gtp.h")
	if have_quilt:
		callcmd("quilt refresh")

	if have_quilt:
		if vnum <= version_num ("v2.6.20"):
			callcmd("quilt import ~/kernel/kgtp-misc/fix-2.6.18-build.patch")
			callcmd("quilt push")
		if tag == "taobao":
			callcmd("quilt import ~/study/kernel/taobao_build.patch")
			callcmd("quilt push")

	#try to build
	if tag == "taobao":
		#callcmd("rm -rf "+kernel_taobao_b)
		#callcmd("mkdir -p "+kernel_taobao_b)
		callcmd("quilt import ~/study/kernel/taobao_build.patch")
		callcmd("quilt push")
		os.chdir(kernel_taobao_b)
		callcmd("make -j8 bzImage", arch)
		callcmd("make lib/gtp.ko", arch)
		#callcmd("make KBUILD_SRC="+kernel_taobao_src+" -f "+kernel_taobao_src+"Makefile allmodconfig", arch)
		os.chdir(kernel_taobao_src)
		callcmd("quilt pop -a")
		callcmd("rm -rf .pc patches")
		#print "taobao patch need to be test with yourself."
		#callcmd("diffstat patches/" + patch)
		query_continue()
		#callcmd("cp patches/"+patch+" "+srcdir)
		return
	else:
		if cmp(arch, "local") == 0:
			callcmd("rm -rf "+kernel_b)
			callcmd("mkdir -p "+kernel_b)
			os.chdir(kernel_b)
		else:
			callcmd("rm -rf "+kernel_barm)
			callcmd("mkdir -p "+kernel_barm)
			os.chdir(kernel_barm)
		callcmd("make KBUILD_SRC="+kernel_src+" -f "+kernel_src+"Makefile allmodconfig", arch)
	callcmd("make modules_prepare", arch)
	callcmd("mkdir -p .tmp_versions")
	callcmd("make lib/gtp.ko", arch)
	if vnum >= version_num ("v3.0") or vnum == 0:
		callcmd("make kernel/events/core.o", arch)
	elif (arch != "arm" and vnum > version_num ("v2.6.32")) or (arch == "arm" and vnum > version_num ("v2.6.33")):
		callcmd("make kernel/perf_event.o", arch)
	callcmd("make kernel/kprobes.o", arch)
	if cmp(arch, "local") == 0:
		callcmd("make kernel/cpu.o", arch)
	#copy patch
	if tag == "taobao":
		os.chdir(kernel_taobao_src)
	else:
		os.chdir(kernel_src)
	if patch == "gtp_for_review.patch":
		os.system("perl scripts/checkpatch.pl patches/gtp_for_review.patch")
		os.system("perl scripts/checkpatch.pl patches/gtp_doc_for_review.patch")
		os.system("perl scripts/checkpatch.pl patches/gtp_script_for_review.patch")
	print "---", tag, patch, arch, "---"
	callcmd("diffstat patches/" + patch)
	#callcmd("head -n 20 patches/" + patch)
	if patch == "gtp_for_review.patch":
		callcmd("diffstat patches/gtp_doc_for_review.patch")
		callcmd("diffstat patches/gtp_script_for_review.patch")
	query_continue()
	callcmd("cp patches/"+patch+" "+srcdir)
	if patch == "gtp_for_review.patch":
		callcmd("cp patches/gtp_doc_for_review.patch "+srcdir)
		callcmd("cp patches/gtp_script_for_review.patch "+srcdir)

clear_kernel_src()
callcmd("git checkout -f master")
callcmd("proxychains git pull")

update_patch("v2.6.18", "gtp_older_to_2.6.19.patch")
clear_kernel_src()

update_patch("v2.6.19", "gtp_older_to_2.6.19.patch")
clear_kernel_src()

update_patch("v2.6.20", "gtp_2.6.20_to_2.6.32.patch")
clear_kernel_src()
#ARM support kprobes from 2.6.25
update_patch("v2.6.25", "gtp_2.6.20_to_2.6.32.patch", "arm")
clear_kernel_src()

update_patch("v2.6.32", "gtp_2.6.20_to_2.6.32.patch", "arm")
clear_kernel_src()
update_patch("v2.6.32", "gtp_2.6.20_to_2.6.32.patch")
clear_kernel_src()

update_patch("v2.6.33", "gtp_2.6.33_to_2.6.38.patch", "arm")
clear_kernel_src()
update_patch("v2.6.33", "gtp_2.6.33_to_2.6.38.patch")
clear_kernel_src()

update_patch("v2.6.38", "gtp_2.6.33_to_2.6.38.patch", "arm")
clear_kernel_src()
update_patch("v2.6.38", "gtp_2.6.33_to_2.6.38.patch")
clear_kernel_src()

update_patch("v2.6.39", "gtp_2.6.39.patch", "arm")
clear_kernel_src()
update_patch("v2.6.39", "gtp_2.6.39.patch")
clear_kernel_src()

update_patch("v3.0", "gtp_3.0_to_3.6.patch", "arm")
clear_kernel_src()
update_patch("v3.0", "gtp_3.0_to_3.6.patch")
clear_kernel_src()

update_patch("v3.6", "gtp_3.0_to_3.6.patch", "arm")
clear_kernel_src()
update_patch("v3.6", "gtp_3.0_to_3.6.patch")
clear_kernel_src()

update_patch("v3.7", "gtp_3.7_to_upstream.patch", "arm")
clear_kernel_src()
update_patch("v3.7", "gtp_3.7_to_upstream.patch")
clear_kernel_src()

update_patch("master", "gtp_3.7_to_upstream.patch", "arm")
clear_kernel_src()
update_patch("master", "gtp_3.7_to_upstream.patch")
clear_kernel_src()

#have_quilt = False
#update_patch("taobao", "gtp_taobao.patch")
#have_quilt = True

#update_patch("master", "gtp_for_review.patch")
#clear_kernel_src()

