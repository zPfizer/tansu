# TANSU

Tansu'dan esinlenen BIST günlük sinyal ve sınama sistemi. Kod belgelere uyar; belge değişmeden davranış
değişmez.

## Okuma sırası
1. `GLOSSARY.md`: terimler.
2. `docs/TASARIM.md`: tasarım; §7 uygulama sırası.
3. `docs/KURALLAR.md`: aile kuralları, YORUM'lar, sadakat kontrolü.
4. Gerekirse `docs/sorgu/sonuc-3-4.md` ve `docs/sorgu/izleme/karar.md`: kararların gerekçesi.

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
- **Git:** `rebase`, `--amend`, `--force`, `reset --hard`, `git add .` ve `git add -A` yok (Claude için `.claude/hooks/block-dangerous-git.sh` engeller); dosyalar adıyla
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
Tansu'nun ekidir. `tests/test_standartlar.py` genel kısmın evdeki asılla aynı kaldığını denetler. `/code-review` ikisini
okur. Ek bölüm, Tansu kurallarının inceleme kaynağına girmesi için bu dosyadan oraya taşındı (10.10).

## İş akışı (Matt Pocock ana akışı)
Her iş bu sırayla yürür. Basamağı atlamadan önce o skill'in `SKILL.md`'sini oku.
1. **Fikir:** `/grill-with-docs`. Netleşen terim o anda `GLOSSARY.md`'ye, karar `docs/TASARIM.md`'ye yazılır.
   Önce TASARIM ve `docs/sorgu/`'ya bak; verilmiş kararı yeniden sorma.
2. **Plan:** iş birden çok oturum sürecekse `/to-spec`, sonra `/to-tickets`
   (`.scratch/<iş>/spec.md`, `.scratch/<iş>/issues/NN-<ad>.md`). Tek oturumluk işte doğrudan 3. adım.
3. **Yapım:** her bilet için `master`'dan `pr/NN-<ad>` dalı açılır. `/implement` biletin işini `/tdd` ile yapar,
   `/code-review` ile denetler, dala commit eder. Biletler arasında bağlam temizlenir.
4. **PR:** dal `kaynak`'a gönderilir; PR gövdesini `/pr` ve `.github/pull_request_template.md` birlikte yazar.
   CI (`ci`: ruff, pytest; `dod`: PR gövdesi) yeşil olmadan ve bağımsız inceleme "geçti" demeden PR birleşmez.
   Levent'in birleştirme isteği onaydır; birleştirme `gh pr merge --merge` ile yapılır.
5. **Kapanış:** `/retro` ortamı düzeltir: mekanik hata bir teste ya da CI adımına, muhakeme hatası kodlama
   standardına gider. Biten işin spec ve biletleri `.scratch/arsiv/`'e taşınır; kalıcı olan yalnız GLOSSARY ve TASARIM'dır.

Yan girişler: hata → `/diagnosing-bugs`, dışarıdan gelen istek → `/triage`, bakım → `/improve-codebase-architecture`.
Hepsi 3. adımdan akışa katılır.

## Agent skills

### Issue tracker

İşler `.scratch/` altında yerel markdown dosyalarıdır; GitHub issue kullanılmaz. See `docs/agents/issue-tracker.md`.

### Triage labels

Varsayılan beş rol: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: kökte `GLOSSARY.md`. ADR yok; kararlar `docs/TASARIM.md`'de, gerekçeleri `docs/sorgu/`'da. See `docs/agents/domain.md`.
