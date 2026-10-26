# Faz 0: dal koruması kapısı

Tarih: 26.10.2026 19:54 (+03:00). Sonuç: GEÇTİ.

İlk deneme 19:50'de durdu: `main` korumasızdı (HTTP 404). Levent korumayı açtı; kapı yeniden koşuldu.

```
$ gh api repos/zPfizer/tansu/branches/main/protection --jq '{required_pull_request_reviews: {required_approving_review_count: ...}, enforce_admins: {enabled: ...}}'
{"enforce_admins":{"enabled":true},"required_pull_request_reviews":{"required_approving_review_count":1}}

$ git rev-parse main origin/main
3778a1c4b11d05965406baa4d4119a72eedea6b3
3778a1c4b11d05965406baa4d4119a72eedea6b3

$ git tag -a v0.1-arsiv 3778a1c4 -m "Arsiv: yeniden kurulus oncesi main (26.10.2026)"
$ git push origin v0.1-arsiv
 * [new tag]         v0.1-arsiv -> v0.1-arsiv

$ git worktree add -b yeniden-kurulus .claude/worktrees/yeniden-kurulus v0.1-arsiv
$ git push -u origin yeniden-kurulus
 * [new branch]      yeniden-kurulus -> yeniden-kurulus

$ gh api repos/zPfizer/tansu/git/tags/b36587c7e4429660c5de9f3c2cb7878202e33b9a --jq '{tag, object: .object.sha}'
{"object":"3778a1c4b11d05965406baa4d4119a72eedea6b3","tag":"v0.1-arsiv"}
```
