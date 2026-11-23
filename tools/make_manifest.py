#!/usr/bin/env python
"""make_manifest.py -- write or check MANIFEST.sha256: the sha256 of every file in this repository except the manifest
itself, version-control metadata and caches.

  python tools/make_manifest.py           write MANIFEST.sha256
  python tools/make_manifest.py --check   verify every listed file and that no file is missing or unlisted (exit 0 = all match)
"""
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', '__pycache__', 'runs'}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def files():
    out = []
    for d, dirs, fs in os.walk(ROOT):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for f in sorted(fs):
            rel = os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/')
            if rel != 'MANIFEST.sha256':
                out.append(rel)
    return out


def main():
    man = os.path.join(ROOT, 'MANIFEST.sha256')
    if '--check' in sys.argv:
        listed = {}
        for ln in open(man, encoding='utf-8'):
            h, p = ln.rstrip('\n').split('  ', 1)
            listed[p] = h
        bad = [p for p, h in listed.items() if not os.path.exists(os.path.join(ROOT, p)) or sha(os.path.join(ROOT, p)) != h]
        extra = [p for p in files() if p not in listed]
        for p in bad:
            print('MISMATCH or MISSING', p)
        for p in extra:
            print('UNLISTED', p)
        print('manifest: %d files, %d mismatched or missing, %d unlisted' % (len(listed), len(bad), len(extra)))
        sys.exit(1 if bad or extra else 0)
    rows = ['%s  %s' % (sha(os.path.join(ROOT, p)), p) for p in files()]
    open(man, 'w', encoding='utf-8', newline='\n').write('\n'.join(rows) + '\n')
    print('wrote MANIFEST.sha256 (%d files)' % len(rows))


if __name__ == '__main__':
    main()
