# İzleme 19: Hesap çekirdeği (cevaplar-19-cekirdek.md, taslak 6'ya karşı)

Kapsam: yalnız EKSİK, KARAR, YANLIŞ hükümlü maddeler (EKSİK: 0, KARAR: 85, YANLIŞ: 4). CEVAPLI, OLGU, ZAYIF SORU maddeleri alınmadı.

19-001 — KARAR — RED — kod ayrıntısı (skaler argüman, düz tuple); tasarım yüzü TASARIM 4'te yeter
19-002 — KARAR — RED — kod ayrıntısı (dict + 2B dizi); tasarım yüzü TASARIM 4
19-003 — KARAR — YENİ — TASARIM 5.1'e: hissenin eksik günü NaN kalır, ileri doldurma yok; o gün sinyal ve giriş yok; açık pozisyon son bilinen kapanışla taşınır
19-004 — KARAR — TEKRAR — 19-002 (hisse başına DataFrame, MultiIndex yok); kanıt testi 19-050
19-006 — KARAR — VAR — sonuc C-2 (bağımlılık listesinde polars yok) ve pyproject.toml
19-007 — KARAR — RED — kod ayrıntısı; pandas varsayılanı float64
19-008 — KARAR — RED — gereksiz; yuvarlama yapılmaz, %0,5 masraf senaryosu kapsar (TASARIM 5.4)
19-009 — KARAR — TEKRAR — 19-007 (Decimal yok, float64)
19-010 — KARAR — RED — TASARIM 5.1 %0,5 eşiğiyle çelişir; eşiği ilk koşuda sonuca bakıp sabitlemek de yanlış
19-011 — KARAR — VAR — TASARIM 5.1 "Seriler" (gösterge düzeltilmiş, limit ve likidite ham)
19-012 — KARAR — VAR — TASARIM 5.1 "Olay denetimi" (SHHE_FIYAT_AYAR_OR ile HGDG karşılaştırması), sonuc O2/O3
19-013 — KARAR — VAR — TASARIM 5.1 "Hacim: HACIM TL'dir", sonuc O1 (lot→TL dönüşümü zaten gerekmiyor)
19-014 — KARAR — VAR — TASARIM 5.13 (bozuk satır karantina) ve 5.1 (fiyat yamanmaz)
19-015 — KARAR — YENİ — TASARIM 5.13'e bir satır: yapısal ihlal (sıra bozuk, tekrar eden gün, ortada NaN) koşuyu durdurur; satır ihlali karantina (o kısım VAR)
19-016 — YANLIŞ — RED — EMA ilk fiyattan tohumlu `ewm(adjust=False)` Tansu'nun kendi formülüdür ve KRDMD'de lejantla birebir (KURALLAR §3, §4; sonuc O9, O16); pandas-ta-classic C-2 ile çıkarıldı; ısınma etkisini 19-017 kapatır
19-017 — KARAR — YENİ — TASARIM 5.1'e: ısınma tamamlanmadan (2 × EMA200 = 400 işlem günü, hissenin kendi ilk gününden) sinyal yok
19-018 — KARAR — TEKRAR — 19-017 (tek ısınma maskesi)
19-019 — KARAR — TEKRAR — 19-017 (evren ∧ ısınma ∧ karantina; evren ve karantina zaten VAR: TASARIM 5.2, 5.1)
19-020 — KARAR — RED — TASARIM 5.1 karantina yeni sinyali 250 gün engeller, seriyi bölmez; ısınma sıfırlama aşırı kurulum (650 gün kayıp)
19-023 — KARAR — RED — pandas-ta-classic C-2 ile çelişir; pyproject'te yok
19-024 — KARAR — RED — pandas-ta-classic C-2 ile çelişir (TASARIM 4: gostergeler kütüphanesiz, birkaç satır); TA-Lib kararı zaten VAR
19-025 — KARAR — YENİ — TASARIM 5.5'e: ATR Wilder, ilk değer ilk 14 TR ortalaması, kendi kodla (kütüphane yok)
19-027 — KARAR — VAR — TASARIM 5.1 "Seriler" (ATR düzeltilmiş seriden); segment yeniden başlatma kısmı 19-020 gibi uygulanmaz
19-028 — KARAR — YENİ — KURALLAR §4 aday kümesine ddof {0,1} eklenir (z için ddof yazılı değil); en iyi üreten seçilir ve kaydedilir
19-029 — KARAR — RED — kod ayrıntısı (β'lı kalıntı yalnız aday, KURALLAR §4); tam pencere kuralı 19-091
19-031 — KARAR — VAR — TASARIM 5.1 "Seriler" (getiri ve gösterge düzeltilmiş seriden; sadakat ayrı ham)
19-033 — KARAR — VAR — sonuc C-11 (200 tekrar ≤ 5 dk; yetmezse algoritma sonra joblib); 1.000 tekrar bütçesi ek ayrıntı
19-035 — KARAR — VAR — sonuc C-11 (numba yok)
19-036 — KARAR — TEKRAR — 19-035
19-037 — KARAR — TEKRAR — 19-035
19-038 — KARAR — VAR — sonuc C-11 (yetmezse joblib)
19-039 — KARAR — VAR — TASARIM 5.7 K1 (rastgele işlemler tam çıkış paketini uygular) ve TASARIM 4 (aynı Adım)
19-040 — KARAR — RED — kod ayrıntısı (maske belleği)
19-041 — KARAR — VAR — TASARIM 5.11 (tohum deneme günlüğünde); RNG türü kod ayrıntısı
19-042 — KARAR — TEKRAR — 19-041 (perm başına SeedSequence.spawn alt tohumu); joblib şimdi yok (C-11)
19-043 — KARAR — YENİ — TASARIM 5.11'e bir cümle ve tek test: aynı tohum ve aynı anlık görüntüyle iki koşu aynı özeti verir
19-044 — YANLIŞ — VAR — pyproject.toml (bağımlılıklar `==`, `requires-python = "==3.14.*"`) ve sonuc C-2; vectorbt, yfinance yok; cevaptaki pandas-ta-classic ve tqdm satırları uygulanmaz (C-2)
19-045 — KARAR — VAR — sonuc C-2 (düz pip, pyproject `==`, uv yok)
19-047 — KARAR — RED — kod ayrıntısı (perm başına yalnız özet)
19-048 — KARAR — RED — 3 aile varsayar; AB=CD çıktı (TASARIM 3, B-1); sayım karar değil tahmin
19-049 — KARAR — TEKRAR — 19-050 (kesme testi aynı güvenceyi verir)
19-050 — KARAR — VAR — sonuc C-9 ("veriyi kes, geçmiş değişmesin" testi)
19-051 — KARAR — RED — pivot yalnız AB=CD'de; ikinci dalga (TASARIM 3, B-1)
19-052 — KARAR — RED — pivot yalnız AB=CD'de; ikinci dalga (TASARIM 3, B-1)
19-053 — YANLIŞ — VAR — KURALLAR §3 "art arda en az 3 gün" ve sonuc B-11/O16 (eski kod hatası olarak kayıtlı; ön deneme kodu silindi)
19-054 — KARAR — RED — AB=CD ikinci dalga; geri kalanı kod ayrıntısı
19-055 — KARAR — YENİ — TASARIM 5.3'e: giriş günü yoksa ya da kilitli tavansa sinyal düşer, kaymaz; rapor "iptal" sayısını yazar
19-056 — KARAR — VAR — TASARIM 5.3 "Kilitli gün" ve 5.1 "Seriler" (ham seriden)
19-057 — KARAR — RED — TASARIM 5.1 ve 5.3 limit fiyatını önceki ham kapanıştan hesaplar (sonuc B-5); kendi 19-056 maddesiyle de çelişir
19-059 — KARAR — VAR — TASARIM 5.6 (%1 risk, %10 tavan, aşağı yuvarlama), 5.4 (likidite), sonuc B-12 (fiili risk raporu)
19-060 — KARAR — TEKRAR — 19-007 (float64, yuvarlama yok)
19-061 — KARAR — VAR — TASARIM 5.6 "Faiz" (takvim günü, /365)
19-062 — KARAR — VAR — TASARIM 5.6 "Faiz" (bir gün gecikmeli)
19-063 — KARAR — VAR — TASARIM 5.4 (%0,3 her yönde, %2 likidite) ve 5.3 (kilitli taban ertesi güne kayar)
19-064 — KARAR — VAR — TASARIM 5.6 (özkaynak = nakit + kapanış değeri) ve 5.7 (günlük portföy getirisi)
19-065 — KARAR — VAR — TASARIM 5.6 (bileşik büyür), 5.7 ve 5.9 (günlük fazla getiri üzerinde bootstrap)
19-066 — KARAR — VAR — TASARIM 5.9 (blok yeniden örnekleme, kendi kod) ve sonuc C-2 (arch bağımlılıkta yok); blok uzunluğu 19-067'ye bakın
19-067 — KARAR — RED — blok = max(20, ortalama tutma) sonuc B-16 / TASARIM 5.9 ile çelişir; ek 10 ve 40 koşuları aşırı kurulum
19-068 — KARAR — VAR — TASARIM 5.7 ve sonuc B-14 (B ≥ max(1.000, 20·m))
19-069 — KARAR — YENİ — TASARIM 5.7'ye: p = (1 + k) / (1 + B), sıfır p çıkmaz
19-070 — KARAR — YENİ — TASARIM 5.9'a: "en iyi %5 atılmış" = işlemler sıralanır, üstten ceil(0,05·n) atılır; aralık 2,5 ve 97,5 yüzdelik
19-071 — YANLIŞ — YENİ — TASARIM 5.12'ye: "düşüşte kalma" = sermaye eğrisinin önceki zirvenin altında kaldığı en uzun ardışık takvim süresi, kapanış bazlı eğriden; (quantstats'ın çıkması zaten VAR: sonuc C-2, TASARIM 4 "ölçütler kendi kodumuz")
19-073 — KARAR — TEKRAR — 19-071 (kapanış bazlı eğriden düşüş; raporda "kapanış bazlı" etiketi)
19-074 — KARAR — RED — kod ayrıntısı; ham karşılaştırma varsayılan davranış
19-075 — KARAR — RED — sonuc C-6 hash'i `ast.dump` + parametre JSON; bayt hash yorum değişince yeni deneme sayar
19-076 — KARAR — RED — sonuc C-4 manifest sha256 yeter; içerik hash'i aşırı kurulum
19-077 — KARAR — VAR — sonuc C-4 (parquet) ve pyproject (pyarrow==25.0.1)
19-078 — KARAR — TEKRAR — 19-077 (tz'siz tarih, float64)
19-079 — KARAR — TEKRAR — 19-015 (veri deposu yapısal ihlali reddeder)
19-080 — KARAR — TEKRAR — 19-015 (tek dogrula; pandera yok zaten C-2)
19-081 — KARAR — RED — kod ayrıntısı (sütun adları); ilk veri işinde (TASARIM 7.2) sabitlenir
19-082 — KARAR — YENİ — AGENTS.md çalışma kurallarına: her dosya açışında `encoding="utf-8"` açık yazılır (Windows varsayılanı cp1254 olabilir)
19-083 — KARAR — VAR — TASARIM 4 (motor: Adım saf, sınama ve canlı aynı Adım)
19-084 — KARAR — RED — eşitlik nadir; kararlı sıralama yeter (TASARIM 5.6 "en likit önce")
19-085 — KARAR — RED — kod ayrıntısı (hız)
19-086 — KARAR — TEKRAR — 19-085 (döngü yapısı kod ayrıntısı)
19-087 — KARAR — VAR — TASARIM 5.6 (her aile kendi sermayesiyle ayrı)
19-088 — KARAR — RED — sonuc C-5 ile çelişir: açık durum saklanmaz, her gün Adım ile yeniden hesaplanır; durum dosyası aşırı kurulum
19-089 — KARAR — VAR — TASARIM 6.6 ve sonuc C-5 (sinyal gününden itibaren her gün Adım ile yeniden hesap)
19-090 — KARAR — VAR — TASARIM 6.6 ve sonuc C-5 (zaten her gün baştan; kartlar.jsonl yalnız eklenir)
19-092 — KARAR — VAR — TASARIM 5.4 (son 10 günün medyanı) ve sonuc C-9 (kesme testi sızıntıyı yakalar)
19-093 — KARAR — RED — TASARIM 5.2 "önceki ayın son kapanışındaki" piyasa değerini ister; ay başı gününün PD'si sızıntı
19-094 — KARAR — VAR — TASARIM 5.6 "Çift seçimi" (önceki 252 gün, her yıl başı)
19-095 — KARAR — VAR — sonuc C-9 ve AGENTS.md (elle hesaplı test, hypothesis yok); "düşük = stop" TASARIM 5.3 stop kenarları
19-096 — KARAR — VAR — TASARIM 4 (aileler sinyal, motor Adım) ve 6.6
19-097 — KARAR — VAR — sonuc C-11 (önce algoritma, sonra joblib; numba yok)
19-098 — KARAR — RED — TASARIM 4 tek giriş `python -m tansu sinama` ile çelişir; tqdm C-2 listesinde ve pyproject'te yok
19-099 — KARAR — TEKRAR — 19-015 (girişte sonlu ve fiyat > 0 assert); `filterwarnings = error` uygulanmaz: üçüncü parti uyarılar testi kırar
19-100 — KARAR — TEKRAR — 19-002 (özet); pandas-ta-classic kısmı RED: 19-016, 19-024

## Özet

Sayımlar grep ile yapıldı (satır başı "19-"):

- VAR: 35
- TEKRAR: 16
- YENİ: 11
- RED: 27
- Toplam: 89

YENİ maddeler ve önerilen değişiklik:
- 19-003: TASARIM 5.1'e, eksik gün NaN, ileri doldurma yok, o gün sinyal/giriş yok, açık pozisyon son kapanışla taşınır.
- 19-015: TASARIM 5.13'e, yapısal ihlal (sıra, tekrar, ortada NaN) koşuyu durdurur.
- 19-017: TASARIM 5.1'e, ısınma 400 işlem günü (hissenin ilk gününden), öncesinde sinyal yok.
- 19-025: TASARIM 5.5'e, ATR Wilder, ilk değer ilk 14 TR ortalaması, kendi kod.
- 19-028: KURALLAR §4 aday kümesine ddof {0,1}.
- 19-043: TASARIM 5.11'e, aynı tohum ve anlık görüntü aynı özeti verir (tek test).
- 19-055: TASARIM 5.3'e, giriş günü yoksa ya da kilitli tavansa sinyal düşer; rapor "iptal" sayısı.
- 19-069: TASARIM 5.7'ye, p = (1 + k) / (1 + B).
- 19-070: TASARIM 5.9'a, en iyi %5 atılmış = üstten ceil(0,05·n) işlem; aralık 2,5 / 97,5.
- 19-071: TASARIM 5.12'ye, düşüşte kalma = zirvenin altında en uzun ardışık takvim süresi (kapanış bazlı).
- 19-082: AGENTS.md'ye, dosya açarken `encoding="utf-8"` açık yazılır.

YANLIŞ maddeler VAR olmayanlar:
- 19-016: RED. EMA ilk fiyat tohumu Tansu'nun formülüdür (KURALLAR §3, §4, sonuc O9, O16); pandas-ta-classic çıkarıldı (C-2). Değişiklik yok.
- 19-071: YENİ. Yukarıdaki değişiklik (TASARIM 5.12).

YANLIŞ maddeler VAR olanlar: 19-044 (pyproject zaten `==` kilitli ve `requires-python` var; sonuc C-2), 19-053 (KURALLAR §3 zaten "art arda").
