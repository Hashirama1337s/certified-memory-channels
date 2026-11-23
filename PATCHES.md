# PATCHES

Moki & Julio (AI-assisted) · version 1.0

## In plain words

Most files in this package are byte-for-byte copies of the files our computations produced. Some copies had to be changed
before release: programs that named folders on the machine where they ran, text files that named those folders, three lines
that named the machine's home folder or the person running it, and a few lines that comment on numbers printed in other
people's work which we keep private until we can read the original source. Every change is listed here with the sha256 of
the original, so the original can be identified (for sealed files, by the hash recorded when the file was sealed). Sources
stay untouched in the working folder: everything was copied, nothing was moved or deleted.

## Code

Byte-identical to their sources: `code/channel_spec.py`, `code/atlas_verify_ub.py`, `code/atlas_ub.py`, `code/lead_tamper.py`,
and the floor kernel `code/cert_backward2.py`, `code/trapcommon.py` (unchanged from the certified-trapdoor-channel release),
and every file in `second-implementation/code/` except `assemble.py`.

| shipped file | original sha256 | change |
|---|---|---|
| `code/atlas_lb.py` | `bd74dd6fbaca5749b181a17b90e16bc78eaeab22786e950fa6fe03b7f0f25de7` | P1: the kernel folder (a working path) replaced by the program's own folder, in the import path and in `KERNEL_PATH` (lines 21, 27) |
| `code/atlas_rows.py` | `723b43bfe915710a9ecf5d118dc0fe92989f40e524417b0404a9d3760dafa70e` | P2: the same import-path change (line 24) |
| `code/atlas_primal4.py` | `8c24a4e73dc29c9ad80b691d3339a1cbe24a54072ed1f96ec100e9f376c9aebd` | P3: `ENG` (the engine folder, a working path) replaced by the program's own folder (line 23) |
| `code/controls.py` | `9cda3b97e39fa5967619279809001a7fbe6e5e6115afe1a938fa83b476cab5b8` | P4: the Ising package is not shipped in v1, so its import is optional and section (a) (Ising controls) prints `[SKIP]` when it is absent; the Ising folder path and the input-law folder now point inside the package (`code/ising`, `floors/laws`). No other control changed; the patched file was run in a fresh copy: 42 PASS, `CONTROLS: ALL PASS` |
| `second-implementation/code/assemble.py` | `6e25bebb4cfc03c8477d87e4f9d4cb9ab3e66f5bb9b30fc4ea947392d7148998` | P5: the lab's memory-cap wrapper (a working path) removed from the command list (line 11) |

## Text copies

Rules: (a) the project's working-folder prefix removed, leaving a path relative to the project folder; (b) the folder of the
trapdoor release kernel shortened to `trapdoor-release/code/floor/`; (c) the lab memory-cap wrapper path shortened to
`memcap.py`; (d) the lab tools folder shortened to `lab-tools/`; (e) the first name of the person running the lab replaced by
"the owner"; (f) a home-folder Python path shortened to `<python>`; (g) a home-folder tool path and a product name replaced
by neutral wording; (h) a line commenting on a number printed in third-party work withheld (replaced by a visible
"[line withheld ...]" or "[clause withheld ...]" note) until the original source can be read. No line was added or removed, so
line numbers match the originals. Sealed files in `bars/` differ from the sealed versions only by these substitutions; the
listed original sha256 is the sealed hash.

