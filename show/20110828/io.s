set circular-trace-buffer on
define dpe
  if ($argc < 2)
    printf "Usage: dpe pe_type pe_config [enable]\n"
  end
  if ($argc >= 2)
    set $tmp=0
    while $tmp<$cpu_number
      eval "tvariable $pc_pe_type_%d%d_%d=%d",$arg0, $arg1, $tmp, $arg0
      eval "tvariable $pc_pe_config_%d%d_%d=%d",$arg0, $arg1, $tmp, $arg1
      eval "tvariable $pc_pe_val_%d%d_%d=0",$arg0, $arg1, $tmp
      if ($argc >= 3)
        eval "tvariable $pc_pe_en_%d%d_%d=%d",$arg0, $arg1, $tmp, $arg2
      end
      set $tmp=$tmp+1
    end
  end
end
dpe 0 0 0
trace mpage_readpages
  commands
    teval $pc_pe_en = 1
  end
list mpage_readpages
trace 400
  commands
    teval $pc_pe_en = 0
    collect $pc_pe_val_00_0
    collect $cpu_id
    teval $pc_pe_val_00_0 = 0
  end
