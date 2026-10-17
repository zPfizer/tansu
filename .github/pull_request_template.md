## Ne değişti

Değişikliği bir veya iki cümleyle açıklayın.

Akış:
Çağrılan beceriler:
<!-- Liste, bu oturumdaki Skill çağrılarının çağrı sırasıyla kopyasıdır. Çağrılmayan beceri yazılmaz. CI, akışa göre gereken adları arar. -->
<!-- Her sayı ve 'hepsi / hiçbiri' iddiası bu oturumda koşulan bir komutun çıktısından kopyalanır. Komutu ya da dosyayı yanına yaz. -->

## Kabul ölçütleri
_Kutuları Claude kanıtıyla işaretler. Birleştirme için `tansu-yeni-is` "Merge" adımını uygulayın. İşaretsiz kutu varsa PR birleşmez._

- [ ]

## Definition of Done (Claude ve denetçi kontrol eder, kanıtıyla)

_Ölçütlerin sahibi `DEFINITION_OF_DONE.md`'dir (genel bölüm ve `## Tansu`). Aşağıdaki satırlar yalnız kanıt alanıdır._

_Kanıt, bu oturumda koşulan komutun çıktısıdır. 'CI'da' yazma. CI sonucunu birleştirmeden önce ekle._

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
Denetçi kararı (aynen):
Yanlış iddia sayısı:
İkinci geçiş:
Denetlenen commit:
Bulgu sayısı:
<!-- Denetlenen commit, kopyalanan geçişin okuduğu commit'in tam sha'sıdır (40 küçük harfli onaltılı hane). CI, bu sha PR başı değilse PR'ı reddeder. Tek istisna: sonraki commit'lerin hepsi taban dal birleştirmesiyse ve her birleştirme yalnız bu dalın değiştirmediği dosyaları getirip her dosyayı bir taraftan değişmeden alıyorsa CI kabul eder. İki tarafın da değiştirdiği bir dosya yeni geçiş ister. Bulgu sayısı, kopyalanan geçişin bulgu sayısıdır (tam sayı, 0 ya da daha çok). -->
<!-- CI kuralları: CI, her kuraldan önce tüm HTML yorumlarını siler. Denetçi kararı satırı, denetçinin karar satırının kelimesi kelimesine kopyasıdır. CI, bölümde KALDI sözcüğünü görürse PR'ı reddeder. "KALDI olabilir" gibi bir şüphe de KALDI sayılır (docs/agents/is-kurallari.md "Auditor and rounds"). CI, KALDI sözcüğünü ve şüphe sözcüklerini (olabilir, belki, şüphe, emin değil) bölümün tamamında arar; yalnız Sonuç satırını dışarıda bırakır. Satır sonları boşluk sayılır, alan satırları da aranır. Bulursa PR'ı reddeder. Kopyadaki karar sözcüğü Sonuç satırındakiyle aynı olmalıdır. Yanlış iddia sayısı, kopyalanan (son) geçişin sayısıdır ve 0 olmalıdır. İkinci geçiş satırı "yok" veya "geçti" olur: düzeltme geçişi koşuldu mu. CI, "İNCELEME" yer tutucusunu reddeder. -->
<!-- CI accepts exactly one Sonuç line, and only one of these three exact texts: "Sonuç: geçti", "Sonuç: GEÇTİ", "Sonuç: NOTLU GEÇTİ". CI rejects "Geçti", KALDI, and a second Sonuç line. -->
Sonuç: 

## Risk

<!-- Ne bozulabilir? Bozulursa kim fark eder? CI, bölümün boş olmasını reddeder. -->

## Nasıl geri alınır

<!-- Komutu ya da adımları yazın. CI, bölümün boş olmasını reddeder. -->

## Bulgu yanıtları

<!-- Kopyalanan geçişin her bulgusu için bir satır yazın. Yanıt şunlardan biri olur: düzeltildi, yanlış, bilerek, önemsiz. Son sütuna commit ya da neden yazın. Satır sayısı Bulgu sayısına eşit olmalıdır. Bulgu sayısı 0 ise başlık ve ayraç dışında yalnız "bulgu yok" satırı kalır. Her tablo satırı | ile başlar ve biter; hücrede | ve ters bölü olmaz. Tablo dışında başka satır olmaz. -->

| Bulgu | Yanıt | Commit ya da neden |
|---|---|---|

## Açık sorular

<!-- Bir alt ajanın her açık sorusu "taşındı: <yer>" veya "düştü: <neden>" diye yazılır. Soru yoksa "yok" yazılır. -->

## Gerçek veri kanıtı

<!-- Son commit'ten sonra, temiz ağaçta koşulan `kurulum\kapi.ps1` çıktısını yapıştırın. Çıktıda `kapi: driftlint -> 0` satırı bulunur. CI, `kapi:` satırlarını ve HEAD sha'sını denetler. CI, dal adının `pr/<ad>` biçiminde olmasını da arar (küçük harf, rakam, tire). Tam olarak bir kapi koşusu yapıştırın. Kod değiştiyse tam koşu gerekir, `-Belge` olmaz. -->

```
```
