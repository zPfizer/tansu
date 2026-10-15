# 07: Kodun TASARIM'dan saptığı yerler karara bağlanır

**What to build:** Kodun TASARIM'dan farklı davrandığı on yer tek tek incelenir. Her biri için ya kod TASARIM'a uyar ya da
TASARIM gerekçesiyle güncellenir.

**Blocked by:** 03

**Status:** done (PR #18, 961902f)

Alt biletler 07a–07e PR #13–#17 ile birleşti; son kapanış PR #18 (07f). (16.10)

- [x] `denetim/tasarim-kod.md` §3'ün her maddesi `/diagnosing-bugs` ile ele alındı: davranışı gösteren test, sonra karar.
- [x] Öncelik: `gunluk.py` yalnız AKTİF kartları indirir (STOP/BOZULDU açık pozisyon izlenmeyebilir).
- [x] Kod değişikliği gerektiren her madde kendi PR'ıyla kapandı; belge değişikliği TASARIM'da karar etiketiyle.
- [x] Bilet 06'da bulunanlar (10.10): `motor.sinama` tek satırlı üyelik tablosunda düşer (`groupby(...).agg(pd.DatetimeIndex)` tek günde Timestamp döndürür, `isin` TypeError); `rapor.py` aynı koşu kimliğinde HTML ve CSV'yi üstüne yazar (TASARIM §6.8 "üstüne yazılmaz").
- [x] Bilet 02'den (10.10, `denetim/tansu-sapma-dogrulama.md` #6, #19): kart etiketi `BOZULDU` Tansu'nun "bozulma"sı (formasyonun geçersizleşmesi) değildir. SMA250 çıkışı, karantina çıkışı ve giriş iptali tek etikette toplanıyor; ayrı etiket (ör. `GÜN SONU STOPU`, `KARANTİNA ÇIKIŞI`, `GİRİŞ İPTAL`) ve `Durum` sütununun `Pozisyon durumu` olması karara bağlanır. Etiket CSV çıktısını değiştirir: önce test.

## Rapor aynı koşu kimliğinde öncekinin üstüne yazar (TASARIM 6.8)

- [x] Bilet 06'dan taşınan HTML ve CSV regresyonlarını test dosyasına geri koy; kod sapmasını düzeltip ikisini yeşile geçir.

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

07a (14.10), denetim tur 1 düzeltmesi: (a) özel yardımcıları çağıran iki test kaldırıldı; yerine açık arayüzden giden `test_dunku_acik_kart_hissesi_eski_ve_yeni_anahtarla_bugun_de_indirilir` (`gunluk.gunluk`, eski ve yeni anahtarlı `kartlar.jsonl`) ve `test_rapor_*` (`sadakat.rapor_metni`) yazıldı. (b) Aday seçimi KURALLAR §4 "Tansu'nun rakamını en iyi üreten seçilir" ile hizalandı: eşdeğerlik (±0,005) yalnız kaç aday sayıldığını belirler (bir); temsilci, ölçülen değerlerin Tansu rakamından mutlak fark toplamı en küçük olan adaydır; eşitlikte ilk aday ("(eşitlikte ilk aday)" üretilen metinde yazar). KURALLAR §4'e eklendi (KURALLAR §4, commit c0ebea7; bilet 04 birleşti; "Tansu'nun rakamını en iyi üreten seçilir" cümlesinin sonuna): "En iyi: ölçülen değerlerin Tansu'nun rakamlarından mutlak farklarının toplamı en küçük olan aday; eşitlikte aday sırasındaki ilk aday (bilet 07a, 14.10)."
Kanıt, kırmızı koşu (ilk commit 25ce53d'den önce, dört dosyada `python -m pytest -q --no-header tests/test_denetim.py tests/test_gunluk.py tests/test_kayit.py tests/test_sadakat.py`): `15 failed, 41 passed`. Hata iletileri: `AssertionError: assert ('(ölçüt 1–4 Geçti ve portföy kuralı reddetmedi)' in ...` (test_denetim.py:165); `assert [['Tarih', 'H...hmini)', ...]] == [['tarih', 'h...hmini)', ...]]` (test_gunluk.py:130); `assert ['Tarih;Hisse...Kanıt;Kaynak'] == ['tarih;hisse...kanit;kaynak']` (test_gunluk.py:157); `KeyError: 'hisse'` (test_gunluk.py:173, 364); `KeyError: 'Durum'` (gunluk.py:198); `KeyError: 'sema'` (test_kayit.py:299, test_sadakat.py:57); `AttributeError: module 'tansu.sadakat' has no attribute '_esdeger_bolumu'` (test_sadakat.py:167, 182); `AssertionError: assert False` (test_sadakat.py:192). Yeşil koşu: `python -m pytest -q --no-header` tam takım, `315 passed` (ilk commit); tur 1 düzeltmesinden sonra `317 passed`, `tests/test_gelecek.py` ayrıca `18 passed`. Dosyalar adıyla eklendi (`git add` ile, `-A` ve `.` kullanılmadı): `tansu/denetim.py`, `tansu/sadakat.py`, `tansu/gunluk.py`, `tansu/kayit.py`, `tests/test_denetim.py`, `tests/test_gunluk.py`, `tests/test_kayit.py`, `tests/test_sadakat.py`, `.scratch/belge-hizasi/issues/07-kod-sapmalari.md`.

