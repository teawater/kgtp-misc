#!/usr/bin/python

import gdb
import time

MAX_NUMNODES = 1
NR_LRU_LISTS = long(gdb.parse_and_eval("NR_LRU_LISTS"))
lru_offset = long(gdb.parse_and_eval("((size_t) &(((struct page *)0)->lru))"))
list_next_offset = long(gdb.parse_and_eval("((size_t) &(((struct list_head *)0)->next))"))

page_num = 0

print time.time()
for i in range(0, MAX_NUMNODES):
	for j in range(0, long(gdb.parse_and_eval("node_data[" + str(i) + "]->nr_zones"))):
		for k in range (0, NR_LRU_LISTS):
			print "node_data["+str(i)+"]->node_zones["+str(j)+"]->lru["+str(k)+"]->list";
			#&(node_data[i]->node_zones[j]->lru[k]->list)
			plist = long(gdb.parse_and_eval("&(node_data[" + str(i) + "]->node_zones[" + str(j) + "]->lru[" + str(k) + "]->list)"))
			#&(node_data[i]->node_zones[j]->lru[k]->list)->next
			#pnext = long(gdb.parse_and_eval("((struct list_head *)"+ str(plist) + ")->next"))
			pnext = long(gdb.parse_and_eval("*(void **)" + str(plist + list_next_offset)))
			while (pnext != plist):
				#page's addr
				page_addr = pnext - lru_offset
				#print long(gdb.parse_and_eval("((struct page *)" + str(page_addr) + ")->flags"))
				page_num += 1
				#pnext = long(gdb.parse_and_eval("((struct list_head *)"+ str(pnext) + ")->next"))
				pnext = long(gdb.parse_and_eval("*(void **)" + str(pnext + list_next_offset)))
				if page_num >= 10000:
					print time.time()
					exit(0)
print page_num
