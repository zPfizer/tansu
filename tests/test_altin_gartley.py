"""Altın test: Tansu'nun SOKE Gartley taraması, yerel veriyle (SPEC 10, çatışma 9 toleransı)."""

from pathlib import Path

import pandas as pd
import pytest

from tansu import veri
from tansu.__main__ import son_anlik
from tansu.stratejiler import gartley

ALTIN = Path("tests/altin/gartley.csv")
VERI = Path("veri")
TOLERANS = 0.01  # yfinance ile İş Yatırım farkı için göreli pay


def test_soke_gartley_seviyeleri_yerel_veride_bulunur():
    if not ALTIN.exists() or not list((VERI / "ag").glob("2*")):
        pytest.skip("yerel altın olgu veya veri yok")
    olgu = pd.read_csv(ALTIN).set_index("nokta")["fiyat"]
    gonderi = pd.Timestamp(pd.read_csv(ALTIN)["gonderi_tarihi"].iloc[0])
    gun = veri.gunluk(son_anlik(VERI), "SOKE")
    s = gartley.STRATEJI.sinyal(gun, {"rr_min": "kapali"})  # seviye olgusu; kapı ayrı
    once = s[s["giris"] & (s.index <= gonderi)]
    assert len(once), "gönderi tarihine kadar SOKE kurulumu yok"
    r = once.iloc[-1]
    x = float(r["kural_durumu"].split("X ")[1].split(" ")[0])
    a = float(r["kural_durumu"].split("A ")[1].split(" ")[0])
    assert x == pytest.approx(olgu["X"], rel=TOLERANS)
    assert a == pytest.approx(olgu["A"], rel=TOLERANS)
    assert olgu["D"] * (1 - TOLERANS) <= r["seviye"] <= olgu["0.786"] * (1 + TOLERANS)
    assert r["stop"] == pytest.approx(x)
    assert r["durum"] == "AKTIF"