2026-10-15 (07b): rapor üstüne yazma ve `motor.sinama` tek günlük üyelik kapandı.
- Kırmızı (düzeltmeden önce): `test_simulator.py -k rapor_ayni` 2 failed (HTML ve CSV `assert yol.read_bytes() == once`); `test_motor.py::test_sinama_uyelik_tablosunda_tek_gunluk_ve_iki_gunluk_sembol[uye_gunleri0]` TypeError "only list-like objects are allowed to be passed to isin(), you passed a `Timestamp`"; iki günlük vaka yeşil.
- Düzeltme: `tansu/rapor.py:325-330` ikinci yazım `FileExistsError` verir (HTML, CSV, çift CSV; dosyaya dokunmadan önce); `tansu/motor.py:237` `agg(list)`.
- Yeşil: `4 passed` (iki rapor vakası, iki üyelik vakası); tam kapı `314 passed`; `test_gelecek.py` ve `test_standartlar.py` `21 passed`; ruff check ve format temiz.
- Hazırlanan dosyalar: `tansu/motor.py`, `tansu/rapor.py`, `tests/test_motor.py`, `tests/test_simulator.py`, `.scratch/belge-hizasi/issues/07-kod-sapmalari.md`.
- 07b ek (kök neden, tüm çağıranlar): `tansu/istatistik.py:35` ve `tansu/saglamlik.py:52` `agg(list)`.
- Kırmızı: `test_saglamlik.py::test_ema_izgarasi_tek_gunluk_ve_iki_gunluk_uyelik_sinyal_gunu_alinir[gunler0]` ve `test_istatistik.py::test_ema_k1_tek_gunluk_ve_iki_gunluk_uyelik_sinyal_gunu_gercege_girer[gunler0]` aynı TypeError ("only list-like objects ... you passed a `Timestamp`"); iki günlük vakalar yeşil.
- İstatistik tarafında tek gün düzeltmeden sonra tasarlanmış `K1Hatasi` verir (tür (b): ±20 günde başka uygun gün yok, TASARIM 5.7 "sessizce kırpılmaz"); test bu yüzden ikiye bölündü: `test_ema_k1_iki_gunluk_uyelik_sinyal_gunu_gercege_girer` ve `test_ema_k1_tek_gunluk_uyelik_typeerror_degil_k1_hatasi_verir`.
- Yeşil: saglamlik iki vaka (işlem 1, fazla 0,0465108), istatistik iki test; tam kapı `318 passed`; `test_gelecek.py` ve `test_standartlar.py` `21 passed`; ruff temiz.
- Ek dosyalar: `tansu/istatistik.py`, `tansu/saglamlik.py`, `tests/test_istatistik.py`, `tests/test_saglamlik.py`.