| shipped file | original sha256 | lines changed | rules |
|---|---|---|---|
| `bars/AMENDMENT-ATLAS1a.md` | `29d1a8bbf669d4d8961a18d43dc9f2a5065af00a60d4e761de8116e9bf954113` | 16, 22 | (a) |
| `bars/BAR-ATLAS1.md` | `2f56539e0dd39d37b732a5870f3d95b385d3a59089b7bb55604b132868dbd3e4` | 36, 42 | (a), (b) |
| `bars/BAR-ATLAS2.md` | `fcd56dd9194ebd387e7f89ef8ca63e42b0c1945b5de92c9a154314e4132cbb2c` | 37, 43 | (a) |
| `bars/BAR-ATLAS3.md` | `c8ad196cc55e8605bda8ebadaba6f1621ffdbcb979beb4c948a66c2e9c5ee857` | 35, 41 | (a) |
| `bars/BAR-ATLAS4.md` | `bf31813af7c376cf0ed81a611e662716377ee14fb753164a4e62c4cddafab5c7` | 31, 37 | (a) |
| `bars/BAR-ATLAS5.md` | `36a7852edfa7e7c0c2d73ee40ced3424b1366fbf9e83faab7b5db4c2d2e6adb9` | 26, 32 | (a) |
| `bars/BAR-ATLAS6.md` | `f7ec935761b295afb6d872248d36b0ceaea8950ffb343b1ddbe25ab197bcde3e` | 26, 32 | (a) |
| `transcripts/run_atlas1/K1_controls.log` | `467c6f35a751321242148cee87b686ccba040e05b6585c94f1076d8809b8b45d` | 5 | (a) |
| `transcripts/run_atlas1/K2_build_dec.log` | `6bd1614497c401f57a6fab964d3baad5f7e00cad21db98c46075f23e8ca6bef5` | 1, 5 | (a) |
| `transcripts/run_atlas1/K2_build_rllbec.log` | `7a49c38b4642338918e7a1cb354b14364120973ced7ef1bd55051e300635734d` | 1, 5 | (a) |
| `transcripts/run_atlas1/K2_build_rllbsc.log` | `4ad1c92264ece701f410556651bdb2310182fcb29d360a54fffeb4c8edf6538a` | 3 | (a) |
| `transcripts/run_atlas1/K2_verify_dec.log` | `84458271793d6a808a6aef5b131261a4cf85fdc14ff3b5684d4f3a048ba0f6f0` | 2 | (a) |
| `transcripts/run_atlas1/K2_verify_rllbec.log` | `6302efc54bc5be9d903ece49381f3888482bd96aabf1c3f79e38867d6947a9bf` | 2 | (a) |
| `transcripts/run_atlas1/K2_verify_rllbsc.log` | `584e5c74549edbd865d8af9353ead928e029dea27342ec7b34e7602d932ea554` | 2 | (a) |
| `transcripts/run_atlas1/ub_dec.log` | `966be4224e8f9410eaf3775c30d1118d19e0d5463b9920add82a5cb7c64b920d` | 1 | (a) |
| `transcripts/run_atlas1/ub_rllbec.log` | `f3a3ea2ebb591c47dbd7fdc55336275e48e9f8c0253e6dfe4257824e7ec434fe` | 1 | (a) |
| `transcripts/run_atlas1/ub_rllbsc05.log` | `8a3ba6dcb7d4d7fbdccd259dbd2d407ac440cbd4c0c7d515f1b83d6f1e682e2b` | 1 | (a) |
| `transcripts/run_atlas1/ub_rllbsc11.log` | `aadbdd5b59cf8218e2f9ad493a7e9ffb76d4aa9fbb028347d03ac3e45f33213b` | 2 | (a) |
| `transcripts/run_atlas1a/clean_cert_dec_1-2_k8_D40.log` | `0933145dc1e4affe4d400c05642af767d1b310f24773017077879706510b8986` | 2 | (a) |
| `transcripts/run_atlas1a/clean_cert_rllbec_1-2_k8_D40.log` | `6afb1e0ffc53b2d2651fabb1be2d0af0dde3ba74a55dad0ae777a3caae744f60` | 2 | (a) |
| `transcripts/run_atlas1a/clean_cert_rllbsc_1-20_k8_D40.log` | `df1ecf6de3995c5d2cbca13548ce4232abde338548ea73bb78e03a5862e67248` | 2 | (a) |
| `transcripts/run_atlas1a/clean_cert_rllbsc_11-100_k10_D40.log` | `302afa6310c37f698201ee6d6713186c61885a2a595e8739e941a3d0b57e7b33` | 2 | (a) |
| `transcripts/run_atlas2/K1_controls.log` | `7b4c77330da26a18cbb443f15efeaf677b01b6decf751a0c52455b26ef708d7c` | 13 | (a) |
| `transcripts/run_atlas2/K2_clean_cert_dec_1-10_k8_D40.log` | `81798fa1768b61f2d8b3463a1b4a268ccb9f0a29b9774bde53dde196e7762560` | 2 | (a) |
| `transcripts/run_atlas2/K2_clean_cert_rllbec_9-10_k7_D40.log` | `c0d658551ea1b8654480461484e7c6a5a807f2832771c40322ffd599ee2f704b` | 2 | (a) |
| `transcripts/run_atlas2/K2_tamp_cert_dec_1-10_k8_D40.log` | `9c7c1c0da6b74b77fceeed0e243b3722f75aefe0fc88f00fab143973ee78298c` | 2 | (a) |
| `transcripts/run_atlas2/K2_tamp_cert_rllbec_9-10_k7_D40.log` | `ff7f269ae34f22fba5f2eb5f2918b3f17f348b2ea328ee23ef98f44a92c968ef` | 2 | (a) |
| `transcripts/run_atlas2/K2_tbuild_cert_dec_1-10_k8_D40.log` | `b50c5d5ed2f831b49a0a549d807b8ed8a2511cccd868262c3dc4d0728ca7f77e` | 1 | (a) |
| `transcripts/run_atlas2/K2_tbuild_cert_rllbec_9-10_k7_D40.log` | `bdfaf770679680d582fcd87d4dcb027fed99fd99e45c878216bf9eb8d99de989` | 1 | (a) |
| `transcripts/run_atlas2/ub_dec_1-10.log` | `d502183b66b5b95ed4b0a868150e1351e0d5d852826283c0867de75ee55c42ec` | 9 | (a) |
| `transcripts/run_atlas2/ub_dec_1-4.log` | `e4a721ca13436d9d5e57314620cfb3d5d49f1c9f587e6e6010986e02fa78e7f8` | 9 | (a) |
| `transcripts/run_atlas2/ub_dec_3-4.log` | `af80a9b9870d3657107987b594dd2f5b5a1736713390761846156f9c7b90f38e` | 9 | (a) |
| `transcripts/run_atlas2/ub_dec_9-10.log` | `18b788488e74654d6a6ca26b6ba07aee0ea00e4ea6f3ed5341e098b6c0e163c0` | 9 | (a) |
| `transcripts/run_atlas2/ub_rllbec_1-10.log` | `f72072f4a5cec9b0a39322299a7a235646dfa01e2f751dbf6ee709d5876d211f` | 9 | (a) |
| `transcripts/run_atlas2/ub_rllbec_1-4.log` | `11eef85437039b0560534408f987debe4558440125e26129c9c0b783c804c524` | 9 | (a) |
| `transcripts/run_atlas2/ub_rllbec_3-4.log` | `9eeb5182fa6ceed72adf6e3f7708ad0220413e1233e2596240fdc1d6dfa929d8` | 9 | (a) |
| `transcripts/run_atlas2/ub_rllbec_9-10.log` | `5e3d7266ecb19a06b65aedc2d4f07159afc4928f26760470f7b66c1c30218b23` | 9 | (a) |
| `transcripts/run_atlas2/ub_rllbsc_1-100.log` | `c3c68651cf9f0546d0fb1d8bc575cf0767d6702f5e71bb52d4caa24d1a956b37` | 10 | (a) |
| `transcripts/run_atlas2/ub_rllbsc_1-5.log` | `38388b692bd24c60750203ba9202b1fe13ed9598ffc9590ef32d252dbd8d83eb` | 15 | (a) |
| `transcripts/run_atlas2/ub_rllbsc_3-10.log` | `603ef24d7d8352efe921ecb78aec837889f474206727772dd9ce0280b4f3ebcc` | 9 | (a) |
| `transcripts/run_atlas3/K1_controls.log` | `b76e7e50c2552619ad5e011f4553ab832983571e65cc212b67d410d259b44720` | 1, 2, 3, 4, 9 | (a) |
| `transcripts/run_atlas3/K2_tamp_dec_1-10_k10.log` | `030d342f43f386de1f93f45908876efd8bd3545a47f466f27670fa1aa8ef5ad3` | 2 | (a) |
| `transcripts/run_atlas3/K2_tamp_rllbsc_1-5_k12.log` | `1fa088f5903045394763c7970b4f592b4a06d500ff5ab0777033b9f0adeda922` | 2 | (a) |
| `transcripts/run_atlas3/K2_tbuild_dec_1-10_k10.log` | `b6b6439f2c8cd06dc2e3f503fa1e6ffb8d7adb39918c0bd15493e06cd1967a55` | 1 | (a) |
| `transcripts/run_atlas3/K2_tbuild_rllbsc_1-5_k12.log` | `ad1aa461cee991861e7e9810d9750be9ce063e76e5e815edb5b0257893860dfd` | 1 | (a) |
| `transcripts/run_atlas3/engine_sha256.txt` | `988b132d330cdc08f8c2e8a34a04bc6f75c35484dbf934bbde657ddb9b86b1b6` | 1, 2, 3, 4 | (a) |
| `transcripts/run_atlas3/ub_dec_1-10_k10.log` | `32d6fa328c2517d19ccc9c0188314b11974d0864f262637e6e238459f30d85ae` | 1, 2, 3, 4, 17 | (a) |
| `transcripts/run_atlas3/ub_dec_1-2_k10.log` | `936186a279a88a11059e9fc7112f3d7ff20c95d776e3846d37ea74bcfc281b3a` | 1, 2, 3, 4, 24 | (a) |
| `transcripts/run_atlas3/ub_dec_1-4_k10.log` | `324c1879b172e51b809fd531e2f5b3b63ad5e3234f7628d805d51c14a074325e` | 1, 2, 3, 4, 20 | (a) |
| `transcripts/run_atlas3/ub_dec_3-4_k10.log` | `31a3c7ecf640ad12b00127bb155a3b7d43e418661f452b022dd9a7c22301dd22` | 1, 2, 3, 4, 66 | (a) |
| `transcripts/run_atlas3/ub_dec_9-10_k10.log` | `b891e6f06d3a73772efda1b2cd4527356f7ba2f324d2dd2d2d447f2f052372f7` | 1, 2, 3, 4, 66 | (a) |
| `transcripts/run_atlas3/ub_rllbec_1-10_k12.log` | `45243542e9227ebb5fc4134103dbc8b83761704c37875fcf87a2b94063137c0a` | 1, 2, 3, 4, 24 | (a) |
| `transcripts/run_atlas3/ub_rllbec_1-2_k12.log` | `5081d0065566057835464a44d0c5e7d6dffcc9cb4f677246836bbb9259546415` | 1, 2, 3, 4, 25 | (a) |
| `transcripts/run_atlas3/ub_rllbec_1-4_k12.log` | `6a14d5b51e389dd21ced1f4514735215f7e1c301437e208e406b9cdce82f4e32` | 1, 2, 3, 4, 25 | (a) |
| `transcripts/run_atlas3/ub_rllbec_3-4_k12.log` | `0642bc49918cc55f5dad5c3b1b5e4e0d2a0102ba6fdb2481826d1795299833ff` | 1, 2, 3, 4, 66 | (a) |
| `transcripts/run_atlas3/ub_rllbec_9-10_k12.log` | `b7548d537777cebdfa679f564a3df97fa2a4fb7964b0ec2d5c7f9c481ea141a9` | 1, 2, 3, 4, 66 | (a) |
| `transcripts/run_atlas3/ub_rllbsc_1-100_k12.log` | `fac1cac56b2e06deaaf542fc42740fdfb5825a2f0118a3392390ee7cebf5ba2a` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas3/ub_rllbsc_1-20_k12.log` | `d1301c042e3b6c37cda904311eee82dca010de98030300167c8a06f183fe50b5` | 1, 2, 3, 4, 14 | (a) |
| `transcripts/run_atlas3/ub_rllbsc_1-5_k12.log` | `bcb100f581b4230b1e2974d0f40c1ed00fca3662c3139e3db1757348e74e531a` | 1, 2, 3, 4, 66 | (a) |
| `transcripts/run_atlas3/ub_rllbsc_11-100_k12.log` | `c12e9e7d4e95ed69327e35883e971b0a1c12dc6909cca0ed959580611eb9f795` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas3/ub_rllbsc_3-10_k12.log` | `a8a64b428b7062e7b1eb9369abf5da15ad18dcc9e41148dde13ccd5a9cb6ba6a` | 1, 2, 3, 4, 66 | (a) |
| `transcripts/run_atlas3/ver_dec_1-10_k10.log` | `f8bcac63319d1ad03bc22b4d1c88c578608ced245531d9c3ca541342607747a0` | 2 | (a) |
| `transcripts/run_atlas3/ver_dec_1-2_k10.log` | `27c546e51a539a7af77d87b9980b2b2a65cf96d4d98a15d8fb25bd15c3383b0a` | 2 | (a) |
| `transcripts/run_atlas3/ver_dec_1-4_k10.log` | `681ed0ec8d0d0484f8b9d72396ed5206a713d31a57659dda65885e1cbbda536e` | 2 | (a) |
| `transcripts/run_atlas3/ver_dec_3-4_k10.log` | `a7c5a503cec72e4c3496cc503d50a0d01037da20d3dd5d7d5be6c6cfd122ec98` | 2 | (a) |
| `transcripts/run_atlas3/ver_dec_9-10_k10.log` | `fc46b50945957a779a74531a43c2770bea9ec39076b5f045ae92b3e9976ad547` | 2 | (a) |
| `transcripts/run_atlas3/ver_rllbec_1-10_k12.log` | `f55aae6b0b5783797d84f42c91ee27ae2bbaddfaf76c883e04ae6e5efb457d79` | 2 | (a) |
| `transcripts/run_atlas3/ver_rllbec_1-2_k12.log` | `d197c52eccc8dd4b5aaeee1d928fe85be2e155982d9a8716f5ebd892ee5841a6` | 2 | (a) |
| `transcripts/run_atlas3/ver_rllbec_1-4_k12.log` | `635c0c1bea35e0f67b8da4fdf28b6e46dc67b036871614bed2c79f79bb0c78c7` | 2 | (a) |
| `transcripts/run_atlas3/ver_rllbec_3-4_k12.log` | `6fb776b416bb132bf6b1061b67ebbfe1b521c79c9177140c3dd76a478088d5f6` | 2 | (a) |
| `transcripts/run_atlas3/ver_rllbec_9-10_k12.log` | `1f6e90137d377f5f74d9c2c1165594b13d3e5be821b9790deec0a956a0de6687` | 2 | (a) |
| `transcripts/run_atlas3/ver_rllbsc_1-100_k12.log` | `4c9804a558aede14b33a663d06d3e40a1d56147da28066440d2cc296c1d6ff68` | 2 | (a) |
| `transcripts/run_atlas3/ver_rllbsc_1-20_k12.log` | `234d0e24ef887eb7d9947e804a8a53569e68a8c01cc4d2bb94e062a09a5a90dc` | 2 | (a) |
| `transcripts/run_atlas3/ver_rllbsc_1-5_k12.log` | `0227394cb0dcb0593f7d429586d19fc0df844c6438cf9c3e0ef50d4b283daa56` | 2 | (a) |
| `transcripts/run_atlas3/ver_rllbsc_11-100_k12.log` | `537728484ce3d694cac42fad7449431587e0dd5d2d29242a8aacc43e1e8d6b3c` | 2 | (a) |
| `transcripts/run_atlas3/ver_rllbsc_3-10_k12.log` | `debb2a3a7b7ba9c80925d48f9ef1b1d379f4b1c6f7ee5368dbdbeb4d3ca3e268` | 2 | (a) |
| `transcripts/run_atlas4/K1_controls.log` | `5eec61b05a5cd825673dac4a30e3ac72d741142a9cf7fb8888bba50065be5e52` | 1, 2, 3, 4, 9 | (a) |
| `transcripts/run_atlas4/K2_tamp_dec_1-10_k10.log` | `31d15c0b386490f2a65de6ad5fc488835c5764d423bdec1df30187fff9b8470d` | 2 | (a) |
| `transcripts/run_atlas4/K2_tamp_rllbsc_1-5_k12.log` | `837621d02a098b837dca06875bb9f8d03c41f6d4cad66e16981bb8ec9df5e593` | 2 | (a) |
| `transcripts/run_atlas4/K2_tbuild_dec_1-10_k10.log` | `d70c55109f03918887bf9fa070fca7ccfea66d49825054ad773f2db65365e20a` | 1 | (a) |
| `transcripts/run_atlas4/K2_tbuild_rllbsc_1-5_k12.log` | `6efb78d57ed6a48c7cd1b03f1780165c3c4c768e4f45b74ccd0b8e84802a44ed` | 1 | (a) |
| `transcripts/run_atlas4/engine_sha256.txt` | `6211a0599ddd2cac914ea42a829e4f7fbe25b6c8d8e31db0fd180bc5bae6fb16` | 1, 2, 3, 4 | (a) |
| `transcripts/run_atlas4/ub_dec_1-10_k10.log` | `f60890ed71d6e2f6e57fedb5bf95861eb5aafe6f49964a0929aa052677087cd9` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_dec_1-2_k10.log` | `8089cfb484944266c022320ab1779d21bfd068476ce771fb0b13e6c8767b9416` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_dec_1-4_k10.log` | `a5053ec7e00aa30594e13f5be76661725fdb0c2ff9433105e05b19273483a8ba` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_dec_3-4_k10.log` | `a8986998f47eb83f164207b833406d70f40bca324b814ef76da4489451d647c8` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_dec_9-10_k10.log` | `becd2cdc135db1e530972ada5225952776f5c0aed175793deba5edcf400b1319` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_rllbec_1-10_k12.log` | `8a0ed53089eaf273b2abbe9793b0d44d25b8ae15fcb847c499b75305344eb8f1` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_rllbec_1-2_k12.log` | `e1785ec4fee9022a5deecac6b6e312108dd933cb433b09721a428523f4362b53` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_rllbec_1-4_k12.log` | `45f2492c5107a1a98a0549465102d0691a80615adfc82a579489794916a4fd4b` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_rllbec_3-4_k12.log` | `ac0ac2f1cc3031873510ba88dccfd1c6c9aba48fb1bbd84428d47c7d7d861f51` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_rllbec_9-10_k12.log` | `393c4d97d48b6bbddf594c5af5ba2e5eadbb96d3ce6c460649963cfef9751b6a` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_rllbsc_1-100_k12.log` | `df5d76f1ad8ab06b0273132a9b1216956db156c336c5fb6184ce5fae30f7a89b` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_rllbsc_1-20_k12.log` | `05924650c59c35a9660a236c3c8a77658625e98a9dc3a7fe3273077ad2556fb9` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_rllbsc_1-5_k12.log` | `8b394b404ad38b9008b346487e88bee1a59212fa3be4825562f0e0f138245207` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_rllbsc_11-100_k12.log` | `b2ff325cf76eb9855ed271c739754ce57b4058bb030d20831220a916f12eeea7` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ub_rllbsc_3-10_k12.log` | `6c1f53d10e0f560f2f6931a4c90d51275fd5eba0557774c3773eeb1b25a708c6` | 1, 2, 3, 4, 13 | (a) |
| `transcripts/run_atlas4/ver_dec_1-10_k10.log` | `a2e01e2d9c7c7de1a4b478f5423eb1af5d25bc460e824721d8be03e2b3179ef6` | 2 | (a) |
| `transcripts/run_atlas4/ver_dec_1-2_k10.log` | `0760704a8fc49cc70859585b3c83f63cf2f6e3e1b6c56afcbb6053e72eb46bae` | 2 | (a) |
| `transcripts/run_atlas4/ver_dec_1-4_k10.log` | `c16adae0365076ed5fab2b5c37f024457c4a6d8768dd5ba0e34fecd457460970` | 2 | (a) |
| `transcripts/run_atlas4/ver_dec_3-4_k10.log` | `cd1cd2249cc14fc45510b9a5ea8ba46afcfe7ab428ee3512e7745d351ee73d74` | 2 | (a) |
| `transcripts/run_atlas4/ver_dec_9-10_k10.log` | `38e83f1f28d645ede73462f39dae054a2b1f2ece06fa11dcec01038210434e14` | 2 | (a) |
| `transcripts/run_atlas4/ver_rllbec_1-10_k12.log` | `5ef871772ddcb88992d132f6b4ebc8060c739424970a51b2c5e81e178b010f59` | 2 | (a) |
| `transcripts/run_atlas4/ver_rllbec_1-2_k12.log` | `c9e6480fe20ecfa7b44bf770add115205375f89974ecea964593360821519776` | 2 | (a) |
| `transcripts/run_atlas4/ver_rllbec_1-4_k12.log` | `3c5e56ee0e62baf887330d439c4b2dbfced66831d68c0269b71aa18637e3ca8b` | 2 | (a) |
| `transcripts/run_atlas4/ver_rllbec_3-4_k12.log` | `dd4afb6479bc80bd77b3fe5640352401f0e3f7e2571920df31f6a36d8e1b3a3c` | 2 | (a) |
| `transcripts/run_atlas4/ver_rllbec_9-10_k12.log` | `aaac525de294eaccccba0d9d63b6aa4e8d6fec7937c8a4330f918cc1e74e0c18` | 2 | (a) |
| `transcripts/run_atlas4/ver_rllbsc_1-100_k12.log` | `4fec76b7a6898f1eebef750dfa085222c263469128e72034fe5e0967ea2c086d` | 2 | (a) |
| `transcripts/run_atlas4/ver_rllbsc_1-20_k12.log` | `166e3b539c6e4ecd4c4cd8093124c4632110a9c9079a697edda8d6c3c4567317` | 2 | (a) |
| `transcripts/run_atlas4/ver_rllbsc_1-5_k12.log` | `967af1710e66d4c463e2a20facb405f0a367a4d68bdb7af89b4a206adb21a859` | 2 | (a) |
| `transcripts/run_atlas4/ver_rllbsc_11-100_k12.log` | `3566bd601570262195bb6a5d09e47563c5a0ff00fa47b70f1cffc76c3106a138` | 2 | (a) |
| `transcripts/run_atlas4/ver_rllbsc_3-10_k12.log` | `be21199653ebf25b3749a807b871570053342a9cea2c1ee223fafa665ba6f119` | 2 | (a) |
| `transcripts/run_atlas5/K1_controls.log` | `74c54b7f92857bea1f408e6264340b28a494f53ddf378f7f636ed579942d040c` | 1, 2, 3, 4, 9 | (a) |
| `transcripts/run_atlas5/K2_tamp_dec_1-10_k10.log` | `e35b92106eed19a4153f6c02521271d8f2b11cc9c8627234d441fac0f99022ef` | 2 | (a) |
| `transcripts/run_atlas5/K2_tamp_rllbsc_1-5_k12.log` | `a42d9a1c329fb99e6fc4b29d4ff61f53ffb33504d323c75e118d9ebca13b625b` | 2 | (a) |
| `transcripts/run_atlas5/K2_tbuild_dec_1-10_k10.log` | `b36cf80357db21b92e5693ce3772b4a386b6c97e224810ad3b09b02adcb9743e` | 1 | (a) |
| `transcripts/run_atlas5/K2_tbuild_rllbsc_1-5_k12.log` | `39ae152fc9c76a4e16b9ce9840a5599ee86e0557d62886f35ac7b793df2d26c4` | 1 | (a) |
| `transcripts/run_atlas5/engine_sha256.txt` | `5c9e4567ae6339d919af8f3f0b09fc9acccdf45b325d9eefecbb6e332f4fd12e` | 1, 2, 3, 4 | (a) |
| `transcripts/run_atlas5/ub_dec_1-10_k10.log` | `01cd5737ead1b7796add10c1bc4e7123d750ead80bc709afb89fbbea0fc45ded` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_dec_1-2_k10.log` | `7fb5a4c29fe86ae859acf35e09021b990597c768b94c150e2d74651ec7b04ca4` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_dec_1-4_k10.log` | `df61740050d63ca19bbf8f5c3f37d384f8a2048f1894d5a512b816a6b1fe1885` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_dec_3-4_k10.log` | `a50c21c635b3ce7701559cdc95e6a83e1de9479821b3c80a6318e3cda04ba827` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_dec_9-10_k10.log` | `55f70e2da45ff26331c598e485575c41dd163dd1095d7eb792974bee7c0b5994` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_rllbec_1-10_k12.log` | `f790e0abf3cb9e56843bd78a095183fc4d7526ca2e7ced0bb6686e0e6716ae00` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_rllbec_1-2_k12.log` | `eab3dec21b1e159ef90e425abbaee109a50a83529c02f81591f30b3b4942aa61` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_rllbec_1-4_k12.log` | `c27115500a9539dc38eb033d13f7db67dab64c1b69f6f831b32b49d0784be948` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_rllbec_3-4_k12.log` | `0fd940133c9432c43576198bc39ad6bc4fd5ab52bf4e95225ca4a2a850d1b44b` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_rllbec_9-10_k12.log` | `02433ae7dc1ce37b419fe0b3328e0c840d902df31edf95908ebb3c0196e045d2` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_rllbsc_1-100_k12.log` | `38dc2374f9d6cc65fb5118cd451c7cb498c434c369f7bb5cd30e37bddc330e5e` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_rllbsc_1-20_k12.log` | `9172e0848577f9a17186478b7ba9a71b77227bca16dd73ebd700af7009853e63` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_rllbsc_1-5_k12.log` | `7c600b5736a171acc635e046143ce89acbbbaffea082b8a0eafe0fa4cdce8384` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_rllbsc_11-100_k12.log` | `372dd11923c372e81356381cb2c755fc8720b8ab818880e09d03c196437823dc` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ub_rllbsc_3-10_k12.log` | `250137992a7fd0fc756b759b502e50515c67102e895526fbe76f54be16859bdc` | 1, 2, 3, 4, 15 | (a) |
| `transcripts/run_atlas5/ver_dec_1-10_k10.log` | `d3d21f31245ec2d47a6d89902b8c50ffa82b57f6062fcd0c2d3dae610b51efe6` | 2 | (a) |
| `transcripts/run_atlas5/ver_dec_1-2_k10.log` | `43c82c41b75b2e100aa8d0ca41ca4afd8a689740314defc8ebb5e86aaecf1efd` | 2 | (a) |
| `transcripts/run_atlas5/ver_dec_1-4_k10.log` | `9520e368ef5074a96b5c0d6ba4842ce819ad62603d798bf8a0fa87a6fc390387` | 2 | (a) |
| `transcripts/run_atlas5/ver_dec_3-4_k10.log` | `2763b2638f81ad61f13ef489ba7743d106862d060766237bc5419719b1c22ed0` | 2 | (a) |
| `transcripts/run_atlas5/ver_dec_9-10_k10.log` | `cb8ace5e64240fa4b24e9439dc855fee39086602a148864c78ac859ac24ff719` | 2 | (a) |
| `transcripts/run_atlas5/ver_rllbec_1-10_k12.log` | `def9cc58b87a076fd20ca8f7112ffbed5b915c1d2b463100e99b4e603aa605fe` | 2 | (a) |
| `transcripts/run_atlas5/ver_rllbec_1-2_k12.log` | `2b8939af97a143a3ec6459f22d0d6f6baae7c853b4f2f69458a94b0943ae730c` | 2 | (a) |
| `transcripts/run_atlas5/ver_rllbec_1-4_k12.log` | `d7381e31b722bde470ad7147d291110c3d149c86c30b0051a62472db20d03ec6` | 2 | (a) |
| `transcripts/run_atlas5/ver_rllbec_3-4_k12.log` | `10bff4d32122eb57720cefe04823be65f34e4a80fa9fae9356e84e9703a45c5b` | 2 | (a) |
| `transcripts/run_atlas5/ver_rllbec_9-10_k12.log` | `d97b5cb7405253f58f05e3e82a73f70650a576e4ac9536403901ec17e09a4289` | 2 | (a) |
| `transcripts/run_atlas5/ver_rllbsc_1-100_k12.log` | `5966670e2b6e744b63497441445e38689a15dcc3378b6b87185ae0099b840c0c` | 2 | (a) |
| `transcripts/run_atlas5/ver_rllbsc_1-20_k12.log` | `e5372b6ab9d452c1480dec2535f333f3bb555a19781a598e50579f9aa5a0ae20` | 2 | (a) |
| `transcripts/run_atlas5/ver_rllbsc_1-5_k12.log` | `f3372e300d0da0638c1ccb3a12d5c4b0b5a41bd648441564691273e06b590a95` | 2 | (a) |
| `transcripts/run_atlas5/ver_rllbsc_11-100_k12.log` | `348d20f2b36a70c99f63fbf3c4999a08c80b6a4157537db46e7fce8801c45c60` | 2 | (a) |
| `transcripts/run_atlas5/ver_rllbsc_3-10_k12.log` | `cf905dc4e2a43a5a40e1294a4bd8d1880809a802e09569ee3595454f91c1ab38` | 2 | (a) |
| `transcripts/run_atlas6/K1_controls.log` | `fbeb02f5c60c179b354b408256fe1a9bc42c882baaee7c582d89e74f339b3c31` | 1, 2, 3, 4, 9 | (a) |
| `transcripts/run_atlas6/K2_tamp_dec_1-10_k10.log` | `097c7df9c8aeffad02113a70684af6e17596900d9ec2909843e71f64637b01e5` | 2 | (a) |
| `transcripts/run_atlas6/K2_tamp_rllbsc_1-5_k12.log` | `7775ebb98f817e9110e11460a52f85c0afa3de81f6006a6ddd7b9400d267dc03` | 2 | (a) |
| `transcripts/run_atlas6/K2_tbuild_dec_1-10_k10.log` | `1959783d175a6ce462bf9365cb12dbc6457299d338fab29369b3f2b7cb59aab1` | 1 | (a) |
| `transcripts/run_atlas6/K2_tbuild_rllbsc_1-5_k12.log` | `0c1fb9c4c58d400fe8afb38e676bd0064b989a6d48be51db07e88470b37d0986` | 1 | (a) |
| `transcripts/run_atlas6/engine_sha256.txt` | `7bf462e5cd22c04e9038d5cf37bebe791cc05fff15027f614dc415aaa0b680a2` | 1, 2, 3, 4 | (a) |
| `transcripts/run_atlas6/ub_dec_1-10_k10.log` | `b65b9e48cf6e8b8e38ac3ef6076f771f7b8a42717c908021fa7050a1401b7bdf` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_dec_1-10_k11.log` | `3d6bbf00568571a9064178c460d5d9be54700981581fee88fb50391bc2c9a312` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_dec_1-2_k10.log` | `3f40111ada9a3aead661c3d9531d414547dc3e3247c360946af0a400419cabbc` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_dec_1-4_k10.log` | `eb69f4c3ea834c8f904a13db38e73e24f744782e0d6e1158d49262cedd2ee26a` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_dec_3-4_k10.log` | `03ba9b3539e8ca7165c84b71416a250e119d196e85967e8b449b5a430f4d3a0e` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_dec_9-10_k10.log` | `efeb75835ee89a70135f5cb6df816cf2a35ad1dd5214f91b8a6eebce36f2f3dd` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_rllbec_1-10_k12.log` | `316a25e4891babe73b6d245ac0558739b4d03dc6e26f005ec67162be9cbe60f4` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_rllbec_1-2_k12.log` | `c9a3318866ae4a75fa4567647869b915dc8875b44b73e47fd773e8ace7b9cc71` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_rllbec_1-4_k12.log` | `5b5578f5ec5614d586b0d85ea963840a178faf8cdea4d83d1883d1edcb3fe66b` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_rllbec_3-4_k12.log` | `a78d7a90af40fd400b106a8683d36bba73a9b929764bf70b3fa2a32706a34e06` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_rllbec_9-10_k12.log` | `f0a6bdd3536d9a582c6c31dbda6d946c7e44b7b30c3bf6949ac8d37511861673` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_rllbsc_1-100_k12.log` | `be906ebe6f44acbca4e7a37ef1379ce7257e1b8102963523651768ec5a1f80af` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_rllbsc_1-20_k12.log` | `7433d1ee7731b35cbabdb350c39f67f391608bbf30dad15ddace246f8f08abd8` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_rllbsc_1-5_k12.log` | `ec45b1d67618c778cdbcb627240057efb9ddd3767d0c6b105cd5748d88526d46` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_rllbsc_11-100_k12.log` | `00ab7baca9139d7e9bfe85080b6b6eeadce905c4c9c95319eee05e2d1bb2b805` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ub_rllbsc_3-10_k12.log` | `aac45a17d1dd74ab39dcc52e44081cc1907760eda497740eea33c7b19fc90e3b` | 1, 2, 3, 4, 19 | (a) |
| `transcripts/run_atlas6/ver_dec_1-10_k10.log` | `d3eacea018e2471c33dbacfec662b5cbf8543f174c936758116b8131283afb5a` | 2 | (a) |
| `transcripts/run_atlas6/ver_dec_1-10_k11.log` | `3e248411469903c0a80ef494a095ba8e070dcb47cd1c32ac75763f7246223dd4` | 2 | (a) |
| `transcripts/run_atlas6/ver_dec_1-2_k10.log` | `329a851f389f4d237137a7eaeb3b73060173c755766a81cd8f72e8b7004c09be` | 2 | (a) |
| `transcripts/run_atlas6/ver_dec_1-4_k10.log` | `a2b1017b1feaa719d39bee4068edb0bcce84fb67bea99d54c957b52b7a062298` | 2 | (a) |
| `transcripts/run_atlas6/ver_dec_3-4_k10.log` | `d2b69beba3af5daa0f91d5ea12efb3b693c126626f2d347acc167a7c830ba5fe` | 2 | (a) |
| `transcripts/run_atlas6/ver_dec_9-10_k10.log` | `842ffd3a3deab3ba636dcee3c098ddabede1fa95a9a7af7e7d98f78855391841` | 2 | (a) |
| `transcripts/run_atlas6/ver_rllbec_1-10_k12.log` | `9d5ca9cc04521c9cd909bf745d8053a6963382b9c7977fe1be4250256e687041` | 2 | (a) |
| `transcripts/run_atlas6/ver_rllbec_1-2_k12.log` | `69b87361f8a0789ed32a0a335266f82c2df56b7811579fb39c4aa1df0b0f2165` | 2 | (a) |
| `transcripts/run_atlas6/ver_rllbec_1-4_k12.log` | `9e531445d0606fbdf1ee061e2f8269277e64629bd0f20f98836819c71474504d` | 2 | (a) |
| `transcripts/run_atlas6/ver_rllbec_3-4_k12.log` | `9431a96a8618372c5cfe73a6c2bd1189ff6f45b67d4eb53e41a2544e504d5d61` | 2 | (a) |
| `transcripts/run_atlas6/ver_rllbec_9-10_k12.log` | `576ec4c8928251147abdaac4e2436b75da1717cc421eb8abe61d3559c860dbaa` | 2 | (a) |
| `transcripts/run_atlas6/ver_rllbsc_1-100_k12.log` | `8413a13586ca6ce8617ea59f98f2ef27557e4ccc7674b64dc7c1cb1b6b88aeb0` | 2 | (a) |
| `transcripts/run_atlas6/ver_rllbsc_1-20_k12.log` | `a6d8ff4bf6eb9fd3a9246b8888092daa7103d0085c09d6258fae7723bf888d19` | 2 | (a) |
| `transcripts/run_atlas6/ver_rllbsc_1-5_k12.log` | `35a416442c6e396dbe3d6a37dac41f1fd2a091745755474560e7994bf9692d4e` | 2 | (a) |
| `transcripts/run_atlas6/ver_rllbsc_11-100_k12.log` | `6a5000f7e8a474a7dd38c33cb81a376b8b12994f7e498e3180ff622fc639b58d` | 2 | (a) |
| `transcripts/run_atlas6/ver_rllbsc_3-10_k12.log` | `e20ff3edb53489eaa3239fad6fbb1f756fece7f0597ec5e0d805843061160332` | 2 | (a) |
| `notes/NODE-B-ATLAS.md` | `dca47e7bb214335f40e9e6c6772930c21055fff01d74044d18ed586ca2b3e583` | 26 | (a) |
| `bars/BAR-ATLAS1.md` (second pass, after rule (a)/(b)) | `70efe8e963b516f4e9741cbf773ebdf231b854af46e53ef7a8cafea615a833b1` | 51 | (e) owner's first name -> 'the owner' |
| `second-implementation/transcripts/log_dualB_K14.txt` | `6c542f1bdafb8ee17f1f54d1a3e35e9ef54419c09e05658ffde36788fa082211` | 6 | (a) |
| `second-implementation/transcripts/lead-recheck/run.sh` | `ec156c9d62dd2d66470c92208128c80579360015804a232a55d91747a1109e73` | 2, 3, 4 | (a), (c) |
| `second-implementation/transcripts/log_dualB_K14.txt` | `1399ea885ed5d853e308adf7b741289673771920e56690c11e7a1c5e9ae1b292` | 9 | (f) home-folder Python path -> `<python>` |
| `second-implementation/RESULT.md` | `9b8bce6c1041f30e090a07751f710a7296b30fc1648d1695488fa681c21ad0b5` | 11 | (g) home-folder tool path and product name -> neutral wording |
| `notes/PRIOR-ART-ATLAS.md` | `0c5cbacc84869cc43901df01c8e9ca62d87d94c3d6cc2351624ff83efcaef35c` | 16, 49, 85, 105 | (h) third-party-number remarks withheld |
| `notes/DESIGN-ATLAS.md` | `dfd9d9e2cf2e59fb71d8989c034c8af0050499df574711c2dd709125a2161a89` | 62, 73 | (h) third-party-number remarks withheld |
| `referees/REFEREE-ATLAS1.md` | `b8c4a4b7bf79bd7d90279a27b921a7c6a6da8455d958fbffdeb2f395e7990e8e` | 19, 21, 23, 24 | (h) third-party-number remarks withheld |

A file listed twice was changed in two passes; its first row gives the original sha256, the second row the sha256 after the
first pass.

## Notes that are not patches

- Certificates in `certificates/` are gzip-compressed copies of the certified JSON files (`gunzip -k` restores the exact bytes).
- `notes/NODE-B-ATLAS.md` cites a step of an Ising-channel note (`ising/lb/NODE-B-ISING.md`) that is not shipped in v1; the
  steps it uses are restated in the note itself, and the transfer to these channels was checked by the referee
  (`referees/REFEREE-ATLAS1.md`).
- Transcripts name working-folder files by their (now relative) working paths, not the package layout; `code/README.md`
  gives the package commands.
