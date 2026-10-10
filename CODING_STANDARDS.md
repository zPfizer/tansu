# Coding standards

## Clarify first
State your assumptions. When several readings exist and the choice changes the result, list them and ask. Name a simpler approach when one exists, and push back when warranted.

## Smallest diff
Write the minimum code the request needs: no unrequested features, single-use abstractions, configurability, or error handling for impossible cases. Trace every changed line to the request. Match the existing style. Leave adjacent code, comments, and formatting unchanged, and refactor only what is broken. Report unrelated dead code and leave it in place. Remove only the imports, variables, and functions your change made unused.

## Verified goals
Turn each task into a checkable success criterion:
- Validation: write tests for invalid inputs, then make them pass.
- Bug: write a test that reproduces it, then make it pass.
- Refactor: tests pass before and after.

For multi-step work, write a plan as `1. [Step] → verify: [check]`. Loop until each check passes.

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
