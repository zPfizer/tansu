# 09: Belgeler bugünkü kodu ve durumu anlatır (uygunluk denetimi 14.10)

**What to build:** YONETIM uygunluk denetiminin (14.10, `YONETIM/.scratch/tansu-uygunluk-1410/`) doğrulanan bulguları
giderilir. TASARIM §7 ve §4 kodla eşlenir; bilet 02 durumu commit'e uyar; AGENTS görev metni ve KURALLAR havuz sayısı
bugünü anlatır; "hafta içi 19:30" tek sahibe (TASARIM §6) atıf olur.

**Blocked by:** None (can start immediately)

**Status:** done (pr/09-uygunluk-1410)

- [x] TASARIM §7: adım 2–9 ilgili MVP biletiyle "tamamlandı"; adım 10 bilet 16 sonucuna atıf. §6 "`evren-indir` elle yapılır" satırı `TansuAylik` görevine uyar.
- [x] TASARIM §4: `__main__` satırı koddaki 7 komutu sayar; `sadakat` satırı var; bölüm→kod tablosunda §3 satırı var. `tansu/__main__.py` docstring aynı 7 komutu sayar.
- [x] Bilet 02 `Status: done (PR #5, ce0fe60)`.
- [x] AGENTS "Task Scheduler": iki görev kurulu ve etkin (bilet 15, 06.10); saat için TASARIM §6'ya atıf; kapalı kurulum ve "bilet 15'te etkinleştir" metni yok. XML açıklamalarındaki "etkinleştirme bilet 15" notu kalkar.
- [x] KURALLAR satır 3 havuz sayısı 14.10 sayımı: 258 not, 228 görsel (63 jpg, 145 png, 19 webp, 1 pdf).
- [x] Test kapısı yeşil; `tests/test_standartlar.py` dahil.

Dışarıda bırakılan (gerekçe): `test_gelecek` ve değişmez kural satırları CODING_STANDARDS'ta kural, DoD'de kanıt maddesidir; çift kayıt değil.
Bilet 02'nin kutuları madde madde doğrulanmadı; kanıt `denetim/tansu-sapma-dogrulama.md`.
