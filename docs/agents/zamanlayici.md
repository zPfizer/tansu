# Task Scheduler (Görev Zamanlayıcı)

- **Task Scheduler (Görev Zamanlayıcı):** No task is installed on this machine (Levent 16.10: the project is still in design).
  Two task definitions stay in the repository:
  `TansuGunluk` (`kurulum/tansu-gunluk.xml`, `python -m tansu gunluk`) and `TansuAylik` (`kurulum/tansu-aylik.xml`, `python -m tansu evren-indir`).
  The times are in TASARIM §6. The paths point to the main repository on this machine (`C:\Users\levent\Desktop\TANSU`).
  To install a definition again, use PowerShell (`schtasks /create /xml` cannot read UTF-8 XML):
  `Register-ScheduledTask -TaskName TansuGunluk -Xml (Get-Content -Raw -Encoding utf8 kurulum\tansu-gunluk.xml)`. The definition comes
  disabled (`<Enabled>false</Enabled>`); enable it with `schtasks /change /tn TansuGunluk /enable`. To delete a task: `schtasks /delete /tn TansuGunluk /f`.
