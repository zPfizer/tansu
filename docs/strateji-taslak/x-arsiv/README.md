# Tansu X arşivi (@The_Tansu_)

Çekim: 06–07.10.2026, `api.fxtwitter.com` (herkese açık veri). Levent'in isteği: tüm tweetler not edilsin, sonra
defterle karşılaştırılsın.

## Dosyalar

- `tweets.jsonl`: 8.785 gönderi (5.366 ana, 3.419 yanıt), 2023-08 → 2026-10-06. Alanlar: id, created_at, ts, text,
  reply_to, reply_to_user, quote_id, quote_user, quote_text, media (URL), note, likes, views. `kaynak: profil`
  olan 8 satır profil zaman tünelinden eklendi.
- `profil.jsonl`: profil zaman tüneli (779 gönderi, 2026-05-04 → 2026-10-06; X bu uçta daha eskisini vermiyor).
- `medya/`: kod adayı gönderilerin görselleri (`<id>-<sıra>.<uzantı>`); git'e girmez.

## Yöntem

1. Haftalık arama: `/2/search?q=from:The_Tansu_ since:<gün> until:<gün+7>`, sayfa sayfa (cursor), kimlikle tekil.
2. Kapsam denetimi: profil zaman tüneli ile karşılaştırma (2026-05 → 10): profildeki 777 gönderinin (683 ana, 94
   Tansu'nun kendi zincirine yanıt) 8'i aramada yoktu (%1); eklendi. Günlük aralık denemesi (2026-08-18 haftası): arama
   172 sonuç döndürdü, hepsi arşivde vardı (arşivde o UTC haftasında 150 gönderi var; aramanın gün sınırı UTC değil).
3. Metin tamlığı: arama `text` alanı uzun gönderiyi tam verir (R252: 5.266 karakter).

## Kapsam sınırı

Profil sayacı 15.326 der (X bu sayıya paylaşımları (repost), silinenleri ve yanıtları katar). Arşiv 8.785'tir; fark
≈6.500. Farkın ne kadarının paylaşım, silinmiş gönderi ya da aramanın döndürmediği yanıt olduğu bilinmiyor. Profil
gönderileri için ölçülen kapsam ~%99'dur (yalnız 2026-05 → 10 dönemi ölçülebildi). Haziran–Temmuz 2026'daki düşük
sayı profilde de vardır (16 ve 5 gönderi): gerçek.

## Sonraki adımlar

1. Kod gönderileri: görseldeki kod birebir yazıya geçer; 66 we.tl bağlantısı denenir.
2. Okuyarak sınıflama, 5'erli gruplar, iki bağımsız sınıflayıcı (Levent 07.10).
3. Defter (R001–R263) ile karşılaştırma: var / yeni / genişletir / çelişir.
