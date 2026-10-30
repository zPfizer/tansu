"""Ham anlık görüntüden `sinama.gunler` sözlüğünü kurar, verilen motor kopyasıyla (her panel satırı kendi motoruyla).

python kur.py <motor klasörü> <cikti.pkl> [<veri kökü> <kimlik>]
Varsayılan girdi eski denemelerin ham görüntüsüdür: 20260101-0000 artı INTEK, LRSHO, LYDHO (eski denemelerin
`gunler-2014-2025-A.pkl` dosyası bu kökten ve b9f6107 motoruyla kuruldu; f4ca87d ile 673 hissenin hepsinde aynıdır).
"""

import hashlib
import os
import sys
from pathlib import Path

wt, cikti = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
sys.path.insert(0, str(wt))

import pandas as pd  # noqa: E402

import tansu  # noqa: E402
from tansu import sinama, veri  # noqa: E402

assert Path(tansu.__file__).resolve().is_relative_to(wt), tansu.__file__
if len(sys.argv) > 3:
    KOK, KIMLIK = Path(sys.argv[3]), sys.argv[4]
else:
    KOK = (
        Path(os.environ["TEMP"])
        / "tansu-gartley-dogrulama-20261029"
        / "eksik-sembol"
        / "veri-A"
    )
    KIMLIK = "20260101-0000"
g = sinama.gunler(veri.oku(KIMLIK, KOK))
pd.to_pickle((KIMLIK, g), cikti)
print(hashlib.sha256(cikti.read_bytes()).hexdigest(), len(g))
