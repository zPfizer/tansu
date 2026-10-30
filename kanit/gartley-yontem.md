# Gartley yöntem işi: Tansu yöntemi ve AB=CD, ayrık hisse sınavı (30.10.2026)

İstek (Levent, 30.10.2026): Tansu yöntemiyle Gartley ya da AB=CD, boştaki paranın faizinden ayrı gerçek bir kazanç
veriyor mu? Ayar yalnız hisselerin üçte ikisinde, 2015-2022; sınav kalan üçte birde, bir kez.

## Sonuç: HAYIR

Ayrık grupta (185 hisse, 2015-2022, 100.000 TL) hiçbir aday üç geçme şartını birlikte tutmadı (k = 3, baraj
p < 0,0167). Yalnız nakit kasası 234.179 TL'dir.

| Aday | Sinyal düzeyi | Faiz geliri | İşlem kârı | En iyi üç olmadan | Son kasa | Nakitten fark | Karar |
|---|---|---|---|---|---|---|---|
| `gt-k` (Gartley, teyitli giriş, 10 gün süre stopu) | 2 dolum, ort. −0,21 R, p 1,00 | 132.521 | −5.353 | 0 | 227.168 | −7.011 | HAYIR |
| `abcd-k` (AB=CD, aynı giriş ve süre stopu) | 54 dolum, ort. 0,20 R, p 0,22 | 123.234 | 123.788 | −20.469 | 347.022 | +112.843 | HAYIR |
| `gartley` (dondurulmuş, bilgi; tam temiz değil) | 12 dolum, ort. 0,34 R, p 0,24 | 129.143 | 35.628 | −497 | 264.771 | +30.592 | HAYIR |

- `abcd-k` kasası nakdi geçti, ama kazanç üç işlemden geliyor: onlarsız işlem kârı eksidir ve sinyal düzeyi kazanç
  şanstan ayrılmıyor (p 0,22).
- `gt-k` teyit kuralları yüzünden 8 yılda 185 hissede yalnız 2 işlem açtı.

## Ölçümler (Adım 1)

- 29.10 seçiminin şans payı (148 ayar, bütün hisseler, 2015-2022, nakit üstü günlük getiri): seçilen ayarın yıllık
  Sharpe'ı 0,90 (148'de 19.). Ön kayıtlı tanımla Deflated Sharpe ≈ 0, PBO 0,28. Faizsiz 68 ayar dağılımı bozduğu
  için yalnız faizli 80 ayarla: Deflated Sharpe 0,67, PBO 0,77. İki okumada da seçim şanstan ayrılmıyor (eşik 0,95).
- Sahte oran sınaması (ayar grubu, kapı kapalı, 100 çekiliş, 30 geçerli): Gartley %86,7'lik dilimde; %95'i
  geçmedi. Geometrinin katkısı gösterilemedi.
- Basit geri çekilme kuralı (ayar grubu): 2.967 işlem, kasa 5.591 TL. Maliyet kazancı yiyor.
- Dondurulmuş Gartley sinyal düzeyi (ayar grubu): 39 dolum, ort. 1,13 R, p 0,048. Bu hisseler 29.10 ayarında
  kullanıldı; ayrık grupta aynı ölçü 0,34 R, p 0,24.

## Ayar grubu koşuları (Adım 2-3)

| Koşu | Sinyal düzeyi | Faiz | İşlem kârı | En iyi üç olmadan | Son kasa |
|---|---|---|---|---|---|
| `gt` (R/R kapısı 1,40) | 0 dolum | 134.179 | 0 | 0 | 234.179 |
| `gt-teyit` | 12 dolum, −0,15 R | 132.097 | −9.248 | −19.487 | 222.849 |
| `gt-k` (= `gt-teyit-sure`) | 12 dolum, −0,13 R | 132.661 | −6.859 | −17.098 | 225.802 |
| `abcd` (R/R kapısı 1,40) | 2 dolum | 133.544 | 21.613 | 0 | 255.157 |
| `abcd-k` | 102 dolum, 0,05 R, p 0,39 | 93.466 | −21.624 | −89.946 | 171.842 |
| `gartley` (bilgi) | 39 dolum, 1,13 R | 141.301 | 296.948 | 11.681 | 538.249 |

Değişiklik 1: teyitli girişte 1,40 R/R kapısı neredeyse hiç geçilmedi (13/13 ve 157/159 elendi); kapı kaldırıldı
(Levent'in "gerçek süzgeç yap ya da kaldır" talimatı). `abcd-k` ayar grubunda geçmediği için Kelebek eklenmedi.

## Dürüstlük kaydı

- Ön kayıt `plan.md` (8304d6d) koşulardan önce gönderildi; Değişiklik 1, okumalar (`okumalar.md`) ve `yontem.py`
  (SHA-256 `f9d682a1…9bde`) ayrık grupta hiçbir koşudan önce fe25da0 ile gönderildi.
- Ayrık grup listesi tohumlu rastgele seçildi (`hisse-gruplari.csv`, 371 ayar / 185 ayrık). Sınav her aday için bir
  kez koştu; kilit kayıtları `gartley-yontem/sinav/kilit-*.txt` (betik, grup listesi, faiz ve veri parmak izi).
- Her koşu `deneme-defteri.tsv` içinde bir satırdır (25 satır; 17-22 prova).
- Bağımsız inceleme: ayrı model aday kurallarını kendisi yazdı; `gt-teyit-sure` 12/12, `abcd-k` 101/102 işlem
  eşleşti; 9 kesim tarihinde 36 ileriye bakma karşılaştırması geçti. Sonuç NOTLU GEÇTİ; bulgular sınavdan önce
  düzeltildi ve prova ile sınandı.
- Sınırlar: dondurulmuş Gartley'in eski düğmeleri bütün hisselerle seçildiği için `gartley` satırı ayrık grupta tam
  temiz değildir. 2014-2015 düzeltilmiş tepe-dip verisi ham veriyle çoğu satırda uyuşmaz. Veride açılış fiyatı yok;
  giriş ve boşluk çıkışı ağırlıklı ortalama fiyattandır.
