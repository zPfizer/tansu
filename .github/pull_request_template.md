## Ne değişti

Değişikliği bir veya iki cümleyle açıklayın.

Closes #<issue>
<!-- Numara, dalın issue'sunun numarasıdır. Birleştirmede GitHub issue'yu kapatır. CI bu satırı denetler (Kural 1). -->

## Kabul ölçütleri
_Kutuları Claude kanıtıyla işaretler. İşaretsiz kutu varsa PR birleşmez (Kural 2)._

- [ ]

## Gerçek veri kanıtı

<!-- Bu oturumda gerçek veriyle koşulan komutun çıktısını ve kurulum/kapi.ps1 çıktısını bir kod bloğuna yapıştırın (Kural 3). Test, biçim ve lint sonucunu ci iş akışı kanıtlar. -->

## Bağımsız inceleme

Denetçi: 
Denetlenen commit: 
<!-- Denetlenen commit, denetçinin okuduğu commit'in tam sha'sıdır (40 küçük harfli onaltılı hane). CI, bu sha PR başı değilse PR'ı reddeder (Kural 5). Tek istisna: sonraki commit'lerin hepsi taban dal birleştirmesiyse ve her birleştirme yalnız bu dalın değiştirmediği dosyaları getirip her dosyayı bir taraftan değişmeden alıyorsa CI kabul eder. -->
<!-- CI accepts exactly one Sonuç line, and only one of these three exact texts: "Sonuç: geçti", "Sonuç: GEÇTİ", "Sonuç: NOTLU GEÇTİ". CI rejects "Geçti", KALDI, and a second Sonuç line. -->
Sonuç: 
