> Saved by the lead from the hand-back (seat 5f8644f3, 2026-11-23). The text below is the seat's report verbatim.

# PRIOR-ART-ATLAS: headline gate for CHANNEL-ATLAS (gate-1, 2026-11-23)

(Lead's faithful condensed transcription of seat gate-1's hand-back: all numbers, verdicts, quotes and locators kept; prose shortened; transcript-read failed. Scratch: atlas/seats/gate-1/ - QUERIES.log (searchcheck: search floor OK), numbers.out (every computed number), src/, rendered page PNGs.)

Coverage: arXiv web search through 2026-11-19 (newest listing seen 2611.26436); Zenodo as of 2026-11-23 (newest relevant: our trapdoor release 2026-11-22); Capacity Atlas GitHub at its last commit 2026-11-06. Units: bits per channel use (Han-Marcus asymptotics in nats, as the paper states). Labels: OPENED = text or rendered page read; ABSTRACT = abstract/listing only; SNIPPET = search-engine text only. "(computed)" = seat's own POST HOC, uncertified evaluation of a published formula, all in numbers.out.

## In plain words
- No computer-certified (interval / exact-rounding) capacity bounds found for any of DEC, RLL-BEC, RLL-BSC; no published window narrower than those below.
- Proven two-sided analytic bounds already exist for all three, so "certified" alone is weak; the atlas is new only where it narrows a window or proves a floor that today exists only as simulation.
- DEC p = 0.5: proven floor 0.673611 (first-order Markov, 1911.02113 Thm 10); analytic ceiling 0.676083 (2303.18008 Thm 14, after correcting two apparent misprints); feedback capacity 0.678509.
- RLL-BEC eps = 0.5: exact first-order Markov floor 0.390811; ceiling (1/4) log2 3 = 0.396241 (Thangaraj Thm 3(1)); feedback capacity 0.405685.
- RLL-BSC p = 0.05: tight ceiling 0.520392 (2303.18008 Thm 9; duality curve about 0.525 in figure); only proven floor is weak, 0.492962 (Rameshwar-Kashyap); tight floor about 0.5198 is simulation only. Clearest open gap.
- Family: certified deletion-channel numerics by three groups in 2026 (2609.19412, 2609.24908, Zenodo 10.5281/zenodo.21780666) plus our trapdoor release. A Lean-formalised registry "Capacity Atlas" exists (Ortega, Zenodo 10.5281/zenodo.23573821, Oct 2026) - name collision; its entries for this family are thin (trapdoor without feedback "open" 0.572 <= C <= 0.5765, our window absent; no DEC, no constrained BSC, no constrained BEC without feedback).
[line withheld in this release: a remark on a number printed in third-party work, kept private until the original source can be read; see PATCHES.md]

## Step 0: own files (selfcite)
Four runs (DEC 22 hits/13 files; RLL-BEC 1141/75; RLL-BSC 47/20; certified family 68/25). Hits: lab notes (frontier-siblings, bigger-idea, MENU, PRIOR-ART-ISING, TRAPDOOR PRIOR-ART, trapdoor release), downloaded papers (all opened in this report). No lab paper claims a result on these three channels.
Correction to own notes: frontier-siblings DEC first-order rate 0.67350 came from a coarse grid; at optimal flip probability 0.5619 the same script brackets [0.6736106030, 0.6736106956] at n = 11, matching published closed form 0.673610662.
Suggested selfcite aliases: dicode erasure channel | dicode erasure | DEC | 1-D erasure channel | generalized erasure channel | erasure ISI channel; (1,inf)-RLL input-constrained BEC | input-constrained erasure channel | no-consecutive-ones erasure | no-repeated-ones BEC | (1,inf)-RIC BEC | constrained BEC; (1,inf)-RLL input-constrained BSC | noisy constrained capacity | input-constrained BSC | (1,inf)-RIC BSC | no-repeated-ones BIBO | input-restricted BSC; Capacity Atlas | capacity registry.

