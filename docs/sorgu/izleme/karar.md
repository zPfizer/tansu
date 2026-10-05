# İzleme kararları (05.10.2026)

20 izleme ajanı, cevap dosyalarındaki bütün EKSİK, KARAR ve YANLIŞ maddelerini (1.561) taslak 6 ile
karşılaştırdı. Etiket sayıları grep ile sayıldı:

| Etiket | Sayı |
|---|---|
| VAR | 723 |
| TEKRAR | 204 |
| YENİ | 185 |
| RED | 449 |
| Toplam | 1.561 |

Karar veren Claude'dur. Kural:
- YENİ maddeler aşağıdaki istisnalar dışında kabul edildi ve taslak 7'ye işlendi.
- RED ve VAR maddeleri izleme dosyalarında gerekçeleriyle duruyor.

## Kabul edilmeyen ya da değiştirilen YENİ maddeler

| Madde | Öneri | Karar | Gerekçe |
|---|---|---|---|
| 20-006 | Kural parmak izi = `git rev-parse HEAD` | RED | İlgisiz her commit (belge düzeltmesi) yeni deneme sayılır ve Holm m'yi şişirir. C-6 (kod `ast.dump` + parametre hash'i) kalır. `git_commit` günlükte iz olarak yazılır (15-046). |
| 20-038 | Belge sessizse "dur, Levent'e sor" | RED | Levent soru cevaplamak istemiyor ve kararı Claude'a bıraktı. Kural "dur, önce belgeyi düzelt, gerekçeyi yaz" kalır. |
| 20-033 | Yeni paket yalnız Levent onayıyla | Kısmen | "Levent onayı" kısmı aynı gerekçeyle RED. Kabul edilenler: `reset --hard` yok, `veri/` silme yok, kural parametresi yalnız belge değişikliği + yeni deneme ile değişir. |
| 20-031 | `.scratch/` yerine `TODO.md` | RED | `.scratch/` düzenini mattpocock skill'leri okuyor (`docs/agents/issue-tracker.md`). İkinci bir iş listesi gereksiz. |
| 11-082 | Canlı etiketini Levent yazar | Değişti | Ölçütleri kod hesaplar. Durum değişikliği `kayit` tarafından yalnız-ekleme satırıyla yazılır. Para kararı yine Levent'indir. |
| 01-089 | Faiz serisi 60 günden eskiyse uyarı | Değişti | Seri yalnız değişim günlerini içerir; faiz aylarca sabit kalabilir, bu yüzden eşik yanlış alarm verir. Rapor yalnız serinin son değişim tarihini yazar. |
| 15-006 | Izgara tanımı hash dışı | Kısmen | Izgara sonuç görüldükten sonra değiştirilirse sağlamlık sınaması anlamsızlaşır. Bu yüzden ızgara tanımı kural kaydına (hash) girer (09-061). Tekrar sayısı, tohum ve blok uzunluğu hash dışıdır. |
| 09-062 | Sağlamlık eşiği %70 | Değişti | Eşik %60 olur. 04-089 ile ve 5.12.4'teki "yılların %60'ı" ile tutarlı. Sonuç görülmeden yazıldı. |

## Çakışan önerilerin birleştirilmesi
- **Isınma:** 250 gün (01-069, 03-068, 05-054, 07-065), 400 gün (19-017) ve en az 500 gün (06, cevap)
  önerildi. Karar:
  - Tek hisse ailesi, hissenin kendi ilk gününden 500 işlem günü dolmadan sinyal vermez. EMA200
    `adjust=False` ile bu kadar ısınır.
  - Çift ailesi 252 gün ister (04-094).
- **K2 dengeleme:** B-13 günlük maruziyet ağırlığı der; 03-065, 08-048 ve 09-019 ay başı dengeleme der.
  Karar:
  - Sepet ay başında evrenle eşit ağırlıklı kurulur ve %0,3 masraf öder.
  - Sepetin yatırımdaki payı her gün kuralın payına eşitlenir; bu eşitleme masrafsızdır (YORUM).
- **Kilitli tavan:** 01-026'nın kötümser tanımı ana kural olur: kapanışı tavanda olan gün giriş yok.
  B-5'in "düşük = yüksek" tanımı duyarlılık olur.
- **Tekrar sayısı:** 15-078 kabul. B ≥ max(1.000, 200·m), p = (1 + k) / (1 + B). Süre ölçülmedi;
  C-11 bütçesi aşılırsa önce algoritma hızlandırılır.
