# 03: Kırmızı CI ve inceleme etiketle döngüye girer

**What to build:** PR'ın CI'ı kırmızıysa ajan aynı dalda düzeltir; yeşilse ikinci bir ajan bağımsız inceleme yapar ve sonucu etiketle bildirir. Birleştirme yalnız CI yeşil ve `inceleme-gecti` ile olur.

**Blocked by:** 02

**Status:** ready-for-agent

- [x] CI kırmızı bittiğinde bir `workflow_run` iş akışı etiketi koyar ve düzeltme ajanını aynı dalda çalıştırır (etiket durumu gösterir, tetik değildir; GITHUB_TOKEN ile konan etiket başka iş akışını tetiklemez); CI yeşil olunca etiket kalkar.
- [x] CI yeşil olunca inceleme ajanı AGENTS.md ve iki standart dosyasına göre inceler (ölçütler isteğin içinde); sonucu PR yorumu, "geçti" ise `inceleme-gecti` etiketi.
- [ ] Deneme PR'ında kırmızıdan yeşile döngü ve inceleme etiketi görüldü (Actions bağlantıları PR'da).
- [x] Döngü sınırı var: aynı PR'da en fazla 3 düzeltme koşusu; sonra `ready-for-human`.

## Comments

f03 (15.10): İş akışı `.github/workflows/dongu.yml` yazıldı (dal `pr/f03-dongu`, push yok). Kutu 1, 2 ve 4 işaretli (iş akışı bunları uygular); kutu 3 canlı koşu ister. Canlı koşu şunlara bağlı: Levent'in iki adımı (Claude GitHub App, sır `CLAUDE_CODE_OAUTH_TOKEN`) ve bu dosyanın `master`'a birleşmesi (`workflow_run` varsayılan daldaki dosyayı çalıştırır). Sapma: inceleme araçlarına salt okunur `gh issue view` eklendi (bağlı issue'yu okumak için). KALDI sonrası otomatik yol yok; insan devreye girer. Birleştirmede yerel Claude `inceleme-gecti` etiketinin son commit'e ait olduğunu denetlemeli: yeni push etiketi hemen silmez, sonraki yeşil CI'da inceleme işi iki etiketi de siler.

f03 ön inceleme (15.10, action kaynağı a26b07d'ye karşı): Eylem uygulama jetonuyla (OIDC) push eder ve gh koşar; ajanın push'u, PR'ı ve gövde düzenlemesi `ci` ve `dod`'u tetikler. Değişenler: iki eylem adımında `allowed_bots: "claude[bot]"` (bot koşuları insan denetiminde düşmesin); push kapsamı `pr/*` ile sınırlı, `master` ve `:` itme reddedilir; `duzelt` işinde `additional_permissions: actions: read` (`gh run view --log-failed` için); inceleme işinde kök `master`, PR dosyaları `pr-head/` altında (`--add-dir pr-head`), yani inceleme işi PR kodunu çalıştırmaz ve ayarı PR'dan yüklemez; `duzelt` işi PR kodunun pytest'ini sırlarla koşar (kabul edilen risk: özel, tek sahipli depo, yalnız yazarlar `pr/*` açar; resmî ci-failure örneği de aynısını yapar); iş başına en düşük GITHUB_TOKEN izni; eski koşu koruması (PR başı `workflow_run.head_sha` ile aynı değilse iş durur); `duzelt` ajanı çözemezse `ready-for-human` koyar; ek yasaklar `git commit -a`, `git -C`, `git add -u`, `git add ./*`.

Birleştirme sırası: bilet 08 (`dod_kontrol.py` `geçti`, `GEÇTİ`, `NOTLU GEÇTİ` kabul eder) bu PR'dan önce `master`'a birleşir. Bu yüzden inceleme istemi `Sonuç: NOTLU GEÇTİ` yazabilir. PR şablonundaki yorum satırı 08'in işidir; bu dalda dokunulmadı.

Hâlâ doğrulanmayan: (1) `gh pr edit --body-file -` ile heredoc, `Bash(gh pr edit:*)` izniyle geçer mi; (2) `gh pr edit --remove-label` PR'da olmayan etiketle hata vermez mi; (3) `workflow_run.pull_requests[0]` dolu mu (boşsa `gh pr list` yedeği); (4) `Bash(git push)` yalın biçimi izin kuralında eşleşir mi; (5) `--add-dir pr-head` ile pr-head altı Read/Glob/Grep'e açılır mı; (6) `allowed_bots` değeri `claude[bot]` bu adla mı geliyor.
