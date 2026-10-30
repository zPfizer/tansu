# `gartley-pdf` geçmişi: eski ve yeni SHA eşlemesi (30.10.2026)

Karar: Levent 30.10.2026'da `gartley-pdf` geçmişinin klasör yollarından temizlenmesini ve dal birleşmeden önce zorla
itilmesini (force-push) onayladı. Önce başka bir dalın ya da PR'ın bu commit'lere bağlı olmadığının doğrulanmasını istedi.

## Ne değişti

- İlk ön kayıt commit'i (`ceb1e7a`) iki dosyada yerel klasör yolu ve beyin yolu taşıyordu: `kanit/gartley-yontem/pdf-setuplar.md`
  (setup listesinin depo kopyası) ve `kanit/gartley-yontem/plan-pdf.md` içindeki setup listesi satırı. Bir sonraki commit
  (`4fb3d47`) ikisini temizlemişti; yollar yalnız geçmişte duruyordu.
- Yeni `21a4d4a` commit'inin ağacı eski `4fb3d47` ağacıdır: `pdf-setuplar.md` hiç eklenmez, `plan-pdf.md` setup listesini
  "depo dışında" diye ve aynı SHA-256 değeriyle gösterir. Ön kaydın kuralları değişmedi.
- `4fb3d47` boş kalacağı için daldan çıktı; değişikliği `21a4d4a` içindedir.
- Diğer dört commit'in ağacı aynıdır. Altı commit'in yazarı, tarihleri ve mesajı aynıdır; yalnız `tree` ve `parent`
  satırları değişti.
- Son ağaç aynı kaldı: eski uç `725a86f` ile yeni uç `6d40101` arasında `git diff` boş; iki ucun ağacı `181c2b1`.
- Yeni geçmişte (`d683045..6d40101`) yerel yol ya da beyin yolu taraması 0 satır buldu.
- `d683045` ve öncesi (`gartley-yontem`, PR 215) değişmedi.

## Eski SHA'lar

`kanit/gartley-pdf.md`, `kanit/gartley-yahoo.md` ve `kanit/gartley-yontem/pdf.py` eski SHA'ları gösterir; metinleri
değişmedi. Yeni karşılık aşağıdaki tablodadır. Eski itme zamanı GitHub'ın dal etkinlik kaydından (`activity` API) alındı;
ön kaydın koşulardan önce gönderildiğini bu zamanlar gösterir.

| Eski | Yeni | Eski itme zamanı (GitHub, UTC) | Ağaç farkı | Konu |
|---|---|---|---|---|
| `ceb1e7a1073624d0eb3eaba17472e41470b06a71` | `21a4d4af87caf53aec3736801ae3afdb94ef5c87` | 2026-10-30T01:11:42Z (dal oluşturma) | `pdf-setuplar.md` yok; `plan-pdf.md` 1 satır | Gartley PDF: setup ailesi ön kaydı (13 deneme, koşulardan önce) |
| `4fb3d472a4e66e71051c76205d8fc7e46101d4d7` | yok (değişikliği `21a4d4a` içinde) | 2026-10-30T01:12:06Z | - | Gartley PDF: yerel yol ve beyin yolları depodan çıkarıldı (kurallar değişmedi) |
| `5e7916c1ed627fc76fce7a222c556ebdff25e6d6` | `8e28dd87d19aa0e7f0669c8b66b6ced4d9fa03c4` | 2026-10-30T01:50:32Z | - | Gartley PDF: sınav öncesi dondurma (Değişiklik 1: S2-Z ve S3, k = 5; pdf.py 3e8f2dc61aa1) |
| `8b740ed9876b463dccb6da95b60480df954c6b0b` | `ce87d20e3888a8bff184a33c77d461b793be2cda` | 2026-10-30T01:52:07Z | - | Gartley PDF: 13 deneme ve ayrık grup sınavı sonucu (HAYIR) |
| `fa804a677d2438397f0b6a0d6f8488c07db8e075` | `2d909eec98f1320f6c96efb7d31f6c96cf5c8a3f` | 2026-10-30T09:04:45Z | - | Ön kayıt: S3 için Yahoo veri kaynağı karşılaştırması |
| `725a86f895d23271d2369f537bcd41617e2ff0d6` | `6d40101aa025369d17d18c8b6583d51f756d690d` | 2026-10-30T09:13:31Z | - | Kanıt: S3 Yahoo veri karşılaştırması ve karantina yuvarlama bulgusu |

## Bağımlılık kontrolü (yeniden yazmadan önce, 30.10.2026)

- `git for-each-ref --contains ceb1e7a`: yalnız `refs/heads/gartley-pdf` ve `refs/remotes/origin/gartley-pdf`. Etiket yok.
- Çalışma ağaçlarının `HEAD`'leri (ayrık olanlar dahil): `gartley-pdf` dışında hiçbiri bu commit'leri içermez.
- `git ls-remote origin` (165 ref): bu commit'leri yalnız `refs/heads/gartley-pdf` içerir. `refs/pull/215/merge` ve
  `refs/pull/250/merge` GitHub birleştirme commit'leridir; ebeveynleri bu commit'leri içermez.
- `gh pr list --state all`: başı ya da tabanı `gartley-pdf` olan PR yok.

GitHub, hiçbir ref'in göstermediği eski commit'leri SHA ile bir süre gösterebilir. Kalıcı silme GitHub Destek ister;
başvurulmadı.
