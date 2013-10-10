#!/usr/bin/python

import gdb

MAX_NUMNODES = 1
NR_LRU_LISTS = long(gdb.parse_and_eval("NR_LRU_LISTS"))
lru_offset = long(gdb.parse_and_eval("((size_t) &(((struct page *)0)->lru))"))

page_num = 0

for i in range(0, MAX_NUMNODES):
	for j in range(0, long(gdb.parse_and_eval("node_data[" + str(i) + "]->nr_zones"))):
		for k in range (0, NR_LRU_LISTS):
			#&(node_data[i]->node_zones[j]->lru[k]->list)
			plist = long(gdb.parse_and_eval("&(node_data[" + str(i) + "]->node_zones[" + str(j) + "]->lru[" + str(k) + "]->list)"))
			#&(node_data[i]->node_zones[j]->lru[k]->list)->next
			pnext = long(gdb.parse_and_eval("((struct list_head *)"+ str(plist) + ")->next"))
			while (pnext != plist):
				#page's addr
				page_addr = pnext - lru_offset
				page_num += 1
				pnext = long(gdb.parse_and_eval("((struct list_head *)"+ str(pnext) + ")->next"))
print page_num