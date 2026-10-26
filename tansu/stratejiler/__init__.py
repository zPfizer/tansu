"""Kayıtlı stratejiler (SPEC 4)."""

from tansu.stratejiler import gartley

STRATEJILER = {s.ad: s for s in (gartley.STRATEJI,)}
