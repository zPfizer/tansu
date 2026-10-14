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
| `docs/kurallar/A-yapi-bolge.md` … `E-risk-cikis-surec.md` | havuzun okuması: Tansu'nun ne dediği. Kural: havuzdaki her not burada atıflı ya da "kural içermez" listesinde olmalı |
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
- **Git (this repository only):** `rebase`, `--amend`, `--force` (ve `--force-with-lease`), `reset --hard`, `clean -f`, `branch -D`,
  `checkout .`, `restore .`, `git add .` ve `git add -A` yok (Claude için izin reddi engeller: `permissions.deny` global ve `.claude/settings.json`); dosyalar adıyla
  eklenir. Veri (`veri/`) ve rapor çıktısı (`rapor/`) git'e girmez; `veri/` silinmez. `kayit/` git'e girer (günlüğün
  yalnız eklendiğinin kanıtı git geçmişidir); `kayit/` dosyalarını commit'te değiştirilmiş değil, yalnız
  eklenmiş olarak bırak. This rule covers this repository only. The global Stop hook runs `git add -A -- receipts "*850-Companion*"` in the brain repository (`YONETIM/beyin`). That is outside this Tansu rule.
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
Tansu'nun ekidir. `tests/test_standartlar.py` genel kısmın YONETIM'deki asılla aynı kaldığını denetler.
`mattpocock-skills:code-review` reads both files. The CI without YONETIM skips the test. The check is in the local test gate.

## İş akışı
The work flow is in `C:\Users\levent\Desktop\YONETIM\AKIS.md` (flow A for code work). The Tansu additions:

**Geliştirme durdu:** belgeler drift, eski bilgi ve çelişkiden arınana kadar Tansu'nun davranışını değiştiren yeni
geliştirme yapılmaz; `.scratch/belge-hizasi/` biletleri ve çalışma düzeni işleri (`.scratch/yazilim-fabrikasi/`) yürür
(Levent 10.10). Bilet 08 bitince bu satır kalkar.

- **Fikir (idea):** In the step of flow A that sharpens the plan, call `/tansu-grill`. It is the Tansu version of `mattpocock-skills:grill-with-docs`. Tansu comes first. It scans the risk and shows the text that will change.
- **Fikir, kayıt (record):** Write a settled term to `GLOSSARY.md` at once. Write a decision to `docs/TASARIM.md`. Read TASARIM and `docs/sorgu/` first. Do not ask again for a decision that exists.
- **Plan:** The spec is `.scratch/<iş>/spec.md`. The tickets are `.scratch/<iş>/issues/NN-<ad>.md`. This is the own ticket layout of Tansu (`docs/agents/issue-tracker.md`). Do not write a ticket by hand. If a new decision appears during the work, update the spec first. Then `mattpocock-skills:to-tickets` builds the tickets again in dependency order.
- **Yapım (build):** Open a branch `pr/NN-<ad>` from `master` for each ticket. Commit to that branch. Clear the context between tickets.
- **PR:** Push the branch to `kaynak`. `mattpocock-skills:pr` and `.github/pull_request_template.md` write the PR body together. Do not merge the PR before two things are true.
- **PR, birleştirme (merge):** CI is green (`ci`: ruff, pytest. `dod`: PR body). An independent review says "geçti". The merge request of Levent is the approval. Merge with `gh pr merge --merge`.
- **Kapanış (close):** Move the spec and the tickets of a finished job to `.scratch/arsiv/`. Only GLOSSARY and TASARIM stay for good.

**Hata kaydı (error log):** Record each meaningful agent error at once, before the job ends. A meaningful error is a correction from Levent, a review finding, or a CI finding. A mechanical error goes to a test or a CI step. A reasoning error goes to `CODING_STANDARDS.md` under `## Tansu`. `mattpocock-skills:retro` records the ones that were missed at the close. `mattpocock-skills:code-review` applies these rules in the next job.

If Levent says "anlamadım", the agent calls `mattpocock-skills:wait-what`. The agent explains the answer again with the GLOSSARY terms and plain words.

## Agent skills

### Issue tracker

İşler `.scratch/` altında yerel markdown dosyalarıdır; GitHub issue kullanılmaz. See `docs/agents/issue-tracker.md`.

### Triage labels

Varsayılan beş rol: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: kökte `GLOSSARY.md`. ADR yok; kararlar `docs/TASARIM.md`'de, gerekçeleri `docs/sorgu/`'da. See `docs/agents/domain.md`.
