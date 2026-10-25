# Task Scheduler (Görev Zamanlayıcı)

## Inspect the current state

Read the installed tasks with `Get-ScheduledTask -ErrorAction Stop | Where-Object { $_.TaskName -like 'Tansu*' }`.
Record the output and date before stating which tasks exist. Repository definitions do not prove installation.
If the command fails, report the state as unknown and retain the error.
The standing coordinator does not install scheduler tasks. See [Standing project coordinator](yonetici.md#durable-work).

## Definitions

The repository has two task definitions:

- `TansuGunluk` uses `kurulum/tansu-gunluk.xml` and `python -m tansu gunluk`.
- `TansuAylik` uses `kurulum/tansu-aylik.xml` and `python -m tansu evren-indir`.

TASARIM §6 owns the times. The paths point to the main repository on this machine (`C:\Users\levent\Desktop\TANSU`).
Both definitions start disabled through `<Enabled>false</Enabled>`.

## Change a task

Get Levent's specific approval before installing, changing, enabling, or deleting a task.
For an approved installation, use PowerShell because `schtasks /create /xml` cannot read UTF-8 XML.
For the daily definition, run `Register-ScheduledTask -TaskName TansuGunluk -Xml (Get-Content -Raw -Encoding utf8 kurulum\tansu-gunluk.xml)`.
For the monthly definition, use `TansuAylik` and `kurulum\tansu-aylik.xml` in that command.
For approved enabling, run `schtasks /change /tn TansuGunluk /enable`.
For approved deletion, run `schtasks /delete /tn TansuGunluk /f`.
Use `TansuAylik` for the corresponding monthly operation. Inspect the task again after the approved operation.
