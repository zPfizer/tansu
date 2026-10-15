# Yazılım fabrikası: biletler GitHub'da, ajan GitHub Actions'ta

Status: ready-for-agent

Kaynak: Matt Pocock (Levent 10.10 paylaştı): GitHub Actions ile başlangıç fabrikası. Biletler issue olur; etiket bir
action'ı tetikler, action PR açar; action'lar etiket koyarak döngü kurar; zamanlı işler cron'la koşar; neyin bozulduğu
Actions ekranında görünür. Levent: "biz de böyle yapalım, workflowun uygun yerine ekleyelim."

## Problem Statement

Tansu'da her bilet bu makinedeki bir Claude oturumunda yürür. Levent bir oturum açıp işi başlatmadan hiçbir bilet
ilerlemez; biten işin ne olduğu da yalnız oturum dökümünde görünür.

## Solution

Biletler GitHub issue olur. Bir bilete `ready-for-agent` etiketi konunca GitHub Actions'ta bir Claude ajanı bileti
AGENTS.md iş akışıyla yapar ve PR açar. CI ve bağımsız inceleme PR'da koşar; sonuç etiketle geri bildirilir. Yerel
veriye ya da beyne ihtiyaç duyan bilet `yerel` etiketiyle bu makinede kalır.

## User Stories

1. Levent olarak, bir bileti yalnız etiketle başlatabilmek istiyorum; böylece oturum açmam gerekmez.
2. Levent olarak, açık işleri ve durumlarını GitHub'da tek listede görmek istiyorum.
3. Levent olarak, bir ajan koşusu bozulursa nedenini Actions ekranında görmek istiyorum.
4. Ajan olarak, Actions'ta da AGENTS.md'yi, standartları ve iş akışını okumak istiyorum; böylece yerelde ve bulutta aynı kurala uyarım.
5. Ajan olarak, bir PR'ın CI'ı kırmızıysa bunu etiketten görmek ve düzeltmek istiyorum; böylece döngü insan beklemeden döner.
6. Levent olarak, beyindeki Tansu havuzuna ya da gerçek veriye ihtiyaç duyan biletlerin bulutta yanlışlıkla koşmamasını istiyorum.
7. Levent olarak, Actions dakikalarının ve Claude kullanımının görünür kalmasını istiyorum; böylece sürpriz maliyet olmaz.
8. Levent olarak, birleştirmenin CI yeşil ve bağımsız inceleme "geçti" olmadan olmamasını istiyorum.

## Implementation Decisions

- İş takibi: GitHub Issues (Matt'in varsayılanı). `.scratch/` yalnız arşiv olarak kalır. Açık biletler issue'ya
  taşınır; tek takip yeri olur (iki takip yeri drift doğurur).
- Etiketler: Matt'in beş durum etiketi (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`)
  ve `yerel` (bulutta koşamaz: beyin havuzu, `veri/` ya da gerçek anlık görüntü gerekir).
- Ajan: `anthropics/claude-code-action`. Tetik: issue'ya `ready-for-agent` etiketi (girdi `label_trigger`), `yerel`
  etiketli issue atlanır. Ajan `pr/NN-<ad>` dalı açar, AGENTS.md iş akışının 3–4. adımlarını uygular, PR açar.
- Kimlik: Levent'in Claude aboneliği (Levent 10.10: "a"). Claude Code OAuth jetonu `claude setup-token` ile alınır,
  depo sırrı `CLAUDE_CODE_OAUTH_TOKEN` olur; ek ücret yok, abonelik kullanım hakkından harcar. Sırrı Levent kendisi
  girer; ajan jeton görmez ve yazmaz.
- Döngü: CI kırmızı bittiğinde bir `workflow_run` iş akışı etiketi koyar ve düzeltme ajanını aynı dalda çalıştırır (etiket durumu gösterir, tetik değildir; GITHUB_TOKEN ile konan etiket başka iş akışını tetiklemez); CI yeşil olunca etiket kalkar.
  Bağımsız inceleme ikinci bir ajan koşusudur (`/code-review`); sonucu PR yorumu ve `inceleme-gecti` etiketidir.
- Birleştirme: CI yeşil ve `inceleme-gecti` varsa. İlk sürümde birleştirmeyi yerel Claude yapar (Levent'in isteği onaydır);
  otomatik birleştirme ayrı bir karardır. Davranış değiştiren ya da kilitli dosyaya dokunan PR'da yerel Codex denetimi de şarttır; yalnız belge PR'ında bulut incelemesi yeterlidir.
- Cron: Tansu'nun günlük koşusu yerelde kalır (TASARIM §6 Görev Zamanlayıcı; `veri/` git'te yok; İş Yatırım ayak izi).
  Actions cron'u ilk sürümde yok.
- Depo özel kalır. GitHub Free'de özel depoya ayda 2.000 Actions dakikası var (GitHub belgeleri, 10.10); açık depo
  ücretsizdir ama depo özel kalır.

## Testing Decisions

- Kanıt: deneme issue'su (yalnız belge değişikliği) etiketlenir; ajan PR açar, CI koşar, inceleme etiketi düşer. Actions
  çalıştırma bağlantısı PR gövdesinde.
- `yerel` etiketli deneme issue'su etiketlenince ajan koşmaz (Actions kaydı "skipped").
- Kırmızı CI deneme PR'ında `ci-kirmizi` etiketi düşer ve ajan aynı dalı düzeltir.

## Out of Scope

- Tansu'nun günlük koşusunun buluta taşınması.
- Kendi sunucuda fabrika.
- Otomatik birleştirme.

## Further Notes

Belge hizası işi (`.scratch/belge-hizasi/`) sürerken Tansu'da yeni geliştirme durur; bu iş Tansu'nun davranışını
değiştirmez, çalışma düzenini değiştirir. Belge hizası biletlerinin çoğu beyin havuzuna ya da gerçek veriye bağlıdır
(`yerel`).
