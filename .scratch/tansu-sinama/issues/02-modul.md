# 02 Modül: `tansu/tansusinama.py` ve `tansu-sinama` komutu

**Status:** ready-for-agent
Blocked by: 01

Build the faces in spec.md test-first (red test committed before code). Reuse `motor.mumlar`, `motor.Zincir`,
`aileler.sinyal`, `ciftbolme.hedef`, `saglamlik.IZGARA`; do not edit aileler.py, gostergeler.py, motor.py. Add
`tansusinama.py` to `kayit.HASH_DISI`, the CLI command to `__main__.py`, `psutil==7.2.2` to pyproject.

Done when: tests for metrics (hand-computed), robust region, para çıkmaz, flags, walk-forward, worker count, and
1 vs 2 workers identical are green; the test gate is green.
