---
name: tansu-grill
description: Tansu'da bir fikri ya da tasarımı sorgulayan görüşme. Matt'in grilling ve domain-modeling skill'lerini Tansu'nun ölçütleriyle çalıştırır. Tansu'da yeni bir kural, parametre, veri kaynağı ya da davranış değişikliği konuşulurken kullan.
---

Skill aracını iki kez çağır: "grilling" ve "domain-modeling". Görüşme boyunca ayrıca şu üç ölçütü uygula.
Kuralların metni sahip dosyalarındadır; bu skill yalnız ne zaman bakılacağını söyler.

## 1. Tansu önce gelir

Bir kural, değer ya da davranış önermeden önce KURALLAR "Okuma kuralları"nı uygula: Tansu havuzunda ve kural
dosyalarında Tansu'nun o konudaki fikrini ara, sonucu öneride göster.

## 2. Risk taraması

Her kararda AGENTS.md "Çalışma kuralları"na ve TASARIM'a karşı şu soruları sor ve cevabını yaz:
- Veri kaynağının kullanım koşullarına uyuyor mu? (TASARIM §4)
- Deneme günlüğü ve `veri/` kuralı korunuyor mu?
- Kural kaydından sonra değişen kural yeni deneme sayılıyor mu? (TASARIM §5.8)
- Geleceği görme riski var mı? (TASARIM §5.12)
- Para kararı Levent'te mi kalıyor? (TASARIM §5.12)

## 3. Değişeceği metni göster

Karar verilecek her yerde değişecek TASARIM, KURALLAR ya da GLOSSARY metnini önceki ve sonraki hâliyle göster. Kod
değişecekse değişecek fonksiyonun bugünkü ve önerilen hâlini kısa göster.

Levent'e yalnız kaynağın ve karar kayıtlarının cevap vermediği yön kararını sor.
