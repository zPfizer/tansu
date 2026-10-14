# Coding standards

The general coding rules are in the global `~/.claude/CLAUDE.md`. This file holds only the rules that real mistakes taught.

## Mistakes
This file starts short. It grows from real mistakes.
- When an agent makes a meaningful coding mistake, record it before the task ends. A mistake is meaningful when Levent corrects it, or when a review or CI finds it.
- For a mechanical mistake, use an existing tool first: `permissions.deny` or a git check. Write a new script only when the same mistake repeats and no existing tool covers it. Do not write a Claude hook. Do not add a rule here.
- For a judgement mistake, add one short rule here. Put a rule for one project only in the `CODING_STANDARDS.md` of that project.
- Write corrections to behavior or communication in Kurallar, not here.
- At the end of a difficult session, the session review in `AKIS.md` (flows B and I) finds the mistakes that nobody recorded.

## Rules
- **Fail loud:** Stop with an error and a non-zero exit when the code cannot complete the requested operation. Do not continue in a weaker mode. (05.10: Tansu `kayit.py` changed an official run to a development run on a dirty tree. 07.10: a hook exited 0 on errors. 07.10: an eval script ignored a subprocess exit code.)
- **Check every item:** Check every record and each required item by its identity. (05.10: Tansu `kaynak.py` checked only the first record. 10.10: Tansu `dod_kontrol.py` checked a count only. 10.10: a git hook matched raw JSON instead of the parsed command.)
- **A check needs the work:** Make the check fail when the required work is missing. (09.10: a PDF reading tool stored the answer codes in the manifest, so the check passed without opening the pages.)
- **One path to outside services:** Send every text to an external service through the same masking function. Check that the response comes from the expected model. (08.10: a hook sent raw text to Jev, bypassed the shared masking function, and did not check the model.)
- **Jev uses the official path only:** Call Jev only through the official TypeSafe service: provider `typesafe`, address `api.typesafe.ai`. Do not use Vercel, Laya, or another proxy. (Levent 14.10.)
- **Read the target before you dictate a fact:** Read the file first. Then write a fact about it into a job prompt or a callout. Use the claim of the file. (14.10: a prompt dictated "version 3.0" for a note whose line 13 said "v3.5.1 + 12 commits". The auditor failed the round.)
- **Sample before the full run:** Before a batch job runs on all items, run it on a sample. Read the distribution of the output. Then run the full set. (14.10: a tag job flagged 251 of 503 notes because of a loose flag rule. A 25-note sample would have shown it.)
- **Wire it and run it:** Connect each new hook, command, or module to the live path in the same change. Show one real run through that path. (07.10: a new hook was not in `settings.json`. 05.10: the Tansu CLI read result keys that the change removed.)

## Tansu
Genel standarda ektir. Davranış kuralının sahibi `docs/TASARIM.md`'dir; burada kod yazarken uygulanış biçimi durur.
- **Geleceği görmeme:** yeni ya da değişen her hesap `tests/test_gelecek.py` kapsamına eklenir (TASARIM §5.12).
- **Tek kod:** sınama ve canlı koşu aynı fonksiyonu kullanır; ayrı kopya yazılmaz (TASARIM §4).
- **Sessiz düzeltme yok:** eksik değer TASARIM §5.1'deki gibi boş kalır; tahminle doldurma, sessiz kırpma ve sessiz
  atlama yok. Beklenmeyen durum hata verir.
- **Belgeye bağlılık:** yeni ya da değişen her davranış kodda `TASARIM <bölüm>` atfı taşır.
- **Değişmez kural:** TASARIM'da bir şeyin hiç olmayacağını ya da hep olacağını söyleyen her hükmün (örnek:
  "anlık görüntü değişmez", "ileri doldurulmaz", "indirme durur") kodda bir uygulayıcısı ve bir testi vardır.
  Yeni hüküm ikisiyle birlikte gelir.
- **Tansu önce gelir:** bir kural, değer ya da tanım yazmadan önce Tansu havuzunda o konudaki fikrine bakılır. Fikri
  varken YORUM yazılmaz; uyulamıyorsa "uygulanamaz" ve nedeni yazılır (KURALLAR "Okuma kuralları"). (10.10: sözlükte
  11 yerde Tansu'nun fikri varken bizim seçimimiz Tansu'nunmuş gibi yazılmıştı.)
- **Atıf ver, kopyalama:** sahip dosyası başka olan sayı, formül ya da kural ikinci dosyaya yazılmaz; atıf verilir
  (AGENTS.md "Belgeler ve sahipleri"). (10.10: sözlük TASARIM'ın formüllerini yeniden yazmıştı.)
- **Olmayanı var gibi yazma:** belgeler yalnız bugün var olanı anlatır. Planlanan iş spec ve bilette durur; kurulunca
  belgeye girer.
