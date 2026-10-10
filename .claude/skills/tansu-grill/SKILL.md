---
name: tansu-grill
description: Tansu'da bir fikri ya da tasarımı sorgulayan görüşme. Matt'in grilling ve domain-modeling skill'lerini Tansu'nun ölçütleriyle çalıştırır. Tansu'da yeni bir kural, parametre, veri kaynağı ya da davranış değişikliği konuşulurken kullan.
---

Skill aracını iki kez çağır: "grilling" ve "domain-modeling". Görüşme boyunca ayrıca şu üç ölçütü uygula.

## 1. Tansu önce gelir

- Bir kural, değer ya da davranış önermeden önce beyindeki Tansu havuzunda ve `docs/kurallar/` dosyalarında Tansu'nun o konudaki fikrini ara.
- Tansu'nun fikri varsa öneri ona uyar. Uyulamıyorsa nedenini yaz ("uygulanamaz").
- Tansu sessizse öneri YORUM olur. YORUM'un deneme sayımına etkisini KURALLAR'dan söyle.
- Not ile görsel çelişirse görseli aç; görsel geçerlidir.
- Seçim yaparken getiri sonucuna bakma.

## 2. Risk taraması

Her kararda şu soruları sor ve cevabını yaz:
- Veri kaynağının kullanım koşullarına uyuyor mu? (İş Yatırım ayak izi, TradingView yasağı, TASARIM §4)
- Deneme günlüğü yalnız ekleme mi kalıyor? `veri/` silinmiyor mu?
- Kural kaydından sonra kural değişiyorsa bu yeni deneme olarak sayılıyor mu?
- Geleceği görme riski var mı? (`tests/test_gelecek.py`)
- Para kararı Levent'te mi kalıyor?

## 3. Değişeceği metni göster

- Karar verilecek her yerde değişecek TASARIM, KURALLAR ya da GLOSSARY metnini önce ve sonra hâliyle göster. Dosya adı ya da bölüm numarası yetmez.
- Kod değişecekse değişecek fonksiyonun bugünkü hâlini ve önerilen hâlini kısa göster.

Levent'e yalnız kaynağın ve karar kayıtlarının cevap vermediği yön kararını sor. Sorular Türkçe ve sadedir.
