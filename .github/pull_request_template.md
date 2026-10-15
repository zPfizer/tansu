## Ne değişti

Değişikliği bir veya iki cümleyle açıklayın.

Akış:

## Kabul ölçütleri
_Kutuları Claude kanıtıyla işaretler. Birleştirme için `tansu-yeni-is` "Merge" adımını uygulayın. İşaretsiz kutu varsa PR birleşmez._

- [ ]

## Definition of Done (Claude ve denetçi kontrol eder, kanıtıyla)

_Ölçütlerin sahibi `DEFINITION_OF_DONE.md`'dir (genel bölüm ve `## Tansu`). Aşağıdaki satırlar yalnız kanıt alanıdır._

- [ ] Doğruluk: kabul ölçütlerinin hepsi karşılandı — kanıt: 
- [ ] Doğruluk: gerçek veriyle çalıştırıldı (yerel koşu çıktısı aşağıda) — kanıt: 
- [ ] Doğruluk: yeni davranışın testi var; değişiklik olmadan kırmızı, değişiklikle yeşil — kanıt: 
- [ ] Doğruluk: eski testler geçiyor (CI) — kanıt: 
- [ ] Doğruluk: kenar durumlar ve hata yolları ele alındı — kanıt: 
- [ ] Kalite: adlar ve yapı niyeti gösteriyor; tekrar eden iş mantığı yok — kanıt: 
- [ ] Kalite: ölü kod, deneme çıktısı, yoruma alınmış kod yok (CI: ruff) — kanıt: 
- [ ] Kalite: lint ve biçim kontrolleri geçti (CI: ruff check, ruff format --check) — kanıt: 
- [ ] Kalite: değişiklik işin kapsamında; ilgisiz düzenleme yok — kanıt: 
- [ ] Entegrasyon: sistemin geri kalanıyla çalışıyor; kayıt ve ayar değişiklikleri hesaba katıldı — kanıt: 
- [ ] Belgeleme: davranış değişikliği belgelendi; belge bugünkü durumu anlatıyor — kanıt: 
- [ ] Tansu: `DEFINITION_OF_DONE.md` `## Tansu` maddelerinin hepsi karşılandı — kanıt: 

## Bağımsız inceleme

Denetçi: 
<!-- CI accepts exactly one Sonuç line, and only one of these three exact texts: "Sonuç: geçti", "Sonuç: GEÇTİ", "Sonuç: NOTLU GEÇTİ". CI rejects "Geçti", KALDI, and a second Sonuç line. -->
Sonuç: 

## Gerçek veri kanıtı

```
```