## 1. DEC(p), feedforward
Definition (OPENED 1911.02113 p.8): y_t = x_t - x_{t-1} w.p. 1-eps, '?' w.p. eps; state = previous input.
| Bound | Source | Value p = 0.5 | Rigour | Label |
|---|---|---|---|---|
| LB first-order Markov | 1911.02113 Thm 10 (Pfister thesis Ch. 4) | 0.673610662 (computed); lab sandwich [0.6736106030, 0.6736106956] n = 11 at flip 0.561924 | exact closed form | OPENED p.8 |
| LB iid uniform (SIR) | Pfister-Siegel JSAC 26(2) 2008 Sec. II: 1 - 2eps^2/(1+eps) | 2/3 (Fig. 3 caption "pDEC eps=1/2 SIR=2/3") | exact | OPENED p.322-323 |
| UB dual Q-graph | 1911.02113 Thm 9: 1 + eps log2((1-p)/p), p^eps = 2 pbar; "coincides with the DEC feedback capacity" | 0.6785093184 (computed) | analytic | OPENED p.8 |
| UB two-step delayed feedback | 2303.18008 Thm 14 | as printed: max diverges as a->0, min 0.663078 below achievable; read as min with sqrt(1+4a^2) (as gamma2 eq. 34): 0.6760832282 at a ~ 0.322, matches Fig. 7 (~0.676) | analytic, printed statement inconsistent; correction POST HOC | OPENED p.9, p.12 eq. (31)-(34) |
| Feedback capacity | 2303.18008 Thm 13 = 1604.01878 Thm 5 | 0.6785093184; 0.1: 0.9822638979; 0.3: 0.8670172967; 0.7: 0.4371915688; 0.9: 0.15448843 | exact | OPENED |
Grid (computed) eps: Thm 10 LB / Thm 9 UB: 0.1 0.9818961288 / 0.9822638979; 0.3 0.8638147664 / 0.8670172967; 0.7 0.4335971586 / 0.4371915688; 0.9 0.1537743546 / 0.15448843.
Published proven window p = 0.5: [0.673611, 0.678509] (width 0.0049); with Thm 14 correction [0.673611, 0.676083] (width 0.0025).
Open sentences (OPENED): 2303.18008 Sec. VII-B "... in the absence of feedback the capacity is still unknown."; 1911.02113 p.8 "in the absence of feedback, the problem of determining the capacity is still open."

