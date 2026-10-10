# TANSU

Tansu'dan esinlenen BIST günlük sinyal ve sınama sistemi. Kod belgelere uyar; belge değişmeden davranış
değişmez.

## Belgeler ve sahipleri
Her bilginin tek sahip dosyası vardır; öteki dosyalar yalnız atıf verir. Okuma sırası tablonun sırasıdır.

| Dosya | Sahibi olduğu bilgi |
|---|---|
| `GLOSSARY.md` | terimlerin anlamı |
| `docs/TASARIM.md` | sayı, formül, davranış ve kararlar; §7 uygulama sırası |
| `docs/KURALLAR.md` | aile kuralları ve YORUM'lar (§3–4) |
| beyin: `kisisel/300-Projects/Tansu X Veri Havuzu/` (depo dışı) | Tansu'nun ham paylaşımları: not ve görsel. Ham kaynaktır, değiştirilmez |
| `docs/kurallar/A-yapi-bolge.md` … `E-risk-cikis-surec.md` (yerel, git dışı) | havuzun okuması: Tansu'nun ne dediği. Kural: havuzdaki her not burada atıflı ya da "kural içermez" listesinde olmalı |
| `docs/sadakat.md` | sadakat ölçümü |
| `AGENTS.md` | çalışma kuralı ve iş akışı |
| `CODING_STANDARDS.md`, `DEFINITION_OF_DONE.md` | kod biçimi ve bitiş ölçütü (`## Tansu`) |
| `docs/sorgu/sonuc-3-4.md`, `docs/sorgu/izleme/karar.md` (yerel, git dışı) | kararların gerekçesi (gerekirse okunur) |

Bu dosyaların hepsi drift denetimindedir: biri ötekiyle çelişirse, eski bilgi taşırsa ya da başka dosyanın
bilgisini kopyalarsa düzeltilir.

Belge ile kod çelişirse ya da belge sessizse dur: belgeyi önce düzelt, gerekçesini yaz, sonra kodu yaz.

## Çalışma kuralları
- Ortam: Windows, PowerShell. Python `.venv\Scripts\python.exe`. Ana dal `master`; uzak depo `kaynak` (GitHub, özel), başka yedek yok.
- Kurulum: `py -3.14 -m venv .venv`, sonra `.venv\Scripts\python.exe -m pip install -r requirements.lock.txt -e ".[dev]"`.
- **Adlar:** kod, dosya, sütun ve CSV başlığı adları Türkçe ASCII (`aile`, `adim`, `evren`); rapor ve kart
  metni Türkçe karakterli. Yollar `pathlib`; her dosya açıkça `encoding="utf-8"` ile açılır (CSV
  `utf-8-sig`).
