"""Eşdeğerlik ağı: ürünün `sina` ve `ayarla` çıktısını sentetik senaryolarda bir klasöre yazar. İki kod kökünün (taban ve
baş) klasörü `diff -r` ile karşılaştırılır; fark, yeniden düzenlemenin davranışı değiştirdiğini gösterir.

Kullanım:
    python -X utf8 kurulum/esdeger.py <kaynak kökü> <çıktı klasörü>
    python -X utf8 kurulum/esdeger.py --deneme      (bu depoyu iki kez koşar; çıktı aynı olmalı)

`tansu` kaynak kökünden yüklenir. Sentetik girdi her zaman bu deponun tests/sentetik.py dosyasından okunur; böylece
taban ve baş aynı girdiyi görür. Ürün yolu: `veri.Anlik` -> `tansu.__main__.main`; kendi yükleyicisi yoktur. Senaryo
başına çıktı: her adımın argv'si, dönüş kodu, stdout, stderr ve senaryonun yazdığı bütün dosyalar. `ayarla` json'undaki
kod sürümü sabitlenir (git SHA'sı kökten köke değişir); json ve rapordaki tarih o günün tarihidir, iki koşu aynı gün
yapılmalıdır.

Ağ yalnız 15 senaryonun çalıştırdığı yolları görür. Eşit dokunuş ve dolum günü hedefi gibi kenar kurallarda fark vermez
(30.10 inceleme); onları tests/test_referans_motor.py korur."""

import contextlib
import dataclasses
import filecmp
import importlib
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

DEPO = Path(__file__).resolve().parents[1]
GUNLER = pd.bdate_range("2019-01-02", "2026-09-30")


def yukle(kok: Path):
    """`tansu`yu `kok`ten, sentetik girdiyi bu depodan yükler. Dönen: (komut modülü, sentetik modülü)."""
    sys.path.insert(0, str(kok))
    komut = importlib.import_module("tansu.__main__")
    if not Path(komut.__file__).resolve().is_relative_to(kok):
        raise SystemExit(f"tansu {kok} dışından yüklendi: {komut.__file__}")
    tanim = importlib.util.spec_from_file_location(
        "esdeger_sentetik", DEPO / "tests" / "sentetik.py"
    )
    sentetik = importlib.util.module_from_spec(tanim)
    tanim.loader.exec_module(sentetik)
    ayar = importlib.import_module("tansu.ayar")
    for ad in ("ISCI", "kod_surumu"):
        if not hasattr(ayar, ad):  # ad değişirse sabitleme sessizce boşa düşmesin
            raise SystemExit(f"tansu.ayar.{ad} yok: kurulum/esdeger.py güncellenmeli")
    ayar.ISCI = 1
    ayar.kod_surumu = lambda: "esdeger"
    return komut, sentetik


def senaryolar(sentetik):
    """Dönen: kayıtlı stratejiler ve senaryolar. Senaryo: (ad, adımlar, tablolar, strateji, durum, json, ek durum
    satırları); strateji None ise kayıtlı listede yoktur."""
    stratejiler = importlib.import_module("tansu.stratejiler").STRATEJILER
    asil = dict(stratejiler)
    SABIT, gun_tablosu = sentetik.SABIT, sentetik.gun_tablosu

    def tek_nokta(ad, **ek):
        s, v = asil[ad], {**SABIT[ad], **ek}
        return dataclasses.replace(
            s, varsayilan=v, aralik={k: (v[k],) for k in s.aralik}
        )

    def rastgele(sembol, tohum, kilit=0.015):
        return {
            f"R{j:02d}": sentetik.rastgele_tablo(
                tohum + j, n=len(GUNLER), bas=GUNLER[0], kilit=kilit
            )
            for j in range(sembol)
        }

    gy = {"AKBNK": gun_tablosu(sentetik.gartley_yolu(), bas="2022-01-03")}
    oy = {"AKBNK": gun_tablosu(sentetik.ortalama_yolu(), bas="2022-01-03")}
    rw = rastgele(4, 7)
    duz = {"DUZ": gun_tablosu(np.linspace(10, 12, 1900), bas=GUNLER[0])}
    gt = {
        f"G{j:02d}": sentetik.gartley_tekrar(
            n=len(GUNLER), tohum=11 + j, carpan=1 + j, bas=GUNLER[0]
        )
        for j in range(7)
    }
    ok = asil["ortalama-kesisim"]
    sma = {**SABIT[ok.ad], "ortalama": "SMA", "cift": "9/21", "teyit_gun": 0}
    ok2 = dataclasses.replace(ok, varsayilan=sma, aralik={"teyit_gun": (0, 2)})
    ok3 = dataclasses.replace(ok, varsayilan=sma, aralik={"teyit_gun": (0,)})
    g = asil["gartley"]
    gv = {**SABIT["gartley"], "tolerans": 0.03}
    bos_sinyal = importlib.import_module("tansu.strateji").bos_sinyal

    def bos_nokta(gun, p):  # tolerans 0.03 hiç işlem açmaz: karışık boş ve dolu pencere
        return bos_sinyal(gun.index) if p["tolerans"] == 0.03 else g.hesapla(gun, p)

    karisik = dataclasses.replace(
        g,
        varsayilan=gv,
        aralik={**{k: (gv[k],) for k in g.aralik}, "tolerans": (0.03, 0.05)},
        hesapla=bos_nokta,
    )
    sinandi_json = '{"parametreler": {}, "suzgecler": ["nabiz"]}'
    ek = "eski,beklemede,2026-10-26,\nbaska,sinandi,2026-10-26,\n"
    gartley_tek = tek_nokta("gartley")
    sina, ayarla = [["sina", "gartley"]], [["ayarla", "gartley"]]

    def sn(ad, adimlar, tablolar, strateji, durum="taslak", json=None, ek=""):
        return ad, adimlar, tablolar, strateji, durum, json, ek

    return asil, [
        sn("01-gartley-sina", sina, gy, gartley_tek),
        sn("02-kesisim-sina", [["sina", ok.ad]], oy, tek_nokta(ok.ad)),
        sn(
            "03-gartley-ayarla-puansiz",
            ayarla,
            gy,
            gartley_tek,
            "sinandi",
            sinandi_json,
        ),
        sn(
            "04-rw-kesisim-ayarla-sina",
            [["ayarla", ok.ad], ["sina", ok.ad]],
            rw,
            ok2,
            "sinyalde",
        ),
        sn("05-rw-gartley-sina", sina, rw, gartley_tek),
        sn("06-duz-gartley-sina-bos", sina, duz, gartley_tek),
        sn("07-duz-kesisim-ayarla-bos", [["ayarla", ok.ad]], duz, ok2),
        sn("08-bilinmeyen", [["sina", "yok-boyle"]], gy, None),
        sn("09-beklemede-ayarla", ayarla, gy, gartley_tek, "beklemede"),
        sn("10-bozuk-json", sina, gy, gartley_tek, json="[]"),
        sn("11-sinanan-sayisi", sina, gy, gartley_tek, ek=ek),
        sn("12-gtekrar-gartley-sina", sina, gt, gartley_tek),
        sn("13-gtekrar-gartley-ayarla", ayarla, gt, gartley_tek),
        sn("14-karisik-ayarla", ayarla + sina, gt, karisik),
        sn(
            "15-tavan-seri-kesisim-sina",
            [["sina", ok.ad]],
            rastgele(6, 23, kilit=0.05),
            ok3,
        ),
    ]


