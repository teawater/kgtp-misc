#sudo gdb ./vmlinux -x softirq.source

target remote /sys/kernel/debug/gtp

define output_entry
	if ($arg2 != 0)
		printf "CPU%d ", $arg0
		output $arg1
		printf ": %u times, %.4f of total, use %u ns, %u ns per time, %.4f of total\n", $arg2, (float)$arg2/(float)$arg4, $arg3, $arg3/$arg2, (float)$arg3/(float)$arg5
	end
end
document output_entry
$arg0 is cpu id
$arg1 is softirq name
$arg2 is softirq times
$arg3 is softirq clock
$arg4 is all times of this cpu
$arg5 is all clock of this cpu
end

#CPU0

tvariable $tmp_0

#run_timer_softirq
tvariable $run_timer_softirq_0
tvariable $run_timer_softirq_t_0
trace softirq.c:238
  condition $bpnum (h->action == run_timer_softirq && $cpu_id==0)
  commands
    teval $run_timer_softirq_0=$run_timer_softirq_0+1
    teval $tmp_0=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == run_timer_softirq && $cpu_id==0)
  commands
    teval $run_timer_softirq_t_0=$run_timer_softirq_t_0+$clock-$tmp_0
  end

#run_hrtimer_softirq
tvariable $run_hrtimer_softirq_0
tvariable $run_hrtimer_softirq_t_0
trace softirq.c:238
  condition $bpnum (h->action == run_hrtimer_softirq && $cpu_id==0)
  commands
    teval $run_hrtimer_softirq_0=$run_hrtimer_softirq_0+1
    teval $tmp_0=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == run_hrtimer_softirq && $cpu_id==0)
  commands
    teval $run_hrtimer_softirq_t_0=$run_hrtimer_softirq_t_0+$clock-$tmp_0
  end

#blk_iopoll_softirq
tvariable $blk_iopoll_softirq_0
tvariable $blk_iopoll_softirq_t_0
trace softirq.c:238
  condition $bpnum (h->action == blk_iopoll_softirq && $cpu_id==0)
  commands
    teval $blk_iopoll_softirq_0=$blk_iopoll_softirq_0+1
    teval $tmp_0=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == blk_iopoll_softirq && $cpu_id==0)
  commands
    teval $blk_iopoll_softirq_t_0=$blk_iopoll_softirq_t_0+$clock-$tmp_0
  end

#blk_done_softirq
tvariable $blk_done_softirq_0
tvariable $blk_done_softirq_t_0
trace softirq.c:238
  condition $bpnum (h->action == blk_done_softirq && $cpu_id==0)
  commands
    teval $blk_done_softirq_0=$blk_done_softirq_0+1
    teval $tmp_0=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == blk_done_softirq && $cpu_id==0)
  commands
    teval $blk_done_softirq_t_0=$blk_done_softirq_t_0+$clock-$tmp_0
  end

#tasklet_action
tvariable $tasklet_action_0
tvariable $tasklet_action_t_0
trace softirq.c:238
  condition $bpnum (h->action == tasklet_action && $cpu_id==0)
  commands
    teval $tasklet_action_0=$tasklet_action_0+1
    teval $tmp_0=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == tasklet_action && $cpu_id==0)
  commands
    teval $tasklet_action_t_0=$tasklet_action_t_0+$clock-$tmp_0
  end

#tasklet_hi_action
tvariable $tasklet_hi_action_0
tvariable $tasklet_hi_action_t_0
trace softirq.c:238
  condition $bpnum (h->action == tasklet_hi_action && $cpu_id==0)
  commands
    teval $tasklet_hi_action_0=$tasklet_hi_action_0+1
    teval $tmp_0=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == tasklet_hi_action && $cpu_id==0)
  commands
    teval $tasklet_hi_action_t_0=$tasklet_hi_action_t_0+$clock-$tmp_0
  end

#net_tx_action
tvariable $net_tx_action_0
tvariable $net_tx_action_t_0
trace softirq.c:238
  condition $bpnum (h->action == net_tx_action && $cpu_id==0)
  commands
    teval $net_tx_action_0=$net_tx_action_0+1
    teval $tmp_0=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == net_tx_action && $cpu_id==0)
  commands
    teval $net_tx_action_t_0=$net_tx_action_t_0+$clock-$tmp_0
  end

#net_rx_action
tvariable $net_rx_action_0
tvariable $net_rx_action_t_0
trace softirq.c:238
  condition $bpnum (h->action == net_rx_action && $cpu_id==0)
  commands
    teval $net_rx_action_0=$net_rx_action_0+1
    teval $tmp_0=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == net_rx_action && $cpu_id==0)
  commands
    teval $net_rx_action_t_0=$net_rx_action_t_0+$clock-$tmp_0
  end

