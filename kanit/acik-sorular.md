# Açık sorular ve kayıtlar

Ajan bu dosyaya yazar; Levent'in kararı gereken sorular "Levent" ile işaretlidir.

## Levent kararı bekleyenler

1. Levent, Ek B #12 (kamu deposu içeriği): kural kartları, Tansu alıntıları, tweet kimlikleri ve `docs/SPEC.md` yerelde kalıyor. Seçenekler: (a) yerelde kalsın, (b) depo gizli olsun ve bunlar commit edilsin.
2. Levent, Git geçmişi: PR 197'nin bir commit'i `tansu/gostergeler.py` içinde Tansu kodundan kısa bir parça taşıyor; bugünkü dosya temiz. Geçmişi temizlemek ortak dalda zorla itme (force-push) ister; Levent'in ayrı onayı gerekir.
3. Levent, `stratejiler/sahip-kararlari.md` 13. satır hâlâ "AÇIK" diyor; ajan bu dosyayı değiştirmez. Ek B #13 kararı aşağıdaki "Verilen kararlar" bölümündedir.
4. Levent, likidite tabanı: bütün BIST'te çok az işlem gören hisseler de sınanır. Varsayılan: taban yok (Tansu bütün BIST'i tarar). Seçenek: önceki 60 günün ortanca TL hacmi bir tutarın altındaysa hisse o gün evren dışı. Gartley ölçümünde kazanç her likidite basamağında artıydı (`kanit/faz5.md`). Cevap gelene kadar taban yok.
5. Levent, akşam sinyali kapsamı (SPEC 6 adım 2): bütün BIST (varsayılan, sınanan evrenle aynı) ya da yalnız BIST 30. `tansu tara` henüz yok; cevap 9. faza kadar bekleyebilir.
6. Levent, `stratejiler/sahip-kararlari.md` 6. satır "Çift evreni: BIST 30" diyor; 28.10 evren kararından sonra bütün BIST olmalı. Ajan bu dosyayı değiştirmez.
7. Levent, bozuk gün (fiyatı 0 ya da yüksek/düşük/AOF tutarsız satır; bütün BIST'te 287 sembolde 8.311 gün): bekleyen emir ve açık işlem o gün ne yapsın? SPEC 5 bunu söylemez. Eski TASARIM 5.13 (#188) karantina gününün fiyatını korur; motor bugün o fiyattan dolum yapar, AOF 0 ise giriş 0 olur. Seçenekler: (a) eksik gün say: o gün fiyat yok, emir dolmaz, çıkış ertesi geçerli güne kayar; karantina aynen kalır (öneri; hazır dal `tum-bist-bozuk-atr`). (b) bugünkü gibi fiyat korunur. Etki ölçümü `kanit/evren.md`. Cevap gelene kadar (b).
8. Levent, eksik günden sonra ATR (bütün BIST'te günlerin %3,6'sında ATR yok): SPEC 3.12 ATR'yi "gerçek aralığın 14 günlük basit ortalaması" diye tanımlar, eksik günü söylemez. Bugün tek eksik gün ATR'yi 14 gün siler. Seçenekler: (a) eksik günü atla: ATR son 14 fiyatlı günün ortalaması (öneri; hazır dal `tum-bist-bozuk-atr`). (b) son geçerli ATR'yi taşı. (c) bugünkü gibi 14 gün ATR yok. Her seçenekte ATR'si olmayan günde stoplu kurulum girmez ve "ATR tanımsız" sayılır (SPEC 5.2 risk tabanı, 3.4). Etki ölçümü `kanit/evren.md`. Cevap gelene kadar (c).

## Gece 1 kayıtları (karar gerekmez)

- Faz 1: `.gitattributes` (satır sonu kuralı) ve `.claude/settings.json` (beyin kancaları, yasak git komutları) korundu; ayrıntı `kanit/faz1.md`.
- Faz 1: `psutil` doğrudan bağımlılıktan çıktı, `borsapy` üzerinden dolaylı kalıyor.
- Faz 2: ilk `tansu veri` koşusu tek bir İş Yatırım isteğinde 14 dakika ilerlemedi; durdurulup yeniden koşuldu. Kaynak yavaşken bir koşu yaklaşık 25 dakika sürüyor.
- Faz 3: `gartley` yalnız boğa (uzun) kurulumu üretir. Tansu'nun SOKE tablosundaki kısa satış yönü SPEC 11'e göre kapsam dışıdır; kaynak yerel kural kartında.

## Gece 2 kayıtları (karar gerekmez)

- İleri yürüme pencereleri sinyal tarihine göredir. SPEC 5.7 "giriş tarihi" der ama terimi tanımlamaz; SPEC 5.5 yalnız sinyal ve dolum tarihini tanımlar. Tansu'nun kaynaklarında pencere ataması yok. Sinyal tarihi kaldı (28.10.2026).
- 2021-2025 koşularında fiyat 31.12.2025'te kesilir; o gün açık kalan kurulum son kapanışta `açık` işaretlenir. SPEC 5.7 hem "kendi çıkışına kadar açık kalır" hem "saklı dönem ileri yürümede kullanılmaz" der; bu iki cümle 2025H2 için çelişir. Tansu'nun kaynaklarında dönem sonundaki açık işlem kuralı yok. Kesim kaldı (28.10.2026).
- Al-tut referansları (SPEC 5.6) henüz yapılmadı; SPEC 12'de bunlara sahip bir faz yok.

## Verilen kararlar

- Evren, Levent 28.10.2026: "Zaten tüm stratejilerimizi bütün bir evreninde deneyeceğiz." Bütün stratejiler bütün BIST'te sınanır: bugünkü KAP şirket listesi ve verinin başladığı 01.01.2019'dan beri işlemi kapanan kodlar; kapanan hisseler sınamada kalır (hayatta kalan yanlılığı yok). Kaynakta fiyatı olmayan kod işlem gören pay değildir, düşer. Bir sembol kaynakta satırı olan her gün evrendedir (`uye`). BIST 30 üyelik tablosu adlı katman olarak kalır. Sıra: (1) evren tanımı, (2) artımlı `tansu veri`, (3) ayrı işteki veri yolu kusurları, (4) bütün stratejilerde `tansu ayarla` yeniden, eski ve yeni sayılar `kanit/evren.md`. Saklı dönem ayara girmez. Durum: yapılıyor. SPEC (yerel) yaması SPEC sahibine verildi.

- Ek B #13 (`gartley` R/R kapısı), Levent 28.10.2026: "tansunun dediği gibi yap". Kapı Tansu'nun yazılı kuralıyla uygulanır: ödül hedef1'e, risk stopa göre ölçülür; oran 1,5'in altındaysa kurulum alınmaz. `rr_min` varsayılanı 1,5; elle verilebilen değerler kapalı, 1,5, 2 (ızgarada değil). Stop X iken oran her Gartley'de ≈ 1,40, X − 2 ATR iken daha düşüktür; bu yüzden `gartley` varsayılan ayarla hiç kurulum üretmez. Tansu'nun tarama tablolarında bu kurala uymayan kurulumlar var; kural metni esas alındı. Durum: uygulandı (kanıt `kanit/faz5.md`).

Levent 28.10.2026: "Tansuya göre cevaplanması gerekiyor bu soruların". Gartley teşhisindeki sorular Tansu'nun kendi metinleriyle cevaplandı (alıntılar yerel kayıtta, Ek B #12 ara kuralı):

- Gartley R/R kapısı açık kalır. 02.12.2025 kuralı, teknik olarak doğru formasyonun da 1,5 altında işleme alınmadığını açıkça söyler; tarama tablosunun (23.08.2026) bir formasyonu listelemesi bu kurala aykırı değildir, tabloda risk adımı yoktur. Tansu'ya göre çözüldü.
- Gartley dedektörü değişmez. Yazılı kural (02.12.2025: X ve A dip/tepe, D'de 0,786 alış limiti, stop X, hedefler AD'ye göre) bugünkü dedektördür; Tansu 22.08.2026'da kodunu iki görüşe göre yazdığını, 25.08.2026'da bunların Carney ve daha esnek Pesavento olduğunu söyler. Kapanış fiyatlı eski tarayıcının (2024-2025) yazılı kuralı yoktur, eklenmez. Pesavento oranlarını Tansu vermez: Tansu'ya göre çözülmedi, yapılmaz.
- Genel R/R kapısı (Levent'in 16.10 tarihli "en az 1:2" kararı, eski site issue'su #164): Tansu'nun genel sözü (25.11.2025) uygun oranı tercih etmektir, her stratejiye tek sert eşik koymaz; stratejiye özel kural (Gartley 02.12.2025) kendi stratejisinde uygulanır. Genel `rr-kapisi` süzgeci SPEC'teki gibi kalır: hedef1'e göre, 0 / 1,5 / 2 / 3, varsayılan kapalı, 12+. aşamada sınanır. Tansu'ya göre çözüldü.
- Gartley teyit süzgeçleri (yutan boğa, RSI 50 üstü, artan hacim, X-B çizgisi kırılımı, 10 günlük tepki) şimdi yapılmaz. Yazılı girişte (02.12.2025) teyit adımı yoktur; 09.12.2025, 23.08.2026 ve 25.08.2026 gönderileri bunları bir kurulumun anlatımı ya da girişten sonraki durum etiketi olarak verir. SPEC 11 madde 1'deki seçenekler olarak 12+. aşamada kalır. Tansu'ya göre çözüldü.