# Spec: Tansu sınaması (`python -m tansu tansu-sinama`)

Akış: `tansu-yeni-is` (A). Kapsam: feature. Levent 16.10: "Ayrı bir oturumda Tansu ne diyorsa onu yap. Yani bu backtest
modülü Tansu'yla Tansu'nun dediğiyle birebir olması lazım kodlarımızda. Ve bu backtest modülünün de sitede olması lazım."
Levent 16.10: "Backtest yapılırken CPU ve GPU ve paralel ilerleme durumlarını da analiz et. Aynı şekilde bu durumlarda
bilgisayarın durumuna göre optimize edilsin mutlaka."

Job to be done: Levent wants to see, per strategy and per stock, what Tansu's own test method says (optimise per stock,
robust region, compare to buy-and-hold, his table columns), beside our honesty check, on the site.

Vekil (Sharpen, 16.10): accepted all 8 proposed YORUM defaults; added: show total pairs tried and the share with a robust
region; walk-forward year without a robust region stays in cash; flags are labels, not filters; one test for 1 vs N
workers; the GPU number must be measured.

## Behaviour (owner after merge: docs/TASARIM.md 5.14)

The TASARIM 5.14 text below is the document. Code follows it.

## Interfaces (test faces; module `tansu/tansusinama.py`, hash dışı)

- `makine() -> dict`: `cekirdek` (logical cores), `bellek_bos_gb`, `bellek_toplam_gb`, `gpu` (name or None).
- `isci_sayisi(cekirdek, bellek_bos_gb, is_sayisi, isci_bellek_gb=ISCI_BELLEK_GB) -> int`.
- `islem_getirisi(giris, cikis, m=MASRAF) -> float`.
- `olculer(getiriler, tutma, egri, pozisyonda) -> dict`: Tansu table columns.
- `saglam_bolge(net: np.ndarray) -> dict`: `saglam` (bool array, grid shape), `secilen` (flat index or None),
  `en_iyi` (flat index), `para_cikmaz` (bool).
- `ileri(islemler_hucre, sekil, bas, son) -> dict`: walk-forward mode.
- `calistir(anlik, sektor, aileler, isci, hisse=None, ilerleme=print) -> dict`: whole run; identical for 1 and N workers.
- CLI: `python -m tansu tansu-sinama [--kok] [--kimlik] [--isci N] [--hisse N] [--aile A] [--sektor-kok veri]`.

## Out of scope / open items

Module-1 variants (1,5 ATR stop, half-sale rules, R/R 1:2) wait for the modul-1-kod PR. Pivot confirmation rule: no
pivot in the two families. Eye check of scan results (göz ile inceleme): no chart in this module. Kelly, fund analysis,
crypto, E K1–K3 readiness, E K4, intraday vendor, 5.12 acceptance rules: Levent.