#run_rebalance_domains
tvariable $run_rebalance_domains_0
tvariable $run_rebalance_domains_t_0
trace softirq.c:238
  condition $bpnum (h->action == run_rebalance_domains && $cpu_id==0)
  commands
    teval $run_rebalance_domains_0=$run_rebalance_domains_0+1
    teval $tmp_0=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == run_rebalance_domains && $cpu_id==0)
  commands
    teval $run_rebalance_domains_t_0=$run_rebalance_domains_t_0+$clock-$tmp_0
  end

define softirq0
	printf "CPU0 softirq: %u times, %u ns, %u ns per time, %.10f of total exec clock\n", $times0=$run_timer_softirq_0+$run_hrtimer_softirq_0+$blk_iopoll_softirq_0+$blk_done_softirq_0+$tasklet_action_0+$tasklet_hi_action_0+$net_tx_action_0+$net_rx_action_0+$run_rebalance_domains_0,$clock0=$run_timer_softirq_t_0+$run_hrtimer_softirq_t_0+$blk_iopoll_softirq_t_0+$blk_done_softirq_t_0+$tasklet_action_t_0+$tasklet_hi_action_t_0+$net_tx_action_t_0+$net_rx_action_t_0+$run_rebalance_domains_t_0, $clock0/$times0, (float)$clock0/(float)($clock-$begin)

	output_entry 0 "run_timer_softirq" $run_timer_softirq_0 $run_timer_softirq_t_0 $times0 $clock0
	output_entry 0 "run_hrtimer_softirq" $run_hrtimer_softirq_0 $run_hrtimer_softirq_t_0 $times0 $clock0
	output_entry 0 "blk_iopoll_softirq" $blk_iopoll_softirq_0 $blk_iopoll_softirq_t_0 $times0 $clock0
	output_entry 0 "blk_done_softirq" $blk_done_softirq_0 $blk_done_softirq_t_0 $times0 $clock0
	output_entry 0 "tasklet_action" $tasklet_action_0 $tasklet_action_t_0 $times0 $clock0
	output_entry 0 "tasklet_hi_action" $tasklet_hi_action_0 $tasklet_hi_action_t_0 $times0 $clock0
	output_entry 0 "net_tx_action" $net_tx_action_0 $net_tx_action_t_0 $times0 $clock0
	output_entry 0 "net_rx_action" $net_rx_action_0 $net_rx_action_t_0 $times0 $clock0
	output_entry 0 "run_rebalance_domains" $run_rebalance_domains_0 $run_rebalance_domains_t_0 $times0 $clock0
end


#CPU1

tvariable $tmp_1

#run_timer_softirq
tvariable $run_timer_softirq_1
tvariable $run_timer_softirq_t_1
trace softirq.c:238
  condition $bpnum (h->action == run_timer_softirq && $cpu_id==1)
  commands
    teval $run_timer_softirq_1=$run_timer_softirq_1+1
    teval $tmp_1=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == run_timer_softirq && $cpu_id==1)
  commands
    teval $run_timer_softirq_t_1=$run_timer_softirq_t_1+$clock-$tmp_1
  end

#run_hrtimer_softirq
tvariable $run_hrtimer_softirq_1
tvariable $run_hrtimer_softirq_t_1
trace softirq.c:238
  condition $bpnum (h->action == run_hrtimer_softirq && $cpu_id==1)
  commands
    teval $run_hrtimer_softirq_1=$run_hrtimer_softirq_1+1
    teval $tmp_1=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == run_hrtimer_softirq && $cpu_id==1)
  commands
    teval $run_hrtimer_softirq_t_1=$run_hrtimer_softirq_t_1+$clock-$tmp_1
  end

#blk_iopoll_softirq
tvariable $blk_iopoll_softirq_1
tvariable $blk_iopoll_softirq_t_1
trace softirq.c:238
  condition $bpnum (h->action == blk_iopoll_softirq && $cpu_id==1)
  commands
    teval $blk_iopoll_softirq_1=$blk_iopoll_softirq_1+1
    teval $tmp_1=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == blk_iopoll_softirq && $cpu_id==1)
  commands
    teval $blk_iopoll_softirq_t_1=$blk_iopoll_softirq_t_1+$clock-$tmp_1
  end

#blk_done_softirq
tvariable $blk_done_softirq_1
tvariable $blk_done_softirq_t_1
trace softirq.c:238
  condition $bpnum (h->action == blk_done_softirq && $cpu_id==1)
  commands
    teval $blk_done_softirq_1=$blk_done_softirq_1+1
    teval $tmp_1=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == blk_done_softirq && $cpu_id==1)
  commands
    teval $blk_done_softirq_t_1=$blk_done_softirq_t_1+$clock-$tmp_1
  end

