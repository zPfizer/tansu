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
- Ortam: Windows, PowerShell. Python `.venv\Scripts\python.exe`. Ana dal `master`; uzak depo ve yedek yok.
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
- **Git:** `rebase`, `--amend`, `--force`, `reset --hard`, `git add .` ve `git add -A` yok; dosyalar adıyla
  eklenir. Veri (`veri/`) ve rapor çıktısı (`rapor/`) git'e girmez; `veri/` silinmez. `kayit/` git'e girer (günlüğün
  yalnız eklendiğinin kanıtı git geçmişidir); `kayit/` dosyalarını commit'te değiştirilmiş değil, yalnız
  eklenmiş olarak bırak.
- **Görev Zamanlayıcı:** tanım `kurulum/tansu-gunluk.xml` (hafta içi 19:30, `python -m tansu gunluk`). Kurulum, bir kez, PowerShell
  (`schtasks /create /xml` UTF-8 XML'i okuyamaz): `Register-ScheduledTask -TaskName TansuGunluk -Xml (Get-Content -Raw -Encoding utf8 kurulum\tansu-gunluk.xml)`.
  Tanım kapalı kurulur (`<Enabled>false</Enabled>`); ilk resmi koşudan sonra `schtasks /change /tn TansuGunluk /enable`
  (bilet 15). Kaldırma: `schtasks /delete /tn TansuGunluk /f`. Yollar bu makinedeki ana depoya (`C:\Users\levent\Desktop\TANSU`) bağlıdır.
- **Kural parametresi:** yalnız TASARIM/KURALLAR değişikliğiyle ve yeni deneme olarak değişir.
- **Bağımlılık:** yeni paket eklemeden önce TASARIM §4 ve stdlib'e bak. Eklenen paket `pyproject.toml`'a
  `==` ile yazılır.

## Agent skills

### Issue tracker

İşler `.scratch/` altında yerel markdown dosyalarıdır (uzak repo yok). See `docs/agents/issue-tracker.md`.

### Triage labels

Varsayılan beş rol: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: kökte `GLOSSARY.md`. ADR yok; kararlar `docs/TASARIM.md`'de, gerekçeleri `docs/sorgu/`'da. See `docs/agents/domain.md`.