## 2. (1,inf)-RLL BEC(eps), feedforward
| Bound | Source | Value eps = 0.5 | Rigour | Label |
|---|---|---|---|---|
| LB first-order Markov | Li-Han ISIT 2014 / 1605.02175 Sec. 4.2; exact series (1-eps) sum_k (1-eps) eps^{k-1} H(X_t|X_{t-k}) | 0.3908109004 (computed); lab sandwich same at n = 11 | exact series | OPENED (1605.02175) |
| LB analytic DP | 2001.03423 Thm V.3: 0.6942(1-eps) | 0.3471209568 | analytic, weak | OPENED |
| LB numerical | Rameshwar-Kashyap NCC 2021 | no numbers seen | stochastic | SNIPPET |
| UB dual mu = 1 | Thangaraj 1609.00189 Thm 3(1): (1-eps)^2 log2(1/beta*) + eps(1-eps) log2(2-beta*), beta^{2(1-eps)} = 1-beta | 0.39624062518 = (1/4) log2 3 exactly (beta* = 1/2) | analytic | OPENED p.5 |
| UB dual mu = 2 | Thangaraj Thm 3(2) | not reproduced (seat's solve 0.42777 > feedback capacity: wrong root or misprint); do not use | analytic | OPENED p.5-6 |
| Feedback capacity | 1503.03359 Thm 1: max_{0<=p<=1/2} Hb(p)/(p + 1/(1-eps)) | 0.405685231376; at 0.71: 0.2546968219 (paper "~0.2547") | exact | OPENED |
Thangaraj 3(1) grid: 0.1 0.639445738737; 0.2 0.582516635826; 0.3 0.523214017279; 0.4 0.461244216201; 0.5 0.39624062518; 0.6 0.327731996369; 0.7 0.255087863425; 0.71 0.247564740095; 0.8 0.177413562144; 0.9 0.0933076032164.
Markov-1 grid: 0.1 0.6380154673; 0.2 0.5797776624; 0.3 0.5193313317; 0.4 0.4564396333; 0.5 0.3908109004; 0.6 0.3220734216; 0.7 0.2497292534; 0.71 0.2422715131; 0.8 0.1730567446; 0.9 0.0908480127.
Feedback grid: 0.1 0.642723981979; 0.3 0.531120793525; 0.5 0.405685231376; 0.7 0.262423984283; 0.9 0.095313045283.
Proven window eps = 0.5: [0.390811, 0.396241], width 0.0054.
[line withheld in this release: a remark on a number printed in third-party work, kept private until the original source can be read; see PATCHES.md]
Open sentences (OPENED): 1503.03359 p.3 "... without feedback, a problem that is still open."; 1609.00189 abstract "some of the simplest upper bounds for an open capacity problem".

## 3. (1,inf)-RLL BSC(p), feedforward
| Bound | Source | Value p = 0.05 | Rigour | Label |
|---|---|---|---|---|
| LB analytic DP | 2001.03423 Thm V.1: max_a [hb(ap + abar pbar) - hb(p)]/(a d + 1), d = 1 | 0.4929617562 | analytic, weak | OPENED p.4 |
| LB simulation | Arnold-Loeliger-Vontobel-Kavcic-Zeng IEEE TIT 52(8) 2006 type, in 2303.18008 Fig. 6 / 1609.00189 Fig. 5 | about 0.5198 (Fig. 6 inset read) | Monte-Carlo | OPENED (figure) |
| UB two-step delayed feedback | 2303.18008 Thm 9 | 0.5203915067 (SLSQP, 300 starts); matches Fig. 6 black line ~0.5205 | analytic; any feasible point valid | OPENED p.6 |
| UB dual (Thangaraj) | 1609.00189 Thm 6 | Fig. 6 dashed red ~0.5252; printed formula evaluates to 0.4106 and negative from p = 0.2 (impossible): misprint or wrong root, UNRESOLVED | analytic | OPENED p.7 |
| Asymptotics | Han-Marcus 0803.3360; Jacquet-Seroussi-Szpankowski ISIT 2007 / IEEE TIT 56(11) 2010; Han-Marcus 1001.1214 | p->0, p->1/2 only | rigorous asymptotics (nats) | OPENED abstract+intro (0803.3360); others ABSTRACT/SNIPPET |
| Feedback capacity | Sabag-Permuter-Kashyap IEEE TIT 64(7) 2018, 1701.06174 Cor. 1 | 0.5576776383 (both forms agree) | exact | OPENED p.6 |
Grid p: feedback / Thm 9 UB / RK floor: 0.01 0.6614064409 / 0.6465573441 / 0.6370059168; 0.05 0.5576776383 / 0.5203915067 / 0.4929617562; 0.1 0.4443883399 / 0.4028902837 / 0.366045608; 0.2 0.2542627354 / 0.2282856814 / 0.1912373343; 0.3 0.1143681024 / 0.1059011559 / 0.08153756389; 0.4 0.0287894394 / 0.0280176011 / 0.0199403377.
Open sentences (OPENED): 2303.18008 Sec. VII-A "while the feedforwad capacity is still open, the feedback capacity was established in [19]"; 1701.06174 p.6 "the non-feedback setting, which is still an open problem."
Gap at p = 0.05: proven LB 0.4930 vs UB 0.5204, simulation ~0.5198; a certified tight floor closes most of 0.027.

## 4. Family claim
| Source | What it certifies | Label |
|---|---|---|
| Papailiopoulos, arXiv 2609.19412 (2026-09-16) "Binary Deletion Channel Capacity to Within One Hundredth of a Bit" | computer-assisted two-sided deletion bounds | ABSTRACT (OPENED by earlier lab seat, PRIOR-ART-SQUEEZE) |
| Khodaiemehr-Feng-Duman, arXiv 2609.24908 (2026-09-21) | deletion LBs via learned run-length inputs; only abstract hit for "interval arithmetic" capacity channel | ABSTRACT |
| Hungjen Chen, Zenodo 10.5281/zenodo.21780666 (2026-08-03) "A Certified Multi-Run Capacity Lower Bound for the Binary Deletion Channel at d = 1/2" | "proves C(1/2) > 0.11032415"; "certified computation" | OPENED (PDF p.1) |
| arXiv 2609.24889 "Orbit Reduction and Learned Run Distributions for Finite-Blocklength Binary Deletion Channels" | block capacity with numerical optimality certificate up to N = 16 | ABSTRACT |
| Ortega, "Capacity Atlas v0.3.0", Zenodo 10.5281/zenodo.23573821 (2026-10-22); GitHub TomasOrtega/CapacityAtlas (last commit 2026-11-06) | "65 capacity problems ... 62 entries with formally stated claims; 19 entries with formally proved capacity claims" (Lean 4); trapdoor-without-feedback open 0.572-0.5765; constrained-bec-with-feedback solved; no DEC, constrained BSC, constrained BEC without feedback, Ising | OPENED (record, repo tree, 2 YAML) |
| our trapdoor release, Zenodo 10.5281/zenodo.24443962 | certified two-sided trapdoor window | own |
| arXiv 1402.2733 (entropy rate of HMM with unambiguous symbols) | method neighbour for erasure outputs | ABSTRACT |
Not certified memory-channel work: 2608.13170, 2609.22389 (ABSTRACT).

## Verdict table
| Item | Verdict | Best source | Label |
|---|---|---|---|
| DEC (a) proven two-sided | PARTIAL (analytic theorems; no certificate) | 1911.02113 Thm 9-10; 2303.18008 Thm 14 | OPENED |
| DEC (b) numbers p = 0.5 | TAKEN (theirs) | 2303.18008 Fig. 7 + Thm 14 | OPENED |
| DEC (c) feedback capacity | TAKEN | 2303.18008 Thm 13 (= 1604.01878 Thm 5) | OPENED |
| DEC certified window narrower than [0.673611, 0.676083] | OPEN (search floor) | none | QUERIES.log |
| RLL-BEC (a) | PARTIAL | 1609.00189 Thm 3 | OPENED |
| RLL-BEC (b) | TAKEN [clause withheld; see PATCHES.md] | 1503.03359 p.3 / TIT 62(1) | OPENED |
| RLL-BEC (c) | TAKEN | 1503.03359 Thm 1 | OPENED |
| RLL-BEC certified window narrower than [0.390811, 0.396241] | OPEN (search floor) | none | QUERIES.log |
| RLL-BSC (a) | PARTIAL (tight UB; weak proven LB) | 2303.18008 Thm 9; 2001.03423 Thm V.1 | OPENED |
| RLL-BSC certified floor near simulated rate (> 0.4930 at p = 0.05) | OPEN (search floor) | closest 2001.03423 | OPENED |
| RLL-BSC (c) | TAKEN | 1701.06174 Cor. 1 | OPENED |
| Family: certified bounds for channels with memory | PARTIAL | Zenodo 21780666; 2609.19412; Capacity Atlas 23573821 | OPENED/ABSTRACT |
| Family: one certified table for Ising, DEC, RLL-BEC, RLL-BSC | OPEN (search floor) | nearest Capacity Atlas (no such entries) | OPENED |

Open gap: nothing found gives interval-certified feedforward windows for DEC, RLL-BEC or RLL-BSC narrower than the published analytic windows (DEC [0.673611, 0.676083] p = 0.5; RLL-BEC [0.390811, 0.396241] eps = 0.5; RLL-BSC [0.492962 proven, 0.520392] p = 0.05), nor any proven RLL-BSC floor near the simulated rate.

## Neighbours and methods to borrow
- BGU/HUJI (Permuter, Huleihel, Sabag): Q-graph duals, delayed-feedback bounds; higher-order Q-graph for DEC/RLL-BSC one step away (2303.18008: "evaluating the upper bound ... with a 3-order Markov Q-graph provides an even tighter upper bound").
- IISc (Kashyap, Rameshwar): input-constrained LBs; Rameshwar thesis etd.iisc.ac.in/handle/2005/6293 not opened (HTTP 502).
- Capacity Atlas (Ortega): registry; our trapdoor certificate absent from its trapdoor entry (citation channel, not a threat).
- Borrow: (a) erasure-type Markov-k rates are exact series; certified floor needs only a tail bound (r^400 = 3.44e-78 at DEC optimum eps = 0.5). (b) Thangaraj Thm 3(1), 2303.18008 Thm 9 closed forms/feasible points: free ceiling positive controls by interval evaluation. (c) Pfister-Siegel SIR 1 - 2eps^2/(1+eps): exact iid control.

## Loose ends (seat)
- 2303.18008 Thm 14 as printed not evaluable; corrected 0.6760832 POST HOC; journal version (BGU author copy IT_Capacity_of_Finite-State_Channels_With_Delayed_Feedback.pdf) not opened.
- Thangaraj Thm 3(2), Thm 6 do not reproduce plotted curves; UNRESOLVED; journal IEEE TIT 63(11) 7052-7065 2017.
[line withheld in this release: a remark on a number printed in third-party work, kept private until the original source can be read; see PATCHES.md]
- Pfister thesis Ch. 4 not found online; Thm 10 via 1911.02113, numerically cross-checked.
- Rameshwar-Kashyap NCC 2021 SNIPPET only. Peled et al. 2019 / 1712.02690 out of scope.
- Citation trails not walked (OpenAlex budget exhausted, Semantic Scholar 429, arXiv export API 429; arXiv coverage via web search). INSPIRE not used (no cs.IT).
- arXiv titles verified via abs-page citation_title: 2609.19412, 2609.24908, 2303.18008, 1609.00189, 1701.06174, 1503.03359, 1605.02175, 2001.03423, 1911.02113, 0803.3360, 1601.06453, 2101.08638, 1604.01878, 2608.13170, 2609.22389, 1107.3253.
- Figure reads +-0.0005.