#tasklet_action
tvariable $tasklet_action_1
tvariable $tasklet_action_t_1
trace softirq.c:238
  condition $bpnum (h->action == tasklet_action && $cpu_id==1)
  commands
    teval $tasklet_action_1=$tasklet_action_1+1
    teval $tmp_1=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == tasklet_action && $cpu_id==1)
  commands
    teval $tasklet_action_t_1=$tasklet_action_t_1+$clock-$tmp_1
  end

#tasklet_hi_action
tvariable $tasklet_hi_action_1
tvariable $tasklet_hi_action_t_1
trace softirq.c:238
  condition $bpnum (h->action == tasklet_hi_action && $cpu_id==1)
  commands
    teval $tasklet_hi_action_1=$tasklet_hi_action_1+1
    teval $tmp_1=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == tasklet_hi_action && $cpu_id==1)
  commands
    teval $tasklet_hi_action_t_1=$tasklet_hi_action_t_1+$clock-$tmp_1
  end

#net_tx_action
tvariable $net_tx_action_1
tvariable $net_tx_action_t_1
trace softirq.c:238
  condition $bpnum (h->action == net_tx_action && $cpu_id==1)
  commands
    teval $net_tx_action_1=$net_tx_action_1+1
    teval $tmp_1=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == net_tx_action && $cpu_id==1)
  commands
    teval $net_tx_action_t_1=$net_tx_action_t_1+$clock-$tmp_1
  end

#net_rx_action
tvariable $net_rx_action_1
tvariable $net_rx_action_t_1
trace softirq.c:238
  condition $bpnum (h->action == net_rx_action && $cpu_id==1)
  commands
    teval $net_rx_action_1=$net_rx_action_1+1
    teval $tmp_1=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == net_rx_action && $cpu_id==1)
  commands
    teval $net_rx_action_t_1=$net_rx_action_t_1+$clock-$tmp_1
  end

#run_rebalance_domains
tvariable $run_rebalance_domains_1
tvariable $run_rebalance_domains_t_1
trace softirq.c:238
  condition $bpnum (h->action == run_rebalance_domains && $cpu_id==1)
  commands
    teval $run_rebalance_domains_1=$run_rebalance_domains_1+1
    teval $tmp_1=$clock
  end
trace softirq.c:239
  condition $bpnum (h->action == run_rebalance_domains && $cpu_id==1)
  commands
    teval $run_rebalance_domains_t_1=$run_rebalance_domains_t_1+$clock-$tmp_1
  end

define softirq1
	printf "CPU1 softirq: %u times, %u ns, %u ns per time, %.11f of total exec clock\n", $times1=$run_timer_softirq_1+$run_hrtimer_softirq_1+$blk_iopoll_softirq_1+$blk_done_softirq_1+$tasklet_action_1+$tasklet_hi_action_1+$net_tx_action_1+$net_rx_action_1+$run_rebalance_domains_1,$clock1=$run_timer_softirq_t_1+$run_hrtimer_softirq_t_1+$blk_iopoll_softirq_t_1+$blk_done_softirq_t_1+$tasklet_action_t_1+$tasklet_hi_action_t_1+$net_tx_action_t_1+$net_rx_action_t_1+$run_rebalance_domains_t_1, $clock1/$times1, (float)$clock1/(float)($clock-$begin)

	output_entry 1 "run_timer_softirq" $run_timer_softirq_1 $run_timer_softirq_t_1 $times1 $clock1
	output_entry 1 "run_hrtimer_softirq" $run_hrtimer_softirq_1 $run_hrtimer_softirq_t_1 $times1 $clock1
	output_entry 1 "blk_iopoll_softirq" $blk_iopoll_softirq_1 $blk_iopoll_softirq_t_1 $times1 $clock1
	output_entry 1 "blk_done_softirq" $blk_done_softirq_1 $blk_done_softirq_t_1 $times1 $clock1
	output_entry 1 "tasklet_action" $tasklet_action_1 $tasklet_action_t_1 $times1 $clock1
	output_entry 1 "tasklet_hi_action" $tasklet_hi_action_1 $tasklet_hi_action_t_1 $times1 $clock1
	output_entry 1 "net_tx_action" $net_tx_action_1 $net_tx_action_t_1 $times1 $clock1
	output_entry 1 "net_rx_action" $net_rx_action_1 $net_rx_action_t_1 $times1 $clock1
	output_entry 1 "run_rebalance_domains" $run_rebalance_domains_1 $run_rebalance_domains_t_1 $times1 $clock1
end

p $begin=$clock
tstart

define softirq
	softirq0
	printf "\n"
	softirq1
end


