# Coding standards

The general coding rules are in the global `~/.claude/CLAUDE.md`. This file holds only the rules that real mistakes taught.

## Mistakes
This file starts short. It grows from real mistakes.
- When an agent makes a meaningful coding mistake, record it before the task ends. A mistake is meaningful when Levent corrects it, or when a review or CI finds it.
- For a mechanical mistake, add an automated check: a test, lint rule, hook, or CI step. Do not add a rule here. Examples: a code pattern, a banned API, a file location.
- For a judgement mistake, add one short rule here. Put a rule for one project only in the `CODING_STANDARDS.md` of that project.
- Write corrections to behavior or communication in Kurallar, not here.
- At the end of a difficult session, the user command `/retro` finds the mistakes that nobody recorded.

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
