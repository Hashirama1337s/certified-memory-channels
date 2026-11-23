import json
json.dump(dict(kind='rllbec', noise='0', m=1, theta={'0': 0.3819660112501051}), open('ctl_src_rll_noiseless.json', 'w'))
json.dump(dict(kind='dec', noise='1/2', m=1, theta={'0': 0.5, '1': 0.5}), open('ctl_src_dec_iid.json', 'w'))
json.dump(dict(kind='decrl', noise='1/2', R=1, g={'1': 0.5}), open('ctl_src_decrl_iid.json', 'w'))