def kos(kok: Path, hedef: Path) -> int:
    if hedef.exists() and any(hedef.iterdir()):
        raise SystemExit(f"çıktı klasörü boş değil: {hedef}")
    komut, sentetik = yukle(kok)
    stratejiler = importlib.import_module("tansu.stratejiler").STRATEJILER
    asil, liste = senaryolar(sentetik)
    eski = Path.cwd()
    for ad, adimlar, tablolar, strateji, durum, json, ek in liste:
        sad = strateji.ad if strateji is not None else "gartley"
        stratejiler.clear()
        stratejiler.update(asil)
        if strateji is not None:
            stratejiler[sad] = strateji
        a = sentetik.anlik(tablolar)
        komut.son_anlik = lambda kok, a=a: a
        cikti = hedef / ad
        cikti.mkdir(parents=True)
        with tempfile.TemporaryDirectory(prefix="esdeger-") as gecici:
            klasor = Path(gecici)
            komut.PROJE = klasor  # eski taban kökü bilmez, chdir ile aynı klasörü okur
            (klasor / "stratejiler").mkdir()
            (klasor / "stratejiler" / "durum.csv").write_text(
                f"ad,durum,tarih,not\n{sad},{durum},2026-10-26,\n{ek}", encoding="utf-8"
            )
            if json is not None:
                (klasor / "stratejiler" / "ayarlar").mkdir()
                (klasor / "stratejiler" / "ayarlar" / f"{sad}.json").write_text(
                    json, encoding="utf-8"
                )
            os.chdir(klasor)
            try:
                for i, argv in enumerate(adimlar):
                    out, err = io.StringIO(), io.StringIO()
                    with (
                        contextlib.redirect_stdout(out),
                        contextlib.redirect_stderr(err),
                    ):
                        sonuc = komut.main(argv)
                    metin = f"argv={argv}\nkod={sonuc}\n--stdout--\n{out.getvalue()}--stderr--\n{err.getvalue()}"
                    (cikti / f"adim{i}.txt").write_text(
                        metin.replace(str(klasor), "<KOK>"), encoding="utf-8"
                    )
            finally:
                os.chdir(eski)
            for yol in sorted(klasor.rglob("*")):
                if yol.is_file():
                    hedef_yol = cikti / "dosyalar" / yol.relative_to(klasor)
                    hedef_yol.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(yol, hedef_yol)
    print(f"tamam: {len(liste)} senaryo -> {hedef}")
    return len(liste)


def farklar(a: Path, b: Path) -> list[str]:
    """İki çıktı klasöründe içeriği farklı ya da yalnız birinde olan dosyalar."""
    c = filecmp.dircmp(a, b)
    sonuc = [str(a / x) for x in c.left_only + c.right_only + c.funny_files]
    sonuc += [
        str(a / x) for x in filecmp.cmpfiles(a, b, c.common_files, shallow=False)[1]
    ]
    for alt in c.common_dirs:
        sonuc += farklar(a / alt, b / alt)
    return sonuc


def deneme() -> None:
    """Bu depoyu iki ayrı süreçte koşar: ağın kendisi belirlenimli olmalı, yoksa taban-baş farkı bir şey kanıtlamaz."""
    with tempfile.TemporaryDirectory(prefix="esdeger-deneme-") as gecici:
        bir, iki = Path(gecici, "1"), Path(gecici, "2")
        for hedef in (bir, iki):
            komut = [sys.executable, "-X", "utf8", __file__, str(DEPO), str(hedef)]
            subprocess.run(komut, check=True)
        fark = farklar(bir, iki)
        assert not fark, fark
        dosya = sum(1 for p in bir.rglob("*") if p.is_file())
        print(f"deneme: iki koşu aynı ({dosya} dosya)")


if __name__ == "__main__":
    if sys.argv[1:] == ["--deneme"]:
        deneme()
    elif len(sys.argv) == 3:
        kos(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
    else:
        raise SystemExit(__doc__)
