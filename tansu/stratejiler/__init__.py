"""Kayıtlı stratejiler (SPEC 4)."""

from tansu.stratejiler import gartley, ortalama_kesisim

STRATEJILER = {s.ad: s for s in (gartley.STRATEJI, ortalama_kesisim.STRATEJI)}
