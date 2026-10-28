# Açık sorular ve kayıtlar

Ajan bu dosyaya yazar; Levent'in kararı gereken sorular "Levent" ile işaretlidir.

## Levent kararı bekleyenler

1. Levent, Ek B #12 (kamu deposu içeriği): kural kartları, Tansu alıntıları, tweet kimlikleri ve `docs/SPEC.md` yerelde kalıyor. Seçenekler: (a) yerelde kalsın, (b) depo gizli olsun ve bunlar commit edilsin.
2. Levent, Git geçmişi: PR 197'nin bir commit'i `tansu/gostergeler.py` içinde Tansu kodundan kısa bir parça taşıyor; bugünkü dosya temiz. Geçmişi temizlemek ortak dalda zorla itme (force-push) ister; Levent'in ayrı onayı gerekir.
3. Levent, genel R/R kapısı (16.10 tarihli "en az 1:2" kararı, eski site issue'su #164): 28.10 cevabı ("tansunun dediği gibi yap") ajan tarafından şöyle okundu: Tansu'nun genel sözü uygun oranı tercih etmektir, her stratejiye sert eşik koymaz; genel `rr-kapisi` süzgeci SPEC'teki gibi kalır (hedef1'e göre, 0 / 1,5 / 2 / 3, varsayılan kapalı, 12+. aşamada sınanır). Onay bekliyor.
4. Levent, `stratejiler/sahip-kararlari.md` 13. satır hâlâ "AÇIK" diyor; ajan bu dosyayı değiştirmez. Ek B #13 kararı aşağıdaki "Verilen kararlar" bölümündedir.

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

- Ek B #13 (`gartley` R/R kapısı), Levent 28.10.2026: "tansunun dediği gibi yap". Kapı Tansu'nun yazılı kuralıyla uygulanır: ödül hedef1'e, risk stopa göre ölçülür; oran 1,5'in altındaysa kurulum alınmaz. `rr_min` varsayılanı 1,5; elle verilebilen değerler kapalı, 1,5, 2 (ızgarada değil). Stop X iken oran her Gartley'de ≈ 1,40, X − 2 ATR iken daha düşüktür; bu yüzden `gartley` varsayılan ayarla hiç kurulum üretmez. Tansu'nun tarama tablolarında bu kurala uymayan kurulumlar var; kural metni esas alındı. Durum: uygulandı (kanıt `kanit/faz5.md`).