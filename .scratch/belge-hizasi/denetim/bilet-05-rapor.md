# Bilet 05 raporu: ajan belgeleri, araştırma ve eski rapor (14.10.2026)

Yazar: Claude (Fable 5.1). Dal `pr/05-ajan-belgeleri`, taban `kaynak/master` c8a1d42. Bulgu satırları 10.10 tarihlidir;
AGENTS.md o günden beri yeniden yazıldı, TASARIM bilet 02, 03 ve 09'da değişti. Her satır bugünkü metne karşı sınandı.

Sonuç sayıları (27 satır): **düzeltildi 15, çürütüldü 0, zaten düzeltildi 12**.
Sıralama `hiza-a.md` 1–7, 17–20, 25–31, sonra `hiza-d.md` 40–45, 48–50.

| Kaynak satırı | Bugünkü yer | Yapılan |
|---|---|---|
| a-1 CSV başlıkları | AGENTS "Names"; TASARIM §6.5 "Sabit sütunlar" (ASCII) | zaten düzeltildi (bilet 03) |
| a-2 `veri/` silme | AGENTS "Git"; TASARIM §6.2 son madde ("Günlük anlık görüntüler silinmez") | zaten düzeltildi (bilet 03) |
| a-3 aylık görev | AGENTS "Task Scheduler"; TASARIM §6.2 (`TansuAylik`, ayın son günü 20:45) | zaten düzeltildi (bilet 03, harness hizası 14.10) |
| a-4 "uzak depo yok" | AGENTS "Environment" (`kaynak`, GitHub); `docs/agents/issue-tracker.md` eski gerekçe yok | zaten düzeltildi (harness hizası 14.10) |
| a-5 PR şablonu "getiriye bakılmadı" | `.github/pull_request_template.md`: koşulsuz getiri kutusu yok | zaten düzeltildi (harness hizası 14.10) |
| a-6 PR şablonu onay | şablon "Kabul ölçütleri": "Levent'in sohbetteki isteği onaydır" | zaten düzeltildi (harness hizası 14.10) |
| a-7 ADR / domain.md | `docs/agents/domain.md`: ADR klasörü yok, kararlar TASARIM'a; AGENTS "Fikir, kayıt" aynı | zaten düzeltildi (harness hizası 14.10) |
| a-17 `docs/denetim.md:10` yanlış kabul | `docs/denetim.md` son paragraf; TASARIM §5.12 "Yanlış kabul" (ölçüt 1–4 + portföy kuralı reddetmedi). Kod (`tansu/denetim.py:158`) tanımla uyumlu, yalnız belge cümlesi portföy koşulunu atlıyordu | düzeltildi: tanım TASARIM §5.12'ye atıf, portföy koşulu eklendi (bilet 05, 14.10) |
| a-18 "tek aday" gerekçesi | `docs/KURALLAR.md` §4 "Kural" ve "bilet 05 ölçümü" maddesi; `docs/sadakat.md` EMA tabloları | düzeltildi: KURALLAR §4'e "eşdeğer aday tek aday sayılır" tanımı eklendi (son 3 yıl = son 2 yıl); nihai karar KURALLAR + sadakat tablolarına atıf. `sadakat.md` kod çıktısı olduğundan elle değişmedi |
| a-19 `sabit_std` ve "yalnız t'ye kadar veri" | AGENTS'te bu kural yok artık; geleceği görmeme testinin kapsamı TASARIM §5.12'de açık liste (sadakat adayı değil); `sadakat.md` `sabit_std` Tansu'nun kaynak formülünü yeniden üretir | zaten düzeltildi (harness hizası 14.10: kural AGENTS'ten çıktı; kapsam listesi açık) |
| a-20 `Status:` sözleşmesi | `docs/agents/issue-tracker.md` yeni "Status field"; `docs/agents/triage-labels.md` yalnız rol metinleri, bölüme atıf | düzeltildi: sahip issue-tracker; uygulama (`claimed`, `in-review`, `done (PR #N, hash)`, `resolved`) yazıldı; kapalı = `done`/`resolved` ile başlar (bilet 05, 14.10) |
| a-25 belge koddan önce | AGENTS satır 3–4 (sahip); TASARIM başı | düzeltildi: TASARIM'daki tam kural "Çalışma kuralı (belge koddan önce gelir): `AGENTS.md`." atfına döndü |
| a-26 deneme günlüğü / git durumu | AGENTS "Trial log"; TASARIM §5.11 (günlük, yalnız ekleme). "Git" maddesindeki `veri/`, `rapor/`, `kayit/` git durumu TASARIM'da yok, sahibi AGENTS | düzeltildi: "Trial log" TASARIM §5.11'e atıf + yalnız yasak; "Git" maddesi AGENTS'te kaldı (başka sahip yok) |
| a-27 getiriye bakma | AGENTS "Do not look at the return"; KURALLAR §4 (sahip); `sadakat.md:3` | düzeltildi: AGENTS satırı KURALLAR §4'e atıf verir. `sadakat.md:3` "Getiriye bakılmaz." kod çıktısıdır (`tansu/sadakat.py`), kural değil durum cümlesi; dokunulmadı |
| a-28 aynı fonksiyon, geleceği görmeme, eksik gün | AGENTS'te yok artık; TASARIM §4 (`motor`), §5.1 "Eksik gün", §5.12 testi | zaten düzeltildi (harness hizası 14.10) |
| a-29 19:30 ve günlük komut | AGENTS "Task Scheduler" saat vermez ("The times are in TASARIM §6"); TASARIM §6.1 | zaten düzeltildi (harness hizası 14.10). Not: `kurulum/tansu-gunluk.xml` açıklaması ve `tests/test_gunluk.py` 19:30 içerir; kod/ayar dosyası, bu biletin kapsamı değil |
| a-30 `.scratch/` yeri | AGENTS "Plan" yalnız issue-tracker'a atıf verir | zaten düzeltildi (harness hizası 14.10) |
| a-31 triage etiket listesi | AGENTS'te liste yok; `triage-labels.md` tek yer | zaten düzeltildi (harness hizası 14.10) |
| d-40 TradingView ikinci kaynak | `veri-kaynaklari.md` §7 madde 1 | düzeltildi: "Geri çekildi, yerine: TASARIM §4 ve §5.1 'İkinci kaynak yok'" |
| d-41 sabit %25 eşiği | `veri-kaynaklari.md` §7 madde 2 | düzeltildi: "Geri çekildi, yerine: TASARIM §5.1 'Olay denetimi' (%0,5) ve 'Karantina'" |
| d-42 evren KAP üyeliğinden | `veri-kaynaklari.md` §7 madde 3 | düzeltildi: "Geri çekildi, yerine: TASARIM §5.2 'Evren kuralı'"; KAP çalışması ek karşılaştırma (§5.2, §8.2). Madde 4 (marj) için karar atfı: §5.1 "Fiyat limiti" |
| d-43 faiz önerisi | `veri-kaynaklari.md` §7 madde 5; §8 madde 6 | düzeltildi: "Geri çekildi, yerine: TASARIM §4 'Faiz' ve §8.9"; fonlama farkı belirsizliği §8.9'da açık |
| d-44 kalan bilinmeyenler | `veri-kaynaklari.md` §8 madde 1, 2, 5, 6 | düzeltildi: dört madde "Cevaplandı / Geçersiz" + TASARIM bölümü ile işaretlendi (§4, §8.1, §8.2, §8.9) |
| d-45 `rapor/kanit-20261005.md` | `rapor/` git dışı; ana depo diskinde dosya var | düzeltildi, **yalnız yerel disk** (git'e girmez): ilk satıra "Geçersiz ön deneme; rakamları hiçbir kararda kullanılmaz (TASARIM §1, C7)" eklendi; rakamlar korundu. Not: TASARIM'da bu hüküm §1'de değil belge başındaki kalın paragraftadır |
| d-48 `bosluk.csv` | `.scratch/arsiv/tansu-mvp/issues/16-kap-bist100.md:71` | düzeltildi: `docs/arastirma/bist100_kap_bosluk.csv` tam yol |
| d-49 kullanım koşulları tekrarı | `kullanim-kosullari-fiyat-adimi.md` §2 "Karar"; TASARIM §4 "Kullanım koşulları" | düzeltildi: §2 "tarihsel gerekçe, sahibi TASARIM §4 ve §5.1" notu; kanıt tablosu (§1) kaldı |
| d-50 fiyat adımı tablosu | TASARIM §5.1 "Fiyat adımı" (tek tablo, AGENTS tablosu sahibi TASARIM); araştırma notu §3 | düzeltildi: araştırma notundaki tablo kaldırıldı, TASARIM §5.1'e atıf; doğrulama sonuçları notta kaldı |


## PR şablonu

Tek değişiklik: "Definition of Done" başlığı altına bir satır: ölçütlerin sahibi `DEFINITION_OF_DONE.md`, aşağıdaki satırlar yalnız kanıt alanı (a-32 ile uyumlu).
`.github/dod_kontrol.py` başlıkları (`## Kabul ölçütleri`, `## Definition of Done`, `## Bağımsız inceleme` + `Denetçi:`/`Sonuç: geçti`,
`## Gerçek veri kanıtı`) ve kutu satırları aynen kaldı. Eklenen satır `_..._` biçimindedir; kutu değildir.

## Kapsam dışı notlar

- `tansu/denetim.py:281` aynı eski cümleyi (`docs/denetim.md` üreticisi) üretir; kod ve kod hash'i değişeceği için dokunulmadı. Belge ilk satır yeniden üretilirse eski cümle geri gelir; ilk resmi koşu tamamlandığı için denetim yeniden koşmaz.
- `docs/sadakat.md` kod çıktısıdır; elle düzenlenmedi.
- `hiza-a-istem.md` yeniden koşusu yapılmadı (kutu işaretsiz).

## Levent'e sorular

Yok. Kararlar (Status değerleri, eşdeğer aday) kodu ve davranışı değiştirmez; "(bilet 05, 14.10)" ile etiketlendi.
