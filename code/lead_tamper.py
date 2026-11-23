"""lead_tamper.py IN.json OUT.json : content null for BAR-ATLAS1a K2.
Every context row of T: move 1% of the largest entry's mass to the second-largest entry (row sum kept exactly, all
entries stay >= 1), rho and h kept. Asserts the certificate actually changed in every row with a largest entry > 100
(the ATLAS1 VOID: a tamper on an unreachable row with entry 1/T_den rounded back to itself and changed nothing)."""
import json, sys
C = json.load(open(sys.argv[1]))
nY = int(C['nY']); Tn = [int(v) for v in C['T_num']]; Tden = int(C['T_den'])
rows = len(Tn) // nY; changed = 0
for q in range(rows):
    r = Tn[q * nY:(q + 1) * nY]
    assert sum(r) == Tden
    order = sorted(range(nY), key=lambda i: -r[i])
    a, b = order[0], order[1]
    d = r[a] // 100
    if d >= 1:
        r[a] -= d; r[b] += d; changed += 1
    assert sum(r) == Tden and min(r) >= 1
    Tn[q * nY:(q + 1) * nY] = r
assert changed == rows, f'only {changed} of {rows} rows changed'
C['T_num'] = [str(v) for v in Tn]
C.setdefault('meta', {})['lead_tamper'] = 'every row: 1% of largest entry moved to second largest; rho, h kept'
json.dump(C, open(sys.argv[2], 'w'))
print(f'tampered {changed}/{rows} rows -> {sys.argv[2]}')