- **Test kapısı:** commit öncesi `.venv\Scripts\python.exe -m pytest -q` yeşil olmalı. Testler ağa
  çıkmaz ve gerçek `kayit/` dosyalarına yazmaz (`tests/conftest.py` yolu `tmp_path`'e yönlendirir).
- **Önce test:** önce kırmızı test, sonra en az kod. Testler yalnız TASARIM'daki yüzlerden.
- **Testi gevşetme yasak:** assert silmek, toleransı büyütmek, `skip`/`xfail` eklemek, beklenen değeri
  koda göre değiştirmek yasak.
  - Test yanlışsa önce gerekçeyi belgeye yaz.
  - Beklenen değerler elle hesaplanır, kodun yaptığı gibi yeniden hesaplanmaz.
  - Testte sabitler literal yazılır.
- **Getiriye bakma:** sadakat kontrolünde ya da YORUM seçerken getiri sonucu hesaplanmaz.
- **Deneme günlüğü:** her sınama koşusu `kayit/deneme.jsonl`'e yazılır. Günlük yalnız eklenir;
  düzenlenmez ve silinmez.
- **Git:** `rebase`, `--amend`, `--force` (ve `--force-with-lease`), `reset --hard`, `clean -f`, `branch -D`,
  `checkout .`, `restore .`, `git add .` ve `git add -A` yok (Claude için `.claude/hooks/block-dangerous-git.sh` engeller); dosyalar adıyla
  eklenir. Veri (`veri/`) ve rapor çıktısı (`rapor/`) git'e girmez; `veri/` silinmez. `kayit/` git'e girer (günlüğün
  yalnız eklendiğinin kanıtı git geçmişidir); `kayit/` dosyalarını commit'te değiştirilmiş değil, yalnız
  eklenmiş olarak bırak.
- **Görev Zamanlayıcı:** tanım `kurulum/tansu-gunluk.xml` (hafta içi 19:30, `python -m tansu gunluk`). Kurulum, bir kez, PowerShell
  (`schtasks /create /xml` UTF-8 XML'i okuyamaz): `Register-ScheduledTask -TaskName TansuGunluk -Xml (Get-Content -Raw -Encoding utf8 kurulum\tansu-gunluk.xml)`.
  Tanım kapalı kurulur (`<Enabled>false</Enabled>`); ilk resmi koşudan sonra `schtasks /change /tn TansuGunluk /enable`
  (bilet 15). Kaldırma: `schtasks /delete /tn TansuGunluk /f`. Yollar bu makinedeki ana depoya (`C:\Users\levent\Desktop\TANSU`) bağlıdır.
  Aylık taban aynı yolla: `kurulum/tansu-aylik.xml` (ayın son günü 20:45, `python -m tansu evren-indir`), görev adı `TansuAylik`,
  kapalı kurulur, bilet 15'te `TansuGunluk` ile birlikte açılır.
- **Kural parametresi:** yalnız TASARIM/KURALLAR değişikliğiyle ve yeni deneme olarak değişir.
- **Bağımlılık:** yeni paket eklemeden önce TASARIM §4 ve stdlib'e bak. Eklenen paket `pyproject.toml`'a
  `==` ile yazılır.

## Standartlar
`CODING_STANDARDS.md` ve `DEFINITION_OF_DONE.md` Levent'in genel standardıyla başlar; altlarındaki `## Tansu` bölümü
Tansu'nun ekidir. `tests/test_standartlar.py` genel kısmın YONETIM'deki asılla aynı kaldığını denetler. `/code-review` ikisini
okur. YONETIM olmayan CI'da test atlanır; denetim yerel test kapısındadır.

## İş akışı (Matt Pocock ana akışı)
**Geliştirme durdu:** belgeler drift, eski bilgi ve çelişkiden arınana kadar Tansu'nun davranışını değiştiren yeni
geliştirme yapılmaz; `.scratch/belge-hizasi/` biletleri ve çalışma düzeni işleri (`.scratch/yazilim-fabrikasi/`) yürür
(Levent 10.10). Bilet 08 bitince bu satır kalkar.

Her iş bu sırayla yürür. Basamağı atlamadan önce o skill'in `SKILL.md`'sini oku. Bu skill'lerin çoğu kullanıcı
komutudur; ajan çağıramıyorsa `SKILL.md`'yi (`~/.claude/plugins/cache/mattpocock/`) okuyup adımlarını uygular.
1. **Fikir:** `/tansu-grill` (Matt'in `/grill-with-docs`'u Tansu ölçütleriyle: Tansu önce gelir, risk taraması,
   değişecek metni gösterme). Netleşen terim o anda `GLOSSARY.md`'ye, karar `docs/TASARIM.md`'ye yazılır.
   Önce TASARIM ve `docs/sorgu/`'ya bak; verilmiş kararı yeniden sorma.
2. **Plan:** her iş `/to-spec`, sonra `/to-tickets` ile planlanır (`.scratch/<iş>/spec.md`,
   `.scratch/<iş>/issues/NN-<ad>.md`). Bilet elle yazılmaz. İş sürerken yeni bir karar çıkarsa önce spec güncellenir,
   sonra `/to-tickets` biletleri bağımlılık sırasıyla yeniden kurar.
3. **Yapım:** her bilet için `master`'dan `pr/NN-<ad>` dalı açılır. `/implement` biletin işini `/tdd` ile yapar,
   `/code-review` ile denetler, dala commit eder. Biletler arasında bağlam temizlenir.
4. **PR:** dal `kaynak`'a gönderilir; PR gövdesini `/pr` ve `.github/pull_request_template.md` birlikte yazar.
   CI (`ci`: ruff, pytest; `dod`: PR gövdesi) yeşil olmadan ve bağımsız inceleme "geçti" demeden PR birleşmez.
   Levent'in birleştirme isteği onaydır; birleştirme `gh pr merge --merge` ile yapılır.
5. **Kapanış:** `/retro` ortamı düzeltir: mekanik hata bir teste ya da CI adımına, muhakeme hatası kodlama
   standardına gider. Biten işin spec ve biletleri `.scratch/arsiv/`'e taşınır; kalıcı olan yalnız GLOSSARY ve TASARIM'dır.

**Hata kaydı:** ajanın yaptığı her anlamlı hata (Levent'in düzeltmesi, inceleme ya da CI bulgusu) o anda, iş bitmeden
kaydedilir: mekanik hata bir teste ya da CI adımına, muhakeme hatası `CODING_STANDARDS.md` `## Tansu`'ya gider.
`/retro` kapanışta kaçanı tamamlar; `/code-review` bu kuralları sonraki işte uygular.

Yan girişler: hata → `/diagnosing-bugs`, dışarıdan gelen istek → `/triage`, bakım → `/improve-codebase-architecture`.
Hepsi 3. adımdan akışa katılır. Anlaşılmayan cevapta Levent `/wait-what` der: ajan cevabı GLOSSARY terimleriyle, sade
dille yeniden anlatır.

## Agent skills

### Issue tracker

İşler `.scratch/` altında yerel markdown dosyalarıdır; GitHub issue kullanılmaz. See `docs/agents/issue-tracker.md`.

### Triage labels

Varsayılan beş rol: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: kökte `GLOSSARY.md`. ADR yok; kararlar `docs/TASARIM.md`'de, gerekçeleri `docs/sorgu/`'da. See `docs/agents/domain.md`.