07d (15.10): istatistik ve kayıt dilimi (`pr/07d-istatistik-kayit`), beş madde ve iki karar uygulandı (sorular vekil kararıyla kapandı, Threads 64).
- e-3 düzeltildi, `tansu/simulator.py:_yillik`: `fazla` artık günlük (kural − K2) getirilerin yıllık toplamı (TASARIM 5.8); `kural` ve `k2` bilgi sütunu olarak yıl sonu getirisi kalır. Test `test_simulator.py::test_yillik_fazla_getiri_gunluk_fazla_getirilerin_yillik_toplamidir`. Kırmızı: `Obtained: -0.0006121681203590246 Expected: -0.00061197 ± 2.0e-09`. Yeşil: geçti.
- e-5 ve `deneme_sayisi` düzeltildi, `tansu/kayit.py`: m tek yerde (`_yarim_ciftler` + `_ilk_p`): resmi koşuların (kural_id, aile) çiftleri, yarıda kalan resmi koşu dahil (iki aile), geliştirme koşusu hariç. `deneme_sayisi`, `tekrar_sayisi` (B) ve `holm_hesapla` (holm_m) aynı kümeyi kullanır; yarım çiftin p'si yok, Holm listesinde p = 1 sayılır (aşağıda soru 2). Testler `test_kayit.py::test_gelistirme_kosusu_deneme_sayisina_girmez` (kırmızı `assert 2 == 0`), `test_kayit.py::test_yarida_kalan_resmi_kosu_m_ye_girer_ve_deneme_sayisi_B_ve_holm_ayni_m_yi_kullanir` (kırmızı `assert 3 == 6`). Yeşil: geçti.
- resmi tekrar=0 düzeltildi, `tansu/kayit.py:kosu`: koşul `resmi and tekrar < tekrar_sayisi(...)` (0 < kalktı). Test `test_kayit.py::test_resmi_kosu_tekrar_0_ile_reddedilir_gunluge_satir_yazmaz` (kırmızı `DID NOT RAISE KayitHatasi`); günlüğe satır yazılmaz. Yeşil: geçti.
- Eski beklenti değişti (belge açık: TASARIM 5.11): `test_kosu_k1.py` yarıda kalan resmi koşu `deneme_sayisi() == 2` (1 idi; iki aile), geliştirme koşulu test `== 0` (1 idi); `test_kayit.py::test_temiz_agacta_resmi_kirli_agacta_resmi_degil` resmi koşuya tam tekrar verir (eskiden tekrar=0 boşluğundan geçiyordu).
- Kayıtlı sayı etkisi yok: günlükte yarıda kalan resmi koşu yok, resmi `bitti` koşusu tam tekrarlı; geçmiş satırlara dokunulmadı. Kod hash'i değişti (`kayit.py`, `simulator.py` hash kapsamında): kod hash değişti; `kayitla` gerekir; `denetim` yalnız tamamlanmış resmi koşu yoksa gerekir (TASARIM 5.12, `_resmi_bitti`).
- Hazırlanan dosyalar: `tansu/kayit.py`, `tansu/simulator.py`, `tests/test_kayit.py`, `tests/test_kosu_k1.py`, `tests/test_simulator.py`, `.scratch/belge-hizasi/issues/07-kod-sapmalari.md`.
- Karar 1 (vekil 15.10), NaN gerçek istatistik: p = 1 kalır, koşu durmaz; `bitti` günlük satırına yalnız yeni satırlarda `uyari: "istatistik NaN"` yazılır, rapor "Uyarı: istatistik NaN; p = 1 alındı." gösterir. TASARIM 5.7 "p değeri" listesine eklendi (önce belge). Kod: `tansu/kayit.py:kosu` (uyari), `tansu/rapor.py:_kabul`. Test `test_kosu_k1.py::test_gercek_istatistik_nan_ise_p_bir_gunluk_satiri_uyari_yazar_rapor_gosterir`. Kırmızı: `KeyError: 'uyari'` (p = 1 iddiası zaten geçiyordu). Yeşil: geçti.
- Karar 2 (vekil 15.10), yarım resmi koşu Holm'da p = 1: TASARIM 5.11 "Deneme sayısı (m), tek tanım" maddesine eklendi. Kod 07d'nin ilk commit'inde (`kayit._yarim_ciftler`, `holm_hesapla`); testi `test_kayit.py::test_yarida_kalan_resmi_kosu_m_ye_girer_ve_deneme_sayisi_B_ve_holm_ayni_m_yi_kullanir` (holm_m 6, holm_p 0,06) karşılar.
- Karar 3 (vekil 15.10), rastgele tekrarda NaN: TASARIM 5.7 sessizdi; muhafazakâr sayım seçildi, 5.7 "p değeri" listesine cümle eklendi. Kod `tansu/istatistik.py:p_deger` (`isnan | r >= gercek`). Test `test_istatistik.py::test_rastgele_tekrarda_nan_gercege_esit_ya_da_iyi_sayilir`, elle: gerçek 0,3, tekrarlar [NaN; 0,5; 0,1], k = 2, p = 3/4. Kırmızı: `assert 0.5 == 0.75`. Yeşil: geçti.
- Beklenti değişti (karar 3): `test_istatistik.py::test_ek_kol_ailenin_p_degerine_girmez` `p_b` 1/21 → 6/21 (5 NaN tekrar artık iyi sayılır; eski sayım NaN'ı kötü sayıp k = 0 veriyordu). Kayıtlı sayıya etkisi: günlükteki üç resmi `bitti` koşusunun p'leri yeniden hesaplanmadı; NaN tekrar içeren bir koşu varsa yeni p daha yüksek çıkar, bu yeni deneme sayılır, eski satır yeniden yazılmaz.
- Denetim tur 1 (Codex, KALDI) düzeltmeleri: (1) `tests/test_gelecek.py::test_t_den_sonrasi_veri_t_oncesi_ciktiyi_degistirmez[yillik_fazla_-*]` (3 kesim; `motor.sinama` + `simulator.calistir` arayüzü, t'den önce biten yılların `yillik` satırı kesilmiş ve tam veride aynı); test_gelecek `21 passed` (18 idi). (2) Sıra ihlali: kod ea84c50'de, cümle 89cfe84'te; sıra ihlali kaydedildi. Kural şimdi TASARIM 5.11 "Deneme sayısı (m), tek tanım" maddesinin son cümlesindedir ("Yarıda kalan resmi koşunun (kural kimliği, aile) çifti Holm listesinde p = 1 ile yer alır; ..."). (3) `test_kayit.py` `kural_id`'yi herkese açık `kayitla()` çıktısından alır. (4) Yukarıdaki `denetim` cümlesi sahip belgeye (TASARIM 5.12) uydurularak düzeltildi; kapı değişmedi.
- Denetim tur 3 (Codex, KALDI), tek madde: test dördüncü kesim günü (2014-12-31) ekledi, TASARIM 5.12 üç kesim sayıyordu.
  AKIS gereği dördüncü tur yok; iş 07d-b olarak yeniden tanımlandı. Kök neden: test kapsamı değişti, sahibi belge güncellenmedi.
  Düzeltme: TASARIM 5.12 dört kesim gününü sayar (bilet 07d, 15.10). Yeni denetim tur 1.
07c (15.10): kart dilimi (`pr/07c-kartlar`; vekil kararları 15.10, Threads 64). Önce belge: TASARIM 6.2 (dünkü her kartın hissesi indirilir), 6.6 (Durum: beş etiket, eski kayıtta BOZULDU), GLOSSARY "Kart durumu". (1) `_acik_hisseler` AKTİF süzgecini kaldırdı. (2) `_durum` BOZULDU yerine `GÜN SONU STOPU` / `KARANTİNA ÇIKIŞI` / `GİRİŞ İPTAL` yazar (`ETIKET` sözlüğü); `durum` sütun adı ve STOP aynen; eski `BOZULDU` satırları hâlâ okunur (test). (3) `_temizle` yalnız `_gecici*` klasörlerini siler; `SAKLA_GUN` ve 30 gün silmesi kalktı (TASARIM bilet 03'te değişmişti: 5.11 silme yasağı).
Testler (`tests/test_gunluk.py`): `test_dunku_kartin_hissesi_durumundan_bagimsiz_indirilir` (5 etiket, eski BOZULDU dahil), `test_dunku_acik_kart_hissesi_eski_ve_yeni_anahtarla_bugun_de_indirilir` (STOP kartın hissesi artık istenir; eski beklenti "YYYY istenmez" eski kuraldı, TASARIM 6.2 değişince yeni kurala çevrildi, `WWWW` eski satırın geçersiz kılındığını korur), `test_kart_durumlari_ve_kapanan_kart_yalniz_kapandigi_gun_gorunur[sma250|giris_iptali|karantina]` (CSV hücre değerleri yeni etiket), `test_gunluk_anlik_goruntuler_yaslari_ne_olursa_olsun_silinmez` (eski `..._30_gun_sonra_silinir_...` testi bu kuralla değiştirildi: gerekçe TASARIM 5.11/6.2, bilet 03).
Kırmızı: `python -m pytest -q tests/test_gunluk.py` -> `11 failed, 13 passed` (ör. `assert 'YYYY' in ['XXXX']`). Yeşil: aynı komut sonra tam takım `322 passed`; `test_gelecek` + `test_standartlar` `21 passed`; ruff check ve format --check temiz.
Dosyalar: `docs/TASARIM.md`, `GLOSSARY.md`, `tansu/gunluk.py`, `tests/test_gunluk.py`, bu bilet. Açık kalan: "Bilet 02'den ... BOZULDU" kutusu işaretlenmedi; `Durum` sütununun `Pozisyon durumu` adı alıp almayacağı yazılı karar değil (sütun adı `durum` kaldı). `kod_hash` değişmedi (denetim tur 1, 15.10: `gunluk.py` hash dışıdır, taban ve uç hash aynı); 07c için `denetim` yeniden koşusu gerekmez.
- 07c (15.10) karar: sütun adı `durum` kalır (vekil kararı 15.10, Threads 64: ASCII ad zaten var; yeniden adlandırma ikinci bir değişiklik eklerdi). Üç etiket TASARIM 6.6 ve GLOSSARY'de; kutu kapandı.
- 07c denetim tur 1 (Codex, 15.10): KALDI (GLOSSARY satırında karar etiketi yoktu; hash/yeniden koşu iddiası yanlıştı). İkisi düzeltildi.
- 07c denetim tur 2 (15.10): Codex sanal alanı üç denemede açılmadı (CreateProcessWithLogonW 1909); AKIS küçük fark kuralıyla bağımsız denetçi Sonnet alt ajanı: GEÇTİ (iki dosya, kod yok; HASH_DISI'de gunluk.py doğrulandı).
- 07d-b denetim tur 1 (Codex, KALDI): iki bulgu 07c'nin dalda olmamasıydı; master birleştirildi (e326319). Tur 2 (Codex, KALDI): rapor
  metni "yıllık kural − yıllık K2" diyordu, hesap TASARIM 5.8 (günlük farkların yıllık toplamı). Önce kırmızı test
  (`test_simulator.py::test_rapor_baslik_...`), sonra `rapor.py` cümlesi düzeltildi. Yeni tur 3.
- 07d-b denetim tur 3 (Codex, KALDI): `kayit.py:221` `tekrar_sayisi` açıklaması m'yi eski tanımla (yarım koşu hariç) anlatıyordu.
  Yeniden tanım 07d-c. Kök neden: hesap güncellenirken düzyazı (docstring, rapor metni) taranmadı. Düzeltme: açıklama sahip
  cümleye (TASARIM 5.11) bağlandı; `kayit.py`, `istatistik.py`, `simulator.py`, `rapor.py` formül anlatan düzyazısı tarandı, başka eski cümle yok.

07e (15.10): veri/motor dilimi (`pr/07e-veri-motor`, worktree `TANSU-b07e`).
- (1) `__main__` ağ yolu: kırmızı `test_sirket_kodlari_...` AttributeError (`kaynak` has no attribute 'sirket_kodlari') ve `test_evren_indir_ag_icin_yalniz_kaynagi_kullanir_...` aynı hata. Yeşil: `kaynak.sirket_kodlari()` (ince sarmalayıcı), `__main__._evren_indir` onu çağırır; borsapy.companies doğrudan çağrılırsa test düşer.
- (2) Limit baz fiyatı: bayat sapma. `veri._gunler` önceki temiz kapanışı alır ama "temiz" yalnız işlem günü ve satır tutarlı demektir; limit aşımı karantinası (`asim`) baz fiyatı dışlamaz. Yani karantinalı gün baz olur (TASARIM 5.1 ile aynı). Kod değişmedi; koruyucu test `test_limit_bazi_onceki_gunun_ham_kapanisidir_karantinali_gun_de_baz_olur` ilk koşuda yeşil (kırmızı yok). Bozuk satır: Karar 1.
- (3) Olay eşleştirmesi ±1: `_olay_denetimi` zaten ±1 yapıyordu; `_gunler` (limit, kilit, karantina) yapmıyordu. Kırmızı: `test_olayla_aciklanan_gun_tablo_tarihinin_bir_gun_oncesi_ya_da_sonrasinda_da_karantinaya_girmez[olay_gunu0|1]` iki failed (`[False]*5` yerine karantinalı gün). Yeşil: ortak `veri._olay_konumu`, iki yer de onu kullanır; test tavan 56,1 (elle: 102 × 0,5 × 1,10).
- (4) Giriş günü karantinası: kod değişmedi, Karar 2.
- (5) Piyasa durumu etiketi: kod değişmedi, Karar 3.
- Kapı: pytest `335 passed` (5 yeni test fonksiyonu, biri iki parametreli: 6 yeni vaka), `test_gelecek` + `test_standartlar` `21 passed`, ruff check ve format temiz, `git diff --check` temiz, LF.
- Sayı etkisi: `veri.py` kod hash'ine girer (`kayit.HASH_DISI`'nda yok): kod hash değişti; `kayitla` gerekir; `denetim` yalnız tamamlanmış resmi koşu yoksa gerekir (TASARIM 5.12, `_resmi_bitti`). Karantina ya da kilit, tablo tarihi gerçek adımdan bir gün kaymış olay günlerinde değişebilir (daha önce o gün sahte karantina ya da gün kayması düşüyordu); önceki resmi koşunun rakamları bu yüzden yeni deneme sayılır, üzerine yazma değil.
- Hazırlanan dosyalar: `tansu/__main__.py`, `tansu/kaynak.py`, `tansu/veri.py`, `tests/test_kaynak.py`, `tests/test_veri.py`.
- Karar 1 (vekil, 15.10, Threads 64; seçenek c): TASARIM 5.1 "Fiyat limiti" (satır 228) "Bozuk satır (satır ihlali, 5.13) baz fiyat olmaz; baz, önceki tutarlı işlem gününün ham kapanışıdır." Kod aynı; yeni vaka `test_bozuk_satir_baz_fiyat_olmaz_...` ilk koşuda yeşil (kırmızı yok; d3 tavanı 100 × 1,10 = 110).
- Karar 2 (seçenek a): TASARIM 5.3 "Düşen sinyal" (satır 311) "giriş günü yoksa, kilitli tavansa ya da karantinadaysa sinyal düşer". Kod ve motor testi `karantinada_giris_gunu` aynı.
- Karar 3 (seçenek a): TASARIM 3 (satır 86-87) "K1(b) örneklemesinde kullanılır, çıktıda görünmez"; TASARIM 6 madde 3 (satır 853) "raporda ve kartta görünmez (3, 5.7)". Kod aynı.

07e denetim tur 1 (Codex, 15.10): KALDI. Düzeltmeler: (a) `test_evren_indir_...` artık `main(["evren-indir", "--kok", ...])` ile çağırır (özel işlev yok); (b) GLOSSARY "Düşen sinyal" TASARIM 5.3'e atıf verir (giriş günü karantinası dahil); (c) TASARIM.md satır 117 "borsapy (yalnız faiz, sektör ve şirket listesi)"; commit 153ec97.
07e-4 (karar, vekil 15.10, Threads 64; seçenek 1, asimetrik pencere): denetçi ±1 eşleştirmenin önek değişmezliğini (5.12) bozduğunu gösterdi (t+1 tarihli olay t günü karantinasını kaldırır). Önce belge: TASARIM 5.1 karantina maddesi (satır 251–255) pencere t−1..t, t+1 tarihli olay açıklamaz; veri katmanı maddesi (222) ±1'i yalnız olay denetimi istatistiğine bağlar; `docs/sorgu/izleme/karar.md` (yerel) 02-024 daraltma satırı. Kod: `veri._olay_konumu(..., kayma=(0, 1))` `_gunler`te; `_olay_denetimi` ±1 kalır.
- Tur 2 (Codex, 15.10): KALDI. TASARIM 5.12 kesim günü t dahil önek eşitliği ister; "en yakın aday" t tarihli olay için t+1 verisi gerektirir (BOLUNME 04.01: tam/kesik karantina yok/var, tavan 111,1/55,55). Karar 07e-4 aynı, tam önek değişmez yapıldı: aday seçimi kalktı, gün başına kural (TASARIM 5.1 satır 251–256): t günündeki adım, tablo tarihi t−1 ya da t olan olayla açıklanır; adım = günün ham kapanışının önceki işlem gününe oranı olay çarpanına 1'den (logaritmik) daha yakın. Adım olmayan gün çarpan almaz. Kod: `_gunler` her olay için t ve t+1 günlerine bakar; `_olay_konumu` yalnız olay denetiminde (±1).
- Kırmızı (4a1a90a'da, kesim günü dahil karşılaştırma): `test_olay_penceresi_onek_degismez_...[ham0|ham1]` `AssertionError: Timestamp('2024-01-04 00:00:00')`, `assert [False, False, True] == [False, False, False]`; `test_adimi_t_eksi_1_...` tavan 04.01 `111,1` beklenir, 55,55.
- Yeşil (eller): olay 04.01 ya da 05.01, adım 05.01: 04.01 oran 102/101 adım değil, baz 101, tavan 111,1, temiz; 05.01 oran 51/102 = 0,5 adım, baz 51, tavan 56,1. Olay 08.01 (t+1): 05.01 taban 102 × 0,9 = 91,8, 51 altında: karantina; 08.01 oran 52/51 adım değil, temiz: `[F,F,F,T,F]`. Adım 03.01 [100, 51, 52], olay 04.01: 03.01 karantina (taban 90), 04.01 adım değil, baz 51, temiz: `[F,T,F]`; her kesimde kesik = tam, kesim günü dahil. Tam kapı `340 passed`, `test_gelecek` + `test_standartlar` `24 passed`, ruff temiz.
- Sonuç: olay tablosu tarihli ama fiyat adımı göstermeyen gün çarpan almaz (TASARIM 5.1'in o günkü "olay günü baz fiyat" cümlesi adım günü için okunur; `test_olay_gunu_tabani_carpanla_olcekli` adım içerir, yeşil).
- Bedel (karar.md): yalnız t+1 tarihli olayla açıklanan adım karantinada kalır; olay tablosu tarihi düzeltilirse çözülür.
- Denetim tur 3 (Codex, KALDI, 15.10): `veri.py` adım tespiti önceki tutarlı kapanışı kullanır, TASARIM 5.1'in o günkü metni "önceki işlem günü" der. Yeniden tanım 07e-b; kök neden: limit bazı süzgeci adım tespitinde belgesiz kullanıldı. Düzeltme: TASARIM 5.1 adım cümlesi önceki tutarlı kapanış (bozuk satırlar limit bazındaki gibi atlanır, 5.13; satır 254). Kod aynı. Test `test_adim_orani_onceki_tutarli_kapanisa_bakar_bozuk_satir_atlanir` fb11a77 kodunda ilk koşuda yeşil (belge değişti, kod değil): kapanışlar [100, 50, 50], 2. gün bozuk, olay çarpanı 0,5 üçüncü günde: oran 50/100 = 0,5 adım, baz 50, taban 45, karantina `[F,T,F]`.

07f (15.10): hash kapsamı dilimi (`pr/07f-hash-kapsami`, worktree `TANSU-b07f`); §3'ün son maddesi (`MASRAFLAR`, `K1_MASRAF`, `GELISTIRME` hash'e girer, TASARIM hash dışı sayar).
- Karar (vekil, 15.10, seçenek 1, yalnız belge): sabitler hash'te kalır; p değerini ya da kabul kararını değiştirirler (`kayit._kabul` 0,003 ve 0,005 masraf anahtarlarını okur ve `istatistik.kabul`'a verir; `K1_MASRAF` `ema_k1`/`cift_k1` varsayılan masrafı ve `GIDIS_DONUS`'tur; B sabitleri p paydasını belirler). TASARIM 5.8 "Kural kaydı" altındaki "Hash dışı" maddesi ve "İki not" cümlesi koda hizalandı. Kodda doğrulama: blok uzunluğu günlükte alan değil, `istatistik.blok_uzunlugu(tutma)` çıktısıdır; metin buna göre yazıldı (tekrar ve tohum günlükte alandır).
- Dosyalar: `docs/TASARIM.md`, `tests/test_kayit.py`, bu bilet. Başka belgede (GLOSSARY, KURALLAR, `tansu/*.py` düzyazısı) masraf ya da tekrar için "hash dışı" cümlesi yok; KURALLAR/TASARIM "masraf senaryoları deneme sayısına girmez" Holm m ile ilgilidir, hash ile değil.
- Test: `test_kayit.py::test_masraf_sabiti_degisince_kod_hashi_degisir[MASRAFLAR|K1_MASRAF|GELISTIRME|TAM_TABAN|TAM_CARPAN]` (tmp paket kopyasında sabit değişince açık yüz `kayit.kayitla`'nın `kod_hash` ve `kural_id` değeri değişir). Mevcut davranışı sabitler: ilk koşuda yeşil, kırmızı yok. Denetim tur 1 (KALDI) düzeltmesi: özel `_kural` yerine `kayitla`; B sabitleri için üç vaka eklendi. Mutasyon kanıtı (geçici kopyada `_kural` B demetini hash'ten çıkarır, repo dosyası değişmedi): `3 failed, 2 passed`; `FAILED ...[GELISTIRME]`, `[TAM_TABAN]`, `[TAM_CARPAN]`, hepsi `assert '057cc7df...' != '057cc7df...'`. Yorum/boşluk testi `test_kod_hashi_yorum_ve_bosluktan_etkilenmez` değişmedi.
- Kod hash'i değişmedi; kayitla ihtiyacı önceki değişikliklerden sürüyor (07d, 07e).
- Kutu: "§3'ün her maddesi" işaretlendi. "Her kod maddesi kendi PR'ıyla" da işaretlendi (orkestratör, 15.10): kutunun amacı kod değişikliğinin başka işe karışmadan PR'la kapanmasıdır; 07a–07f her dilim kendi PR'ıdır (#13–#17 ve 07f), madde başına PR değil.
- Aynı dalda ayrı commit: `CODING_STANDARDS.md` genel kısmı YONETIM'le eşitlendi (15.10 "Seen once" satırı); `test_standartlar` yerelde kırmızıydı (öncül #11, #12).
