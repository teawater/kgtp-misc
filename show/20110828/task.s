#output how much time each task used in CPU 0
#		sched_info_switch(prev, next);
#		perf_event_task_sched_out(prev, next);
#		rq->nr_switches++;
#		rq->curr = next;
#		++*switch_count;
#		context_switch(rq, prev, next); /* unlocks the rq */

set $tmp=0
while $tmp<$cpu_number
  eval "tvariable $pc_first_%d=1",$tmp
  eval "tvariable $pc_begin_%d=1",$tmp
  eval "tvariable $pc_pid_%d=1",$tmp
  set $tmp=$tmp+1
end

set circular-trace-buffer on

#Must before context_switch
list schedule
#For 32
#trace 5821 if ($pc_first_0 == 1)
#For 3.0.0-rc6+
#trace 4282 if ($pc_first_0 == 1)
#For 3.1.0-rc2+
trace 4351 if ($pc_first_0 == 1)
action
  collect $no_self_trace
  teval $pc_begin_0 = $cooked_clock
  teval $pc_first_0 = 0
end

list schedule
#For 32
#trace 5821 if ($pc_first_0 == 0)
#For 3.0.0-rc6+
#trace 4282 if ($pc_first_0 == 0)
#For 3.1.0-rc2+
trace 4351 if ($pc_first_0 == 0)
action
  collect $no_self_trace
  collect $cpu_id
  teval $pc_pid_0 = (uint64_t)((struct task_struct *)$current_task)->pid
  collect $pc_pid_0
  teval $pc_begin_0 = $cooked_clock - $pc_begin_0
  collect $pc_begin_0
  teval $pc_begin_0 = $cooked_clock
  collect ((struct task_struct *)$current_task)->comm
end

trace do_exit if ($pc_first_0 == 0)
action
  collect $no_self_trace
  collect $cpu_id
  teval $pc_pid_0 = (uint64_t)((struct task_struct *)$current_task)->pid
  collect $pc_pid_0
  teval $pc_begin_0 = $cooked_clock - $pc_begin_0
  collect $pc_begin_0
  collect ((struct task_struct *)$current_task)->comm
  teval $pc_first_0 = 1
end
