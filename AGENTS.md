# TANSU

Tansu'dan esinlenen BIST günlük sinyal ve sınama sistemi. Kod belgelere uyar; belge değişmeden davranış
değişmez.

## Okuma sırası
1. `GLOSSARY.md`: terimler.
2. `docs/TASARIM.md`: tasarım; §7 uygulama sırası.
3. `docs/KURALLAR.md`: aile kuralları, YORUM'lar, sadakat kontrolü.
4. Gerekirse `docs/sorgu/sonuc-3-4.md`: kararların gerekçesi.

Belge ile kod çelişirse ya da belge sessizse dur: belgeyi önce düzelt, sonra kodu yaz.

## Çalışma kuralları
- Ortam: Windows, PowerShell. Python `.venv\Scripts\python.exe`. Ana dal `master`; uzak depo ve yedek yok.
- **Test kapısı:** commit öncesi `.venv\Scripts\python.exe -m pytest -q` yeşil olmalı.
- **Önce test:** önce kırmızı test, sonra en az kod. Testler yalnız TASARIM'daki yüzlerden.
- **Testi gevşetme yasak:** assert silmek, toleransı büyütmek, `skip`/`xfail` eklemek, beklenen değeri
  koda göre değiştirmek yasak.
  - Test yanlışsa önce gerekçeyi belgeye yaz.
  - Beklenen değerler elle hesaplanır, kodun yaptığı gibi yeniden hesaplanmaz.
  - Testte sabitler literal yazılır.
- **Getiriye bakma:** sadakat kontrolünde ya da YORUM seçerken getiri sonucu hesaplanmaz.
- **Deneme günlüğü:** her sınama koşusu `kayit/deneme.jsonl`'e yazılır. Günlük yalnız eklenir;
  düzenlenmez ve silinmez.
- **Git:** `rebase`, `--amend`, `--force` ve `git add .` yok. Veri (`veri/`) ve rapor çıktısı (`rapor/`)
  git'e girmez.
- **Bağımlılık:** yeni paket eklemeden önce TASARIM §4 ve stdlib'e bak. Eklenen paket `pyproject.toml`'a
  `==` ile yazılır.

## Agent skills

### Issue tracker

İşler `.scratch/` altında yerel markdown dosyalarıdır (uzak repo yok). See `docs/agents/issue-tracker.md`.

### Triage labels

Varsayılan beş rol: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: kökte `GLOSSARY.md`, kararlar `docs/adr/`. See `docs/agents/domain.md`.
