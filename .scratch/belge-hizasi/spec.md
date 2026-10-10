# Belge hizası: Tansu belgeleri birbiriyle ve kodla aynı şeyi söyler

Status: ready-for-agent

## Problem Statement

Tansu'da her iş belgelere göre yapılır: ajanlar AGENTS.md, GLOSSARY.md, TASARIM.md ve KURALLAR.md'yi okur ve uygular.
10.10'daki altı bağımsız denetim bu belgelerin birbirinden ayrıldığını gösterdi: yaklaşık 200 bulgu (çelişki, eski
bilgi, iki yerde yazılmış kural, eksik terim). TASARIM'daki yaklaşık 95 değişmez kuralın 28'i kodda ya da testte
korunmuyor. Levent belgelere güvenemezse ajanlar da yanlış kurala göre çalışır.

## Solution

Her bilgi tek sahip dosyada durur; öteki dosyalar yalnız atıf verir. Çelişkiler karar kayıtlarına
(`docs/sorgu/izleme/karar.md`, soru turları) göre düzeltilir; kayıt sessizse Levent'e sorulur. Mekanik olarak
denetlenebilen her kural bir teste ya da CI adımına bağlanır, böylece belge yeniden ayrılırsa CI kırmızı olur.

## User Stories

1. Levent olarak, sözlükteki her terimin TASARIM'daki anlamla aynı olmasını istiyorum; böylece ajanın sözünü yanlış anlamam.
2. Levent olarak, bir kuralın yalnız bir dosyada yazılı olmasını istiyorum; böylece bir yeri düzeltince öteki eskimez.
3. Levent olarak, verdiğim kararın TASARIM'a aynı anlamla geçmesini istiyorum; böylece ajan eski öneriyi uygulamaz.
4. Levent olarak, yalnız karar kayıtlarının sessiz kaldığı çelişkilerin bana sorulmasını istiyorum; böylece aynı kararı iki kez vermem.
5. Ajan olarak, TASARIM'daki her değişmez kuralın bir testi olmasını istiyorum; böylece kuralı bozan değişiklik CI'da durur.
6. Ajan olarak, kodun TASARIM'dan farklı davrandığı yerlerin bilinmesini istiyorum; böylece hata mı belge mi eksik, ayırabilirim.
7. Ajan olarak, araştırma ve eski rapor dosyalarında geri çekilmiş önerilerin işaretli olmasını istiyorum; böylece onları güncel karar sanmam.
8. Levent olarak, belge ayrılırsa bunun otomatik yakalanmasını istiyorum; böylece düzen kendiliğinden bozulmaz.

## Implementation Decisions

- Sahiplik: terimin anlamı GLOSSARY; sayı, formül ve davranış TASARIM; aile kuralı ve YORUM KURALLAR (§3–4);
  kaynak okuması `docs/kurallar/A–E`; sadakat ölçümü `docs/sadakat.md`; çalışma kuralı AGENTS.md; kod biçimi ve
  bitiş ölçütü CODING_STANDARDS.md / DEFINITION_OF_DONE.md `## Tansu`.
- Geçerli tasarım TASARIM.md (taslak 7). Taslak 8 ve strateji modülleri taslağı onay bekleyen öneridir; onlardaki
  farklar düzeltilmez, yalnız yanlış kaynak aktarımı düzeltilir.
- Karar kaydında cevabı olan çelişki o karara göre düzeltilir ve TASARIM'da karar etiketiyle (İ:, B-, C-, bilet) gösterilir.
- Kaynak görselinden okunan iki çelişkili sayı (G-125 stop 104,34/184,54; ICBCT ilk EMA 20/30) görsel açılarak çözülür.
- Kodun TASARIM'dan farklı davrandığı her yer `/diagnosing-bugs` ile ele alınır: önce davranışı kanıtlayan test, sonra
  karar (kod mu belge mi düzelir).
- Bulguların kaynağı `denetim/` altındaki altı rapordur. Raporlar 10.10 satır numaralarını taşır; düzeltmeden önce
  satır yeniden açılır.

## Testing Decisions

- Belge biletinin kanıtı: aynı denetim istemi (`denetim/hiza-*-istem.md`) o biletin kapsamında yeniden koşar ve
  yeni bulgu vermez; `pytest -q` ve driftlint temiz kalır.
- Kod biletinin kanıtı: kuralı dış davranıştan sınayan test; kural bozulunca kırmızı. Önceki örnek:
  `tests/test_kapilar.py`, `tests/test_gelecek.py`.
- Atıf testi: koddaki ve belgelerdeki `TASARIM <bölüm>` atıfları ve karar etiketleri var olan bir bölüme ya da
  karara gider. Önceki örnek: `tests/test_standartlar.py`.

## Out of Scope

- Taslak 8'deki yeni kuralların (iz süren stop, şok freni, üç hipotez) TASARIM'a alınması: mimari işinin
  (`.scratch/tansu-mimari/spec.md`) kararıdır.
- Kodu hiç olmayan dokuz kararın (Kâğıt dönemi, Canlı durumu vb.) yazılması: mimari işinin 5. adımıdır. Bu iş
  yalnız listeyi oraya bağlar.
- `docs/strateji-taslak/` ham kaynakları (defterler, ham yapıştırmalar): kural belgesi değildir.

## Further Notes

Denetim raporları: `denetim/hiza-a.md` (ajan belgeleri), `hiza-b.md` (TASARIM–GLOSSARY–KURALLAR), `hiza-c.md`
(KURALLAR ve kural dosyaları), `hiza-d.md` (biletler; bilet bulgularının çoğu MVP arşivlenince kapandı), `hiza-e.md`
(karar kayıtları), `tasarim-kod.md` (değişmez kurallar ve kod).
