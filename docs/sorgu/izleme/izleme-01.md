# İzleme 01: cevaplar-01-veri.md karşılaştırması (taslak 6'ya karşı)

Kapsam: hüküm değeri EKSİK, KARAR veya YANLIŞ olan 75 madde (71 EKSİK, 4 YANLIŞ, 0 KARAR). Diğer hükümler (CEVAPLI, OLGU, ZAYIF SORU) alınmadı.
Referans kısaltmaları: TASARIM = docs/TASARIM.md taslak 6; sonuc = docs/sorgu/sonuc-3-4.md (B-n, C-n, O-n).

01-001 — EKSİK — YENİ — TASARIM 6.2 / sonuc C-4: manifest sha256 koşu başında doğrulanır, uymazsa koşu durur (parquet + manifest zaten C-4'te).
01-002 — EKSİK — VAR — sonuc C-4 (her akşam tam indirme); HGDG/HG oran adımı TASARIM 5.1 olay denetimiyle uyarı verir.
01-003 — EKSİK — VAR — TASARIM 5.13 günlük koşu (5'ten fazla hisse inmezse SORUNLU) + 6.2 (kapı geçmezse kart yok) + 5.11 (günlükte anlık görüntü).
01-004 — EKSİK — VAR — TASARIM 6.6 (kartlar.jsonl yalnız eklenir, kâğıt üstü dönem geriye dönük değişmez); ham TL için 01-079.
01-006 — EKSİK — VAR — TASARIM 8.1 (yayın saati açık soru) + 6.1 (4 saat saatlik yeniden deneme) + 5.1 bugünkü veri kuralı.
01-007 — EKSİK — VAR — TASARIM 5.1 Bugünkü veri (son çubuk bugün değilse kart yok) + Hacim (hacmi sıfır gün işlem günü değildir).
01-008 — EKSİK — RED — aşırı kurulum; evren hacim filtresi (5.2) ve %2 likidite sınırı (5.4) var.
01-009 — EKSİK — VAR — TASARIM 4 ("Takvim, fiyat günlerinden çıkar").
01-010 — EKSİK — RED — aşırı kurulum; tatil/hata ayrımı yalnız etiket, 5.1 bugünkü veri ve durum.txt (VERİ YOK) yeter.
01-013 — EKSİK — TEKRAR — 01-009.
01-014 — EKSİK — RED — 01-008 reddine bağlı; yılda 2-3 gün, etkisi küçük.
01-015 — EKSİK — VAR — TASARIM 5.1 Hacim (hacmi sıfır gün işlem günü değildir) + 5.2 (60 günden uzun durdurma = kapanma).
01-016 — EKSİK — VAR — TASARIM 4 ("Endeks günleri ve sektör: borsapy"; piyasa durumu XU100 6.3).
01-018 — EKSİK — VAR — TASARIM 5.1 İndirme (2010'dan indir, ilk sinyal 30.11.2015) / sonuc B-6.
01-019 — EKSİK — VAR — TASARIM 5.1 İndirme (ilk sinyal 30.11.2015) / sonuc B-6.
01-023 — EKSİK — YENİ — TASARIM 5.3 Kilitli gün: fiyat adımı tablosunun kaynağı (Borsa İstanbul prosedürü) yazılır; sınama vakası KONTR 08.07.2026.
01-024 — EKSİK — YENİ — TASARIM 5.1 Fiyat limiti: olay gününde baz = önceki ham kapanış × SHHE_FIYAT_AYAR_OR (kilit ve karantina bu bazla).
01-025 — EKSİK — RED — hesap HGDG serisinde yapılır (5.1), çarpan örtük uygulanır; karantina olayla açıklananı zaten dışlar; ek kural aşırı.
01-026 — EKSİK — YENİ — TASARIM 5.3 Kilitli gün: kapanışı tavan olan (limit − 1 adım) günde de giriş yok; yalnız MIN=MAX sürümü duyarlılık.
01-027 — EKSİK — TEKRAR — 01-026 (simetrik taban kuralı aynı değişiklikte).
01-028 — EKSİK — VAR — TASARIM 5.3 Kilitli gün (kilitli tabanda çıkış ertesi güne kayar, her gün aynı kural) + 5.2 kapanan hisse.
01-029 — EKSİK — VAR — TASARIM 5.3 Kilitli gün / sonuc B-5 (MIN=MAX ∧ HACIM>0 ∧ limit fiyatında).
01-030 — EKSİK — RED — aşırı kurulum; kilit tanımı B-5 ile ayrıştırıldı, 01-026 duyarlılığı yeter.
01-031 — EKSİK — VAR — TASARIM 5.13 Satır şartları (düşük ≤ AOF ≤ yüksek, düşük ≤ kapanış ≤ yüksek; bozuk satır karantina).
01-032 — EKSİK — RED — TASARIM 5.4 %2 medyan sınırı var; ayrı dolum oranı raporu aşırı.
01-033 — EKSİK — VAR — TASARIM 5.3 Giriş günü (yalnız stop) + Stop dolumu (gün düşüğü ≤ stop ise dolum) / sonuc B-4.
01-034 — EKSİK — RED — B-3 ile çelişir (borsapy açılışı motora bağlanmaz).
01-036 — EKSİK — VAR — sonuc B-11 ("520 dönem" sayımı silinir); KURALLAR §3'te sayı yok.
01-038 — EKSİK — RED — Yahoo çıktı (B-2); sadakat ham İş serisiyle (KURALLAR §4).
01-039 — EKSİK — RED — Yahoo çıktı (B-2), auto_adjust ayarı konu dışı.
01-040 — EKSİK — VAR — TASARIM 5.1 Olay denetimi (fark %0,5'i aşan gün uyarı, HGDG geçerli kalır).
01-043 — EKSİK — VAR — TASARIM 5.1 Olay denetimi (olay tablosu bütün kodlarıyla, HGDG ile karşılaştırılır) + TASARIM 4 Şirket olayları.
01-045 — EKSİK — RED — kapsam dışı; olay denetimi (5.1) zaten HGDG ile karşılaştırır, çok kayıt çarpımı kod ayrıntısı.
01-047 — EKSİK — VAR — TASARIM 5.1 Olay denetimi + Karantina (olayla açıklanmayan sıçrama karantina).
01-048 — EKSİK — VAR — TASARIM 5.1 Karantina (o günden 250 gün yeni sinyal yok).
01-049 — EKSİK — VAR — TASARIM 5.1 İkinci kaynak (borsapy getirileriyle bütün hisse × gün, fark %0,5'i aşan günler listelenir).
01-051 — EKSİK — VAR — TASARIM 5.13 Eşikler (karantina hisse-gün oranı > %1 ise veri sorunlu).
01-052 — EKSİK — VAR — TASARIM 5.1 Karantina ("Aynı maske kural, K1 ve K2'ye uygulanır").
01-053 — YANLIŞ — VAR — örnek taslak 6'da yok; sonuc O7 + TASARIM 5.1 Fiyat limiti (L %20 → 13.03.2020'den %10).
01-055 — EKSİK — VAR — TASARIM 5.13 Eşikler (ikinci kaynak uyuşmazlığı > %2) + TASARIM 4 (İş birincil).
01-056 — EKSİK — TEKRAR — 01-055.
01-057 — EKSİK — YENİ — sonuc C-8 / TASARIM 4: okuma zaman aşımı 30 sn → 120 sn (ağır sorgular 40 ve 90 sn'de zaman aşımına uğradı; borsapy yedek fiyat kaynağı reddedilir, HGDG kaybolur).
01-058 — EKSİK — VAR — sonuc C-8 (şema assert) + TASARIM 5.13 günlük koşu.
01-059 — EKSİK — RED — kapsam dışı; kişisel kullanım, kullanım koşulları zaten Açık soru 1.
01-064 — EKSİK — TEKRAR — 01-032.
01-065 — EKSİK — RED — fiili dolaşım taraması ikinci dalgada (TASARIM 3).
01-067 — EKSİK — RED — aşırı kurulum; BIST100 evreninde çift sınıf pay nadir, elle eşleme tablosu gereksiz.
01-068 — EKSİK — VAR — TASARIM 5.2 Evren kuralı (ayın ilk işlem günü, önceki ayın son kapanışı).
01-069 — EKSİK — YENİ — TASARIM 5.2 (ya da 5.3): gösterge penceresi (SMA250, 60 gün hacim) dolmayan hissede sinyal yok.
01-070 — EKSİK — VAR — TASARIM 5.2 İşlemi kapanan hisseler (−%100, nedeni bilinirse son fiyat; 60 gün durdurma = kapanma) / sonuc B-9.
01-071 — EKSİK — TEKRAR — 01-070.
01-073 — EKSİK — RED — aşırı kurulum; kod yeniden kullanımı nadir, limit dışı sıçramayı karantina (5.1) yakalar.
01-075 — EKSİK — RED — aşırı kurulum; bedelli günü HGDG ile düzeltilir (5.1), ayrı rapor gereksiz.
01-077 — EKSİK — RED — kapsam dışı; sadakat ham İş serisiyle yapılır (KURALLAR §4), HGDG/borsapy ayrı hesabı aşırı.
01-078 — EKSİK — VAR — TASARIM 5.1 Seriler (göstergeler HGDG) + Olay denetimi (çarpan yalnız denetim) / sonuc B-2.
01-079 — EKSİK — YENİ — TASARIM 6.5 Kart içeriği: referans fiyat ve stop ham TL gösterilir = HGDG seviyesi × (HG_t / HGDG_t).
01-080 — EKSİK — TEKRAR — 01-079.
01-081 — EKSİK — TEKRAR — 01-079.
01-082 — EKSİK — RED — aşırı kurulum; Motor belirleyici ve anlık görüntü sabit (sonuc C-4, C-5).
01-083 — EKSİK — VAR — TASARIM 5.4 Masraf (%0,1 / %0,3 / %0,5 senaryoları, kabul %0,5'te).
01-084 — YANLIŞ — VAR — TASARIM 5.4 Masraf ("komisyon, BSMV, kayma birlikte"); "açılışta kovalama" ifadesi taslak 6'da yok.
01-085 — EKSİK — RED — aşırı kurulum; stop dolumu min(stop, AOF) (B-4) ve %0,5 masraf senaryosu kapsar.
01-086 — EKSİK — VAR — TASARIM 5.2 Sektör + 5.6 Çift seçimi (aynı sektörden çift; sektörsüz hisse çifte giremez).
01-087 — YANLIŞ — VAR — TASARIM 4 Faiz + 5.6 Faiz (borsapy politika faizi; EVDS/TLREF yok) / sonuc B-8, O8.
01-088 — YANLIŞ — VAR — TASARIM 4 Faiz ("2015'ten tek seri") / sonuc B-8.
01-089 — EKSİK — YENİ — TASARIM 5.13: faiz serisinin son tarihi > 60 gün eskiyse "faiz bayat" uyarısı; ileri doldurma süresi raporlanır.
01-091 — EKSİK — VAR — TASARIM 5.6 Faiz ("bir gün gecikmeli").
01-092 — EKSİK — VAR — TASARIM 5.4 Vergi (sınamaya girmez, raporda not) + 8.7.
01-093 — EKSİK — VAR — TASARIM 5.11 (günlükte anlık görüntü; aynı kuralın tekrar koşusu yeni deneme değil) / sonuc C-6.
01-094 — EKSİK — YENİ — TASARIM 4 veri / 6.2: anlık görüntü fiyat (ham + HGDG), olay tablosu ve faiz serisini birlikte içerir; hepsi manifest'te hash'li (evren ve takvim fiyattan türer).
01-095 — EKSİK — RED — aşırı kurulum; tek kullanıcı, hata olursa yeni anlık görüntü alınır (5.8: sonraki her değişiklik yeni deneme).
01-096 — EKSİK — VAR — TASARIM 6.1 (kaçırılan koşu açılışta çalışır) + 6.6 (açık kartlar Adım ile yeniden hesaplanır).
01-097 — EKSİK — YENİ — TASARIM 5.1 İkinci kaynak: borsapy'nin bugünkü yarım çubuğu karşılaştırmaya girmez; karşılaştırma T−1'e kadar.
01-098 — EKSİK — TEKRAR — 01-094.
01-100 — EKSİK — VAR — TASARIM 5.13 (getiri görülmeden yazılır, kural kaydına girer; karantina ve uyuşmazlık eşikleri) / sonuc B-7.

## Özet

**Etiket sayıları** (grep ile sayıldı, toplam 75)

1. VAR: 38
2. TEKRAR: 8
3. YENİ: 10
4. RED: 19

**YENİ maddeler (uygulanacak değişiklik)**

- 01-001 — TASARIM 6.2 / C-4: koşu başında manifest sha256 doğrula; uymazsa dur.
- 01-023 — TASARIM 5.3: fiyat adımı tablosunun kaynağını (BIST prosedürü) yaz; vaka KONTR 08.07.2026.
- 01-024 — TASARIM 5.1 Fiyat limiti: olay gününde baz = önceki ham kapanış × SHHE_FIYAT_AYAR_OR.
- 01-026 — TASARIM 5.3 Kilitli gün: kapanışı tavan olan günde de giriş yok (01-027 ile taban çıkışı simetrik kayar); MIN=MAX duyarlılık.
- 01-057 — C-8: okuma zaman aşımı 30 sn → 120 sn.
- 01-069 — TASARIM 5.2: gösterge penceresi dolmadan sinyal yok.
- 01-079 — TASARIM 6.5: kartta ham TL seviye = HGDG seviyesi × (HG_t / HGDG_t) (01-080 ve 01-081 aynı değişiklik).
- 01-089 — TASARIM 5.13: faiz serisi > 60 gün eskiyse uyarı; ileri doldurma süresi raporlanır.
- 01-094 — TASARIM 4 / 6.2: anlık görüntü = fiyat (ham + HGDG) + olay tablosu + faiz, hepsi manifest hash'li (01-098 aynı).
- 01-097 — TASARIM 5.1 İkinci kaynak: borsapy bugünkü yarım çubuğu atılır; T−1'e kadar karşılaştır.

**YANLIŞ maddeler, VAR olmayan**

- Yok. Dört YANLIŞ maddenin hepsi taslak 6'da zaten çözülmüş: 01-053 (sonuc O7), 01-084 (TASARIM 5.4), 01-087 ve 01-088 (sonuc B-8).
