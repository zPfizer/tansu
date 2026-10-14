# 07: Kodun TASARIM'dan saptığı yerler karara bağlanır

**What to build:** Kodun TASARIM'dan farklı davrandığı on yer tek tek incelenir. Her biri için ya kod TASARIM'a uyar ya da
TASARIM gerekçesiyle güncellenir.

**Blocked by:** 03

**Status:** ready-for-agent

- [ ] `denetim/tasarim-kod.md` §3'ün her maddesi `/diagnosing-bugs` ile ele alındı: davranışı gösteren test, sonra karar.
- [ ] Öncelik: `gunluk.py` yalnız AKTİF kartları indirir (STOP/BOZULDU açık pozisyon izlenmeyebilir).
- [ ] Kod değişikliği gerektiren her madde kendi PR'ıyla kapandı; belge değişikliği TASARIM'da karar etiketiyle.
- [ ] Bilet 06'da bulunanlar (10.10): `motor.sinama` tek satırlı üyelik tablosunda düşer (`groupby(...).agg(pd.DatetimeIndex)` tek günde Timestamp döndürür, `isin` TypeError); `rapor.py` aynı koşu kimliğinde HTML ve CSV'yi üstüne yazar (TASARIM §6.8 "üstüne yazılmaz").
- [ ] Bilet 02'den (10.10, `denetim/tansu-sapma-dogrulama.md` #6, #19): kart etiketi `BOZULDU` Tansu'nun "bozulma"sı (formasyonun geçersizleşmesi) değildir. SMA250 çıkışı, karantina çıkışı ve giriş iptali tek etikette toplanıyor; ayrı etiket (ör. `GÜN SONU STOPU`, `KARANTİNA ÇIKIŞI`, `GİRİŞ İPTAL`) ve `Durum` sütununun `Pozisyon durumu` olması karara bağlanır. Etiket CSV çıktısını değiştirir: önce test.

## Rapor aynı koşu kimliğinde öncekinin üstüne yazar (TASARIM 6.8)

- [ ] Bilet 06'dan taşınan HTML ve CSV regresyonlarını test dosyasına geri koy; kod sapmasını düzeltip ikisini yeşile geçir.

## Comments

10.10: Orkestratör kararıyla iki kırmızı vaka bilet 06 dalından buraya taşındı. Üretim kodu değiştirilmedi.
Kaynak: `tests/test_simulator.py:73–92`. Aşağıdaki parametrik test aynen korunmuştur; mevcut
`kos`, `sinyalli`, `mum` yardımcılarını kullanır. Geri koyarken `from tansu import ...` satırına `rapor` eklenir.

```python
@pytest.mark.parametrize("dosya", ["rapor", "csv"])
def test_rapor_ayni_kosu_kimliginde_onceki_dosyanin_ustune_yazmaz(tmp_path, dosya):
    # TASARIM 6.8: ikinci yazım reddedilebilir ya da yeni dosya kullanabilir; ilki değişmez.
    _, ilk = kos(tmp_path / "ilk", {"A": sinyalli()})
    yol = ilk[dosya]
    once = yol.read_bytes()
    fiyat = sinyalli()
    fiyat[-1] = mum(pd.Timestamp("2026-02-04"), 106, 106.5, 105.5)
    kimlik, ikinci = kos(tmp_path / "ikinci", {"A": fiyat})
    # İki boş işlem listesi sahte yeşil vermez.
    assert ikinci[dosya].read_bytes() != once
    try:
        rapor.yaz(
            ikinci["sim"],
            {"kosu_id": ilk["kosu_id"], "anlik": kimlik, "kod_hash": "abc123"},
            cift=ikinci["cift"],
        )
    except FileExistsError:
        pass  # Aynı kimlikte yazımı reddetmek sözleşmeye uygundur; dosya yine denetlenir.
    assert yol.read_bytes() == once
```

Kırmızı kanıt (taşımadan önce bu koşuda yeniden doğrulandı):

```bash
.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=.codex-tmp tests/test_simulator.py -k rapor_ayni --tb=short
```

Çıkış 1; iki vaka da `assert yol.read_bytes() == once` satırında kırıldı:

```text
FAILED tests/test_simulator.py::test_rapor_ayni_kosu_kimliginde_onceki_dosyanin_ustune_yazmaz[rapor]
FAILED tests/test_simulator.py::test_rapor_ayni_kosu_kimliginde_onceki_dosyanin_ustune_yazmaz[csv]
2 failed, 18 deselected in 1.07s
```

HTML bayt 437'de, CSV bayt 188'de değişti. Bu testlerin 06'dan çıkarılması hatayı düzeltmez; yeşil kanıt bu bilettedir.

2026-10-14 (bilet 05, denetim tur 1): üretici dosyalar belgeyi eski metinle yeniden yazar; ikisi bu bilette düzeltilir.
- `tansu/denetim.py:281–288` `docs/denetim.md`'yi yeniden üretir ve eski yanlış kabul cümlesini yazar ("ölçüt 1–4 geçen oran ... Kâğıt bunun alt kümesidir"). Cümle TASARIM 5.12 tanımıyla eşleşmeli (ölçüt 1–4 Geçti ve portföy kuralı reddetmedi) ya da yalnız TASARIM 5.12'ye atıf vermeli. `docs/denetim.md` bilet 05'te elle düzeltildi; yeniden koşu bu düzeltmeyi siler.
- `tansu/sadakat.py:258–283` `docs/sadakat.md`'yi yeniden üretir. Çıktı, KURALLAR §4'teki eşdeğer aday tanımını (aynı dönem ve gün, ölçülen değerler ±0,005 içinde) ve EMA için seçilen adayı göstermeli; ayrıca sayfa başındaki "Getiriye bakılmaz." cümlesi (satır 3) KURALLAR §4'e atıf olmalı. `docs/sadakat.md` elle düzenlenmedi.

07a (14.10): kod metin dilimi kapandı (`pr/07a-kod-metin`). Kapanan: (1) `denetim.py` yanlış kabul cümlesi `docs/denetim.md` metniyle aynı (TASARIM 5.12 atfı, "ölçüt 1–4 Geçti ve portföy kuralı reddetmedi"); (2) `sadakat.py` çıktısı 3. satırda KURALLAR §4'e atıf verir, "Eşdeğer adaylar" bölümü kuralı (±0,005) ve seçilen EMA adayını yazar; (3) `gunluk.py` `_kanit` "sepete göre"; (4) CSV başlıkları ASCII (`tarih` … `kaynak`), `kayit/kartlar.jsonl` yeni satırlarda yeni anahtar, okuyucu eski büyük harfli anahtarı da okur (`_alan`); (5) Kaynak hücresi "Tansu'dan esinlenen yorum · İş Yatırım <kimlik>"; (6) `kayit._yaz` ve `sadakat.calistir` her yeni deneme günlüğü satırına `sema: 1` yazar. Kalan (kutular işaretlenmedi): bu biletin diğer maddeleri, `kayit.py` hash kapsamında olduğu için kod hash'i değişti: resmi koşudan önce `denetim` yeniden koşulmalı.
