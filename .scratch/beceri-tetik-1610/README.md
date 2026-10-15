# Beceri tetik eval: ilk örnek koşular (16.10)

Kurallar kalıcıdır: `.claude/skills/tansu-eval/SKILL.md` "Skill trigger eval". Bu klasör ilk eval setini ve iki örnek koşuyu tutar.
İki koşu da geçerli bir ölçü değildir. Sebepleri aşağıda.

## Dosyalar

- `sorgular.tsv`: 44 sorgu. Sütunlar: beklenen beceri, sorgu. Beceriler: `tansu-yeni-is`, `tansu-hata`, `tansu-belge`, `tansu-karar`, `tansu-eval` (her biri 8 sorgu) ve `yok` (4 sorgu, hiçbir beceri tetiklenmemeli).
- `ornek-kosu-1.tsv`: koşu 1 sonucu, 44 satır. Sütunlar: no, beklenen, tetiklenen, sorgu.
- `ornek-kosu-2.tsv`: koşu 2 sonucu, 42 satır (43 ve 44 numaralı sorgu yok). Aynı sütunlar.

`tetiklenen` sütunu, oturumdaki ilk Skill aracı çağrısının beceri adıdır. Çağrı yoksa `yok`.

## Koşu 1 (geçersiz)

- Ayar: `--allowedTools Skill`, `--max-turns 2`.
- Sorun: oturumlar beceriden önce Glob veya Bash ile keşfe başladı. Araç reddedildi ve oturum beceriye varmadan durdu.
- Sonuç (doğru/sorgu): yeni-is 3/8, hata 0/8, belge 3/8, karar 6/8, eval 7/8, yok 3/4.

## Koşu 2 (geçersiz)

- Ayar: `--allowedTools Skill Read Grep Glob`, `--max-turns 6`, sorgu başına 1 koşu, `--model` yok.
- 44 sonuçtan 42'si geldi (43 ve 44 eksik). Yanlış beceri tetiklenmedi.
- Sorun 1: birçok oturum beceri yüklemek yerine soru sordu veya reddedilen bir kabuk aracı kullandı.
- Sorun 2: global hook'lar oturumlara beyin bağlamı soktu. 9 numaralı sorguya oturum eval'in kendisi hakkında cevap verdi.
- Sonuç (doğru/sorgu): yeni-is 2/8, hata 1/8, belge 4/8, karar 7/8, eval 8/8, yok 2/2.

Sonuçlar bu yüzden bir tetik oranı göstermez. Kurulumun gürültüsünü gösterir.

## Koşu 2 komutu

Elle yazılmış bash döngüsü. Not: aşağıdaki metin koşunun parametrelerinden yeniden yazıldı. Koşu anındaki kabuk metni kaydedilmedi.
Depo köküne girilir ve `sorgular.tsv` satır satır okunur.

```bash
n=0
while IFS=$'\t' read -r beklenen sorgu; do
  n=$((n+1))
  claude -p "$sorgu" --allowedTools Skill Read Grep Glob --max-turns 6 \
    --output-format stream-json --verbose > "cikti-$n.jsonl"
  tetiklenen=$(grep -o '"name":"Skill","input":{"skill":"[^"]*"' "cikti-$n.jsonl" \
    | head -1 | sed 's/.*"skill":"//; s/"$//')
  printf '%s\t%s\t%s\t%s\n' "$n" "$beklenen" "${tetiklenen:-yok}" "$sorgu"
done < sorgular.tsv > ornek-kosu-2.tsv
```

## Olay (16.10)

İki örnek koşu salt okuma değildi. `--allowedTools` diğer araçları engellemedi. Oturumlar sorguları iş olarak yaptı: 22. ve 24. sorgu `.claude/skills/tansu-grill/SKILL.md` ile `.claude/agents/vekil.md` dosyalarını değiştirdi (`git restore` ile geri alındı), beyin Threads'e sahte bir vekil satırı yazıldı (YONETIM oturumu sildi, beyin 391b890). Önlem: `tansu-eval` "Skill trigger eval", "Sample first".

Koşu 2'de ek bir sorun daha var: döngüdeki `claude -p` sorgu dosyasının kalanını standart girdiden okudu ve isteğe ekledi. 43 ve 44 bu yüzden koşmadı. Önlem: `tansu-eval` "Runner" (`< /dev/null`).

## Yalıtılmış örnek (16.10, geçerli kurulum)

- Ayar: `tansu-eval` "Isolation". Atılabilir kopya `git worktree add --detach` ile (`%TEMP%\tansu-eval-kopya`), kopyanın `hooks` anahtarı silindi, `--settings '{"disableAllHooks": true}' --include-hook-events --disallowedTools "Bash PowerShell Edit Write NotebookEdit Agent" --allowedTools "Skill Read Grep Glob" --permission-mode default --strict-mcp-config --no-session-persistence --model claude-opus-5-5 --max-turns 6`, her çağrıda `< /dev/null`.
- Sorgu 22 (belge) ve 26 (karar), birer koşu. Araçlar: o22 Skill, Read, Skill, Skill; o26 Skill, Grep, Glob, Read×5, Grep. İlk beceri: `tansu-belge`, `tansu-karar` (ikisi de doğru).
- Hook olayı 0. Oturum araç listesinde yasak araç ve `mcp__` aracı yok. Kopyanın ve beynin `git status --porcelain` ile `git log -1` değeri önce ve sonra aynı.

## Tam ölçüm denemesi (16.10, durduruldu)

Bu sette 132 koşuluk ölçüm başladı ve YONETIM oturumu onu durdurdu (Levent onayı). Sebep: set gözden geçirilmedi, model yazdı, bir kısmı eskidi. Tamamlanan koşular sayılmaz. Yeni set: `sorgular-2.tsv`.

## Set 2 (`sorgular-2.tsv`)

Sütunlar: beklenen beceri, kaynak (`gercek` ya da `yazili`), sorgu. Gerçek istekler Levent'in Tansu ve YONETIM oturum dökümlerindeki kendi mesajlarıdır. Yazılanlar onun üslubundadır.

Setten çıkan sorgular ve sebepleri:
- "Günlük koşu dün çıkış kodu 1 verdi": zamanlanmış günlük görev kurulu değil. Elle `python -m tansu gunluk` koşusu olarak yeniden yazıldı.
- "TASARIM §5.8'deki hash kapsamı": §5.8 dönemleri anlatır. Bölüm numarası olmadan yazıldı.
- "Sınama motoruna komisyon maliyetini ekleyen bir özellik": masraf zaten TASARIM §5.4'te var.
- "Sinyal eşiğini 0,6 mı 0,7 mi yapalım": böyle bir eşik yok.
- "Rapordaki kazanç oranı yanlış": getiriye bakma kuralına (`KURALLAR.md` §4) yakın. İşlem sayısı hatasıyla değişti.
- "KAP duyurularını da çekelim": TASARIM'daki durumu doğrulanmadı. Bildirim özelliğiyle değişti.
- "Şu linki sakla", "Bu oturumu yeni bir oturuma devret": Tansu isteği değil. Levent'in gerçek devir isteğiyle değişti.

## Açık iş

1. Levent seti gözden geçirir (`tansu-eval` "Review the set").
2. Onaydan sonra `sorgular-2.tsv` ile sorgu başına 3 koşu. Kural: `tansu-eval` "Skill trigger eval".
