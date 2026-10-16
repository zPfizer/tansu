# Build izi: sürüm 2 ana kapsamı (17.10)

Codex sürüm 2 tur 2 bulgusu: ilk Build turunda `mattpocock-skills:implement` ve `mattpocock-skills:tdd` çağrılmadı. Ana kapsam
bu iki beceriyle yeniden yürütüldü. Yüz (seam): `tansusinama.calistir` çıktısı (spec.md "Interfaces"). Dilim başına bir TASARIM
5.14 kuralı, bir test. Kırmızı: HEAD'in test dosyası geçici bir çalışma ağacında sürüm 1 koduyla (b464df1) koşuldu. Yeşil: HEAD.
Geçici çalışma ağacı kaldırıldı (`git worktree list` çıktısında yok).

| Dilim (TASARIM 5.14) | Test | b464df1'de kırmızı satırı | Kod commit'i |
|---|---|---|---|
| Dönemin son günü: son satır karantinalı, karantina çıkışı | `test_cift_son_satir_karantina_karantina_cikisi_veri_sonu_degil` | `assert (1 == 1 and 0.05052841894947191 == 0.0400231 ± 1.0e-07` | 02341c8 |
| Son gün sonlu kapanışlı karantina (çift) | `test_cift_son_gun_limit_asimi_karantina_cikisi` | `assert 0.02295204795204797 == -0.001998 ± 1.0e-06` | 02341c8 |
| Son gün sonlu kapanışlı karantina (EMA) | `test_ema_son_gun_limit_asimi_karantina_cikisi` | `assert 0.06582737650698811 == 0.0076913 ± 1.0e-07` | 02341c8 |
| İleri yürümenin son yılı | `test_ema_ileri_son_yil_donemin_son_gunu` | `KeyError: 'donem'` | 02341c8 |
| Al-tut: dönem başı AOF sıfır | `test_ema_al_tut_donem_basi_aof_sifir_sonraki_gecerli_gun` | `ZeroDivisionError: division by zero` | 02341c8 |
| Al-tut: son kapanış sonsuz | `test_ema_al_tut_son_kapanis_sonsuz_son_gecerli_kapanis` | `assert inf == 0.0076913 ± 1.0e-07` | 02341c8 |
| Dönem başı: tek gün, AOF sıfır (EMA) | `test_ema_donem_basi_sifir_aof_tek_gun_atlanir` | `ZeroDivisionError: division by zero` | 02341c8 |
| 1-3-5 gün: geçersiz gün sayılmaz (EMA) | `test_sonraki_gecersiz_gun_sayilmaz` | `assert 0.06796116504854366 == 0.0776699 ± 1.0e-07` | 02341c8 |
| 1-3-5 gün: geçersiz gün sayılmaz (çift) | `test_sonraki_cift_gecersiz_gun_sayilmaz` | `assert 0.0 == 0.0526316 ± 1.0e-07` | 02341c8 |
| Çift: son kapanış sonsuz | `test_cift_sonsuz_son_kapanis_son_gecerli_fiyat_ve_karantina_cikisi` | `assert inf == -0.001998 ± 1.0e-06` | 02341c8 |
| Çift dönem başı: AOF sıfır | `test_cift_donem_basi_gecersiz_gun_sonraki_gune_kayar[aof_sifir]` | `assert inf == 0.0030424 ± 1.0e-07` | 02341c8 |
| Çift dönem başı: limit aşımı | `test_cift_donem_basi_gecersiz_gun_sonraki_gune_kayar[limit_asimi]` | `assert -0.0019980019980019303 == 0.0030424 ± 1.0e-07` | 02341c8 |
| Tek günlük çift dönemi: geçersiz fiyat | `test_cift_tek_gunluk_donem_gecersiz_fiyat_atlanir` | `AssertionError: assert ([] == ['A-B']` | 02341c8 |
| Tek günlük çift dönemi: `donem` alanı | `test_cift_tek_gunluk_donem_donem_alani` | `KeyError: 'donem'` | 02341c8 |
| Sonsuz düzeltilmiş fiyat karantina (EMA) | `test_ema_sonsuz_duzeltilmis_fiyat_karantina_gunu` | `assert inf == -0.001998 ± 1.0e-06` | 157fb8d |
| Sonsuz düzeltilmiş fiyat karantina (çift) | `test_cift_sonsuz_duzeltilmis_fiyat_karantina_gunu` | `assert (1 == 1 and 0.05052841894947191 == -0.001998 ± 1.0e-06` | 157fb8d |

Özet çıktılar:
- b464df1 kodu, HEAD testleri: `16 failed, 36 passed, 6 warnings in 6.37s`.
- af0acd2 kodu (157fb8d'den önce), HEAD testleri: `2 failed, 50 passed, 2 warnings in 6.95s` (yalnız son iki satır).
- HEAD 9f8f79c: `52 passed in 6.04s`.

Not: `test_ema_ileri_son_yil_donemin_son_gunu` ve `test_cift_tek_gunluk_donem_donem_alani` b464df1'de önce `donem` alanında kalır.
İleri yürüme diliminin yıl sonucu ayrıca Codex tur 2'de ölçüldü: b464df1 `{"A": []}`, HEAD `{"A": [{"yil": 2026, "hucre": null}]}`.
