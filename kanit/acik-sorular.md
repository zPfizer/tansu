# Açık sorular ve kayıtlar

Ajan bu dosyaya yazar; Levent'in kararı gereken sorular "Levent" ile işaretlidir.

## Levent kararı bekleyenler

1. Levent, Ek B #12 (kamu deposu içeriği): kural kartları, Tansu alıntıları, tweet kimlikleri ve `docs/SPEC.md` yerelde kalıyor. Seçenekler: (a) yerelde kalsın, (b) depo gizli olsun ve bunlar commit edilsin.
2. Levent, Git geçmişi: PR 197'nin bir commit'i `tansu/gostergeler.py` içinde Tansu kodundan kısa bir parça taşıyor; bugünkü dosya temiz. Geçmişi temizlemek ortak dalda zorla itme (force-push) ister; Levent'in ayrı onayı gerekir.
3. Levent, `stratejiler/sahip-kararlari.md` 13. satır hâlâ "AÇIK" diyor; ajan bu dosyayı değiştirmez. Ek B #13 kararı aşağıdaki "Verilen kararlar" bölümündedir.
4. Levent, `stratejiler/sahip-kararlari.md` 6. satır "Çift evreni: BIST 30" diyor; 28.10 evren kararından sonra bütün BIST olmalı. Ajan bu dosyayı değiştirmez.

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

Levent 29.10.2026: "bana olan soruların en mantıklı ve global olarak kabul edilmiş standartlarda". Evren işinin dört sorusu yaygın backtest uygulamasına göre karara bağlandı:

- Bozuk gün (fiyatı 0 ya da yüksek/düşük/AOF tutarsız satır; bütün BIST'te 287 sembolde 8.311 gün) eksik gün sayılır: o gün hesap fiyatı yok, emir dolmaz, çıkış ertesi geçerli güne kayar; karantina kuralı değişmez. Gerekçe: backtest motorları (LEAN, Zipline) geçersiz çubukta dolum yapmaz, onu eksik veri sayar. Eski TASARIM 5.13 (#188) karantina fiyatını koruyordu; bütün BIST'te bu, AOF 0'dan dolumla `tansu ayarla`'yı sıfıra bölmede çökertti (ölçüm `kanit/evren.md`). Durum: uygulandı (`veri.Anlik.hesap_fiyati`).
- Eksik günden sonra ATR: fiyatlı 14 çubuğun basit ortalaması; eksik gün atlanır. Gerekçe: Wilder'ın ATR'si çubuk başınadır, işlem olmayan gün çubuk değildir. Bütün BIST'te günlerin %3,6'sında ATR yoktu. ATR'si yine tanımsız günde (listelenmenin ilk 13 çubuğu) stoplu kurulum girmez, "ATR tanımsız" sayılır (SPEC 5.2, 3.4). Durum: uygulandı (`gostergeler.atr_basit`, `islem`).
- Akşam sinyali kapsamı (SPEC 6 adım 2): bütün BIST, sınanan evrenle aynı. Gerekçe: canlı sinyalin evreni sınamanın evreniyle aynı olmazsa sınama canlıyı temsil etmez. Durum: `tansu tara` 9. fazda yapılacak.
- Likidite tabanı: yok. Gerekçe: Levent'in 28.10 kararı bütün evreni ister ve Tansu bütün BIST'i tarar. Endekslerin likidite elemesi (MSCI ve benzerleri) büyük tutarın alınıp satılabilmesi içindir; program adet ve tutar vermez. Sığ hisse riski SPEC 5.6 sembol tablosu ve %40 uyarısında görünür. Gartley ölçümünde kazanç her likidite basamağında artıydı (`kanit/faz5.md`).

- Ek B #13 (`gartley` R/R kapısı), Levent 28.10.2026: "tansunun dediği gibi yap". Kapı Tansu'nun yazılı kuralıyla uygulanır: ödül hedef1'e, risk stopa göre ölçülür; oran 1,5'in altındaysa kurulum alınmaz. `rr_min` varsayılanı 1,5; elle verilebilen değerler kapalı, 1,5, 2 (ızgarada değil). Stop X iken oran her Gartley'de ≈ 1,40, X − 2 ATR iken daha düşüktür; bu yüzden `gartley` varsayılan ayarla hiç kurulum üretmez. Tansu'nun tarama tablolarında bu kurala uymayan kurulumlar var; kural metni esas alındı. Durum: uygulandı (kanıt `kanit/faz5.md`).

Levent 28.10.2026: "Tansuya göre cevaplanması gerekiyor bu soruların". Gartley teşhisindeki sorular Tansu'nun kendi metinleriyle cevaplandı (alıntılar yerel kayıtta, Ek B #12 ara kuralı):

- Gartley R/R kapısı açık kalır. 02.12.2025 kuralı, teknik olarak doğru formasyonun da 1,5 altında işleme alınmadığını açıkça söyler; tarama tablosunun (23.08.2026) bir formasyonu listelemesi bu kurala aykırı değildir, tabloda risk adımı yoktur. Tansu'ya göre çözüldü.
- Gartley dedektörü değişmez. Yazılı kural (02.12.2025: X ve A dip/tepe, D'de 0,786 alış limiti, stop X, hedefler AD'ye göre) bugünkü dedektördür; Tansu 22.08.2026'da kodunu iki görüşe göre yazdığını, 25.08.2026'da bunların Carney ve daha esnek Pesavento olduğunu söyler. Kapanış fiyatlı eski tarayıcının (2024-2025) yazılı kuralı yoktur, eklenmez. Pesavento oranlarını Tansu vermez: Tansu'ya göre çözülmedi, yapılmaz.
- Genel R/R kapısı (Levent'in 16.10 tarihli "en az 1:2" kararı, eski site issue'su #164): Tansu'nun genel sözü (25.11.2025) uygun oranı tercih etmektir, her stratejiye tek sert eşik koymaz; stratejiye özel kural (Gartley 02.12.2025) kendi stratejisinde uygulanır. Genel `rr-kapisi` süzgeci SPEC'teki gibi kalır: hedef1'e göre, 0 / 1,5 / 2 / 3, varsayılan kapalı, 12+. aşamada sınanır. Tansu'ya göre çözüldü.
- Gartley teyit süzgeçleri (yutan boğa, RSI 50 üstü, artan hacim, X-B çizgisi kırılımı, 10 günlük tepki) şimdi yapılmaz. Yazılı girişte (02.12.2025) teyit adımı yoktur; 09.12.2025, 23.08.2026 ve 25.08.2026 gönderileri bunları bir kurulumun anlatımı ya da girişten sonraki durum etiketi olarak verir. SPEC 11 madde 1'deki seçenekler olarak 12+. aşamada kalır. Tansu'ya göre çözüldü.