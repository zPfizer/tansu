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
| a-17 `docs/denetim.md:10` yanlış kabul | `docs/denetim.md` son paragraf; TASARIM §5.12 "Yanlış kabul" (ölçüt 1–4 + portföy kuralı reddetmedi). Kod (`tansu/denetim.py:158`) tanımla uyumlu, yalnız belge cümlesi portföy koşulunu atlıyordu | düzeltildi (belge tarafı): tanım TASARIM §5.12'ye atıf, portföy koşulu eklendi. Açık: üretici `tansu/denetim.py:281–288` eski cümleyi yeniden yazar, bilet 07'ye |
| a-18 "tek aday" gerekçesi | `docs/KURALLAR.md` §4 "Kural" ve "bilet 05 ölçümü" maddesi; `docs/sadakat.md` EMA tabloları | düzeltildi: KURALLAR §4 eşdeğerlik ölçütü artık `sadakat.md` başındaki toleransa (±0,005) dayanır; nihai karar `sadakat.md`'ye yazılmadı (kod çıktısı, üretici bilet 07'ye) |
| a-19 `sabit_std` ve "yalnız t'ye kadar veri" | AGENTS'te bu kural yok artık; geleceği görmeme testinin kapsamı TASARIM §5.12'de açık liste (sadakat adayı değil); `sadakat.md` `sabit_std` Tansu'nun kaynak formülünü yeniden üretir | zaten düzeltildi (harness hizası 14.10: kural AGENTS'ten çıktı; kapsam listesi açık) |
| a-20 `Status:` sözleşmesi | `docs/agents/issue-tracker.md` yeni "Status field"; `docs/agents/triage-labels.md` yalnız rol metinleri, bölüme atıf | düzeltildi: sahip issue-tracker; uygulama (`claimed`, `in-review`, `done (PR #N, hash)`, `resolved`) yazıldı; kapalı = `done`/`resolved` ile başlar (bilet 05, 14.10) |
| a-25 belge koddan önce | AGENTS satır 3–4 (sahip); TASARIM başı | düzeltildi: TASARIM'daki tam kural "Çalışma kuralı (belge koddan önce gelir): `AGENTS.md`." atfına döndü |
| a-26 deneme günlüğü / git durumu | düzeltildi (tur 1): AGENTS "Trial log" maddesi kaldırıldı; "Git" maddesi AGENTS'te kalır ve günlük kurallarını TASARIM §5.11'e bırakır. TASARIM §5.11 (693–694) de git durumunu söyler; önceki "TASARIM'da yok" cümlesi yanlıştı |
| a-27 getiriye bakma | AGENTS "Do not look at the return"; KURALLAR §4 (sahip); `sadakat.md:3` | düzeltildi (tur 1): AGENTS satırı salt atıf ("See `docs/KURALLAR.md` §4"). `sadakat.md:3` kod çıktısı (`tansu/sadakat.py:258–283`), elle düzenlenmedi, bilet 07'ye |
| a-28 aynı fonksiyon, geleceği görmeme, eksik gün | AGENTS'te yok artık; TASARIM §4 (`motor`), §5.1 "Eksik gün", §5.12 testi | zaten düzeltildi (harness hizası 14.10) |
| a-29 19:30 ve günlük komut | AGENTS "Task Scheduler" saat vermez ("The times are in TASARIM §6"); TASARIM §6.1 | zaten düzeltildi (harness hizası 14.10). Not: `kurulum/tansu-gunluk.xml` açıklaması ve `tests/test_gunluk.py` 19:30 içerir; kod/ayar dosyası, bu biletin kapsamı değil |
| a-30 `.scratch/` yeri | AGENTS "Plan" yalnız issue-tracker'a atıf verir | zaten düzeltildi (harness hizası 14.10) |
| a-31 triage etiket listesi | AGENTS'te liste yok; `triage-labels.md` tek yer | zaten düzeltildi (harness hizası 14.10) |
| d-40 TradingView ikinci kaynak | `veri-kaynaklari.md` §7 madde 1 | düzeltildi: "Geri çekildi, yerine: TASARIM §4 ve §5.1 'İkinci kaynak yok'" |
| d-41 sabit %25 eşiği | `veri-kaynaklari.md` §7 madde 2 | düzeltildi: "Geri çekildi, yerine: TASARIM §5.1 'Olay denetimi' (%0,5) ve 'Karantina'" |
| d-42 evren KAP üyeliğinden | `veri-kaynaklari.md` §7 madde 3 | düzeltildi: "Geri çekildi, yerine: TASARIM §5.2 'Evren kuralı'"; KAP çalışması ek karşılaştırma (§5.2, §8.2). Madde 4 (marj) için karar atfı: §5.1 "Fiyat limiti" |
| d-43 faiz önerisi | `veri-kaynaklari.md` §7 madde 5; §8 madde 6 | düzeltildi: "Geri çekildi, yerine: TASARIM §4 'Faiz' ve §8.9"; fonlama farkı belirsizliği §8.9'da açık |
| d-44 kalan bilinmeyenler | `veri-kaynaklari.md` §8 madde 1, 2, 5, 6 | düzeltildi: dört madde "Cevaplandı / Geçersiz" + TASARIM bölümü ile işaretlendi (§4, §8.1, §8.2, §8.9) |
| d-45 `rapor/kanit-20261005.md` | `rapor/` git dışı; ana depo diskinde dosya var | düzeltildi (tur 1: atıf "TASARIM giriş uyarısı, satır 15, C7"), **yalnız yerel disk** (git'e girmez): ilk satıra "Geçersiz ön deneme; rakamları hiçbir kararda kullanılmaz (TASARIM giriş uyarısı, satır 15, C7)" eklendi; rakamlar korundu. |
| d-48 `bosluk.csv` | `.scratch/arsiv/tansu-mvp/issues/16-kap-bist100.md:71` | düzeltildi: `docs/arastirma/bist100_kap_bosluk.csv` tam yol |
| d-49 kullanım koşulları tekrarı | `kullanim-kosullari-fiyat-adimi.md` §2 "Karar"; TASARIM §4 "Kullanım koşulları" | düzeltildi: §2 "tarihsel gerekçe, sahibi TASARIM §4 ve §5.1" notu; kanıt tablosu (§1) kaldı |
| d-50 fiyat adımı tablosu | TASARIM §5.1 "Fiyat adımı" (tek tablo, AGENTS tablosu sahibi TASARIM); araştırma notu §3 | düzeltildi: araştırma notundaki tablo kaldırıldı, TASARIM §5.1'e atıf; doğrulama sonuçları notta kaldı |


## PR şablonu

Tek değişiklik: "Definition of Done" başlığı altına bir satır: ölçütlerin sahibi `DEFINITION_OF_DONE.md`, aşağıdaki satırlar yalnız kanıt alanı (a-32 ile uyumlu).
`.github/dod_kontrol.py` başlıkları (`## Kabul ölçütleri`, `## Definition of Done`, `## Bağımsız inceleme` + `Denetçi:`/`Sonuç: geçti`,
`## Gerçek veri kanıtı`) ve kutu satırları aynen kaldı. Eklenen satır `_..._` biçimindedir; kutu değildir.

## Kapsam dışı notlar

- `hiza-a-istem.md` yeniden koşusu yapılmadı (kutu işaretsiz).

## Denetim tur 1 (Codex)

- A1 düzeltildi: `docs/KURALLAR.md` §4 eşdeğerlik ölçütü `sadakat.md` toleransına (±0,005) bağlandı; sadakat.md'ye karar yazılmadı.
- A2–A3 düzeltildi: issue-tracker `done (PR #N, hash)` (birleşti) ile `done (dal, kısa not)` (teslim edildi, birleşmedi) ayrıldı; triage-labels dört durumu saymaz, yalnız sözleşmeye atıf verir.
- A4 düzeltildi: AGENTS "Trial log" kaldırıldı, "Git" maddesi TASARIM §5.11'e atıf verir; rapor satırı a-26 düzeltildi.
- A5 düzeltildi (AGENTS salt atıf); `docs/sadakat.md:3` Bilet 07'ye (üretici `tansu/sadakat.py:258–283`).
- A6 düzeltildi: `CODING_STANDARDS.md` `## Tansu` yalnız kodlama yükümlülüğünü tutar, davranış TASARIM §4 ve §5.1'e atıfla; genel bölüm dokunulmadı.
- A7 Bilet 04'e (KURALLAR:138 ile sadakat:25 tekrarı; bilet 04 A13).
- A8 Bilet 04'e (GLOSSARY:11 ile KURALLAR:7,28 tekrarı; bilet 04 A11).
- A9 düzeltildi: iş akışı AGENTS "Fikir, kayıt"ta kalır; `docs/agents/domain.md` ona atıf verir.
- Üreticiler Bilet 07'ye (bilet 07 Comments, 14.10): `tansu/denetim.py:281–288` ve `tansu/sadakat.py:258–283`. Önceki "kod hash'i değişir" gerekçesi yanlıştı: `tansu/kayit.py:49` `denetim.py`'yi hash dışı tutar.
- d-45 düzeltildi: atıf "TASARIM giriş uyarısı (satır 15, C7)" (yalnız yerel dosya).
- Kutular: `hiza-a.md` 1–7, 17–20 kutusu açık bırakıldı (üretici `denetim.py`, bilet 07); kutu 4 açık.

## Bilet 04'e

- A7: `docs/KURALLAR.md:138` EMA ölçümleri ve çift aday sayıları `docs/sadakat.md:25` ile tekrar; KURALLAR yalnız karar + atıf tutsun.
- A8: `GLOSSARY.md:11` kaynak sınıfı/hazırlık tanımları `docs/KURALLAR.md:7,28` ile tekrar; anlamın sahibi GLOSSARY.

## Levent'e sorular

Yok. Kararlar (Status değerleri, eşdeğer aday) kodu ve davranışı değiştirmez; "(bilet 05, 14.10)" ile etiketlendi.

## Denetim tur 2 (Codex, 14.10)

- A2 düzeltildi: `issue-tracker.md` `done (kısa not)`; dal adı isteğe bağlı; bilet 06 örnek.
- A4 düzeltildi: `AGENTS.md` Git maddesi yalnız-ekleme kuralını tekrar etmez; TASARIM §5.11 atfı. Tur 1 satırı a-26 "düzeltildi" iddiası buna bağlıydı.
- A10 düzeltildi: `KURALLAR.md` eşdeğer aday cümlesindeki ölçüm rakamları kaldırıldı; `docs/sadakat.md` EMA tablosuna atıf.

## Denetim tur 3 (Codex, 14.10): KALDI; yeniden tanım 05b

- A4: `AGENTS.md` Git maddesi hangi klasörün izlendiğini TASARIM §5.11'e bırakır (05b tur 1: parantezdeki klasör listesi de kaldırıldı). Kalan: yalnız git komut yasakları, `veri/` silinmez, `kayit/` commit'te yalnız eklenir.
- Status: bilet 02 → `done (PR #5, 4c3199e)`, bilet 03 → `done (PR #8, c8a1d42)`, bilet 09 → `done (PR #7, 76a4da8)` (birleşme hash'leri `gh pr view`).
