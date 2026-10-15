# 03: Kırmızı CI ve inceleme etiketle döngüye girer

**What to build:** PR'ın CI'ı kırmızıysa ajan aynı dalda düzeltir; yeşilse ikinci bir ajan bağımsız inceleme yapar ve sonucu etiketle bildirir. Birleştirme yalnız CI yeşil ve `inceleme-gecti` ile olur.

**Blocked by:** 02

**Status:** ready-for-agent

- [x] CI kırmızı bittiğinde bir `workflow_run` iş akışı etiketi koyar ve düzeltme ajanını aynı dalda çalıştırır (etiket durumu gösterir, tetik değildir; GITHUB_TOKEN ile konan etiket başka iş akışını tetiklemez); CI yeşil olunca etiket kalkar.
- [x] CI yeşil olunca inceleme ajanı AGENTS.md ve iki standart dosyasına göre inceler (ölçütler isteğin içinde); sonucu PR yorumu, "geçti" ise `inceleme-gecti` etiketi.
- [ ] Deneme PR'ında kırmızıdan yeşile döngü ve inceleme etiketi görüldü (Actions bağlantıları PR'da).
- [x] Döngü sınırı var: aynı PR'da en fazla 3 düzeltme koşusu; sonra `ready-for-human`.

## Comments

f03 (15.10): İş akışı `.github/workflows/dongu.yml` yazıldı (dal `pr/f03-dongu`, push yok). Kutu 1, 2 ve 4 işaretli (iş akışı bunları uygular); kutu 3 canlı koşu ister. Canlı koşu şunlara bağlı: Levent'in iki adımı (Claude GitHub App, sır `CLAUDE_CODE_OAUTH_TOKEN`) ve bu dosyanın `master`'a birleşmesi (`workflow_run` varsayılan daldaki dosyayı çalıştırır). Doğrulanmayanlar: (1) ajanın push'u CI'ı yeniden tetikler mi (GITHUB_TOKEN push'u tetiklemez; claude-code-action uygulama jetonu kullanıyorsa tetikler); (2) PR gövdesi düzenlemesi `dod` iş akışını yeniden tetikler mi (aynı neden); (3) `gh pr edit --body-file -` ile stdin'den gövde, `Bash(gh pr edit:*)` izniyle geçer mi; (4) `gh pr edit --remove-label` PR'da olmayan etiketle hata vermez mi; (5) `workflow_run.pull_requests[0]` dolu mu (boşsa `gh pr list` yedeği); (6) inceleme işinde `contents: read` yeter mi. Sapma: inceleme araçlarına salt okunur `gh issue view` eklendi (bağlı issue'yu okumak için). `Sonuç: NOTLU GEÇTİ` satırını yalnız bilet 08'in `dod_kontrol.py` değişikliği kabul eder; 08 birleşmeden bu sonuçta `dod` kırmızı olur. KALDI sonrası otomatik yol yok; insan devreye girer. Birleştirmede yerel Claude `inceleme-gecti` etiketinin son commit'e ait olduğunu denetlemeli: yeni push etiketi hemen silmez, sonraki yeşil CI'da inceleme işi iki etiketi de siler.
