# 04: Kural kataloğu ve kural dosyaları tek sahipli

**What to build:** KURALLAR.md, `docs/kurallar/A–E` ve `docs/sadakat.md` arasındaki eski aktarımlar ve tekrarlar
giderilir; her bilgi sahip dosyada kalır, ötekiler atıf verir. Kapsam istisnası (04c, 14.10): iki yerel taslak
(`docs/strateji-modulleri-taslak.md`, `docs/strateji-taslak/tasarim-8.md`) git dışı çalışma belleğidir, sahip tablosunda
değildir ve başlarındaki geçerlilik notu sahibi A–E/KURALLAR/TASARIM olarak gösterir; sapma denetiminin dışındadır
(AGENTS "Documents and owners"). Taslaklardaki tekrar bulgu sayılmaz; yalnız geçerlilik notu olmayan bir taslak bulgu olur.

**Blocked by:** 01, 02

**Status:** in-review

- [x] `denetim/hiza-c.md` 1–22 (eski sözlük alıntıları, BALAT TP2, SAYAS etiketi, Nabız toplama, EMA payda iddiası vb.) düzeltildi. Kanıt: `denetim/bilet-04-rapor.md` bölüm 1 (19 düzeltildi, 1 çürütüldü, 2 zaten düzeltildi); denetim tur 1 düzeltmeleri: rapor "Denetim tur 1 (Codex)".
- [ ] İki görsel çelişkisi (G-125 stop, ICBCT ilk EMA) görsel açılarak çözüldü; doğru sayı tek yerde. Kanıt: rapor bölüm 4 ve tur 1. Açık kısım: ikisi de görselden belirlenemedi. G-125: rakamlar okunamaz (3 piksel yazı), iki aday okuma yalnız E K2'de. ICBCT: ilk EMA etiketi 20 ya da 30 okunamıyor, tek yer B §2 (KRDMD ayarı 20/50/100/200; sadakat ölçümü 20 ile uyuştu). Kutu daha yüksek çözünürlüklü kaynakla ya da Levent'in okumasıyla kapanır.
- [ ] `hiza-c.md` 23–40 ve `hiza-b.md` 16–20, 22 tekrarları atıfa çevrildi. Kanıt: rapor bölüm 2, 3, 5 ve tur 1 (KURALLAR dizini ve sadakat hedefleri, A–E çapraz kopyaları, M ve T8 tabloları atıfa çevrildi). Açık kısım: TASARIM tarafı (K ile T'de iki kez tanımlı çift sinyali ve EMA karşılaştırma koşulları); bilet 03/07 listesi: rapor "TASARIM'a" satırları.
- [ ] `hiza-c-istem.md` yeniden koştu; ÇELİŞKİ, ESKİ ve TEKRAR bulgusu yok.
- [x] KURALLAR okuma kurallarındaki birinci el, ikinci el ve NotebookLM tanımları GLOSSARY'ye atıf verir; KURALLAR yalnız nasıl kullanıldıklarını söyler. Aynı biçimde KURALLAR §2'deki H/K/X tanımı ("birinci elden") GLOSSARY "Hazırlık" maddesine atıf verir. Kanıt: KURALLAR:6–11 ve :24. Yazarlığı belirsiz metin ve imzasız şema da ikinci el sayılır (GLOSSARY "İkinci el").
- [x] Havuz kapsamı: beyindeki Tansu havuzunun 257 (14.10: 258) notundan 136'sı (10.10 sayımı) A–E ve KURALLAR'da hiç geçmiyor. Her biri okunur; kural içeriyorsa ilgili A–E dosyasına işlenir, içermiyorsa A–E'deki "kural içermez" listesine gerekçesiyle yazılır. KURALLAR başlığındaki havuz sayısı güncellenir (14.10: 258 not, 228 görsel, bilet 09). Kanıt: kapsam kontrolü 258 / 258 (her havuz notu adı KURALLAR veya A–E içinde); "kural içermez" listesi KURALLAR sonunda ("Kural içermeyen notlar", 65 not; tur 1'de DEA/VZA ve aylık mevsimsellik notları kural içerdiği için D'ye alındı); 95 atıfsız notun 17 kural + 11 kanıt işlendi; rapor `denetim/bilet-04-havuz-rapor.md`.
- [x] KURALLAR §2 risk satırında "lot" hesaplanan miktar anlamında: "lot adedi" diye yazılır (GLOSSARY "Adet, lot"). Kanıt: KURALLAR:55.
- 14.10 denetim (Codex): tur 1 KALDI (15 bulgu), tur 2 KALDI (9), tur 3 KALDI (3 küçük). AKIS: dördüncü tur yok; yeniden tanım 04b (aynı dal): M:418 formül atfı, rapor rakamı, K tablo kesintisi. Kök neden raporda. Yeni denetim tur 1.
- 14.10 04b denetim (Codex): tur 1 KALDI, tur 2 KALDI, tur 3 KALDI (taslaklarda kalan eşdeğer formüller). AKIS: yeniden tanım 04c = açık kapsam istisnası (AGENTS tablo satırı, hiza-c-istem kapsamı, bilet metni). Kök neden raporda.
