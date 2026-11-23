#!/bin/bash
B=atlas/seats/blind-1
O=atlas/run_blindcheck
MC="py -3.11 memcap.py 8 py -3.11"
cd $B
sha256sum check_ceil.py check_floor.py cert_*K12.json cert_*K14.json cert_*K9.json theta_rllbec_dualK8.json theta_rllbsc_dualK8.json g_decrl_R10.json > $O/sha.txt
r() { n=$1; shift; s=$(date +%s); $MC "$@" > $O/$n.log 2>&1; echo "exit $? secs $(( $(date +%s)-s ))" >> $O/$n.log; }
r floorA check_floor.py theta_rllbec_dualK8.json 13 0.393198484464437
r floorB check_floor.py theta_rllbsc_dualK8.json 14 0.519684268667857
r floorC check_floor.py g_decrl_R10.json 18 0.674950676626481
r ceilA check_ceil.py rllbec 1/2 12 qtab_rllbec_1-2_K12.npy V_rllbec_1-2_K12.npy 0.393198484526574
r ceilC check_ceil.py dec 1/2 9 qtab_dec_1-2_K9.npy V_dec_1-2_K9.npy 0.674968222857599
r ceilB check_ceil.py rllbsc 1/20 14 qtab_rllbsc_1-20_K14.npy V_rllbsc_1-20_K14.npy 0.519684268667911
r ceilB_neg check_ceil.py rllbsc 1/20 14 qtab_rllbsc_1-20_K14.npy V_rllbsc_1-20_K14.npy 0.519684268667900
echo DONE > $O/DONE
