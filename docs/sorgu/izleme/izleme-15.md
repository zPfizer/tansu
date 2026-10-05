# İzleme 15: cevaplar-15-kayit.md ile taslak 6 karşılaştırması

Kapsam: yalnız KARAR ve YANLIŞ hükümleri (dosyada EKSİK yok). CEVAPLI, OLGU ve ZAYIF SORU satırları dışarıda: 15-004, 15-014, 15-025, 15-030, 15-062, 15-092.
Kısaltmalar: TASARIM = docs/TASARIM.md (taslak 6); sonuc = docs/sorgu/sonuc-3-4.md; AGENTS = AGENTS.md.

15-001 — KARAR — VAR — sonuc C-6 (parametreler kodda donmuş dataclass, hash'e girer); MASRAF notu silinen ön deneme koduna ait
15-002 — KARAR — TEKRAR — 15-070 (kayit türü satırı)
15-003 — KARAR — VAR — sonuc C-6 (parametreler kodda donmuş dataclass)
15-005 — KARAR — VAR — sonuc C-6 (donmuş dataclass)
15-006 — KARAR — YENİ — TASARIM 5.8: hash = kod + kural parametreleri; tekrar sayısı, blok, tohum, ızgara, masraf senaryo listesi sınama ayarıdır, hash dışı, günlükte ayrı alan
15-007 — KARAR — TEKRAR — 15-006 (likidite/pozisyon/sermaye kuralda; masraf üç düzeyi tek deneme; TASARIM 5.4 ile uyumlu)
15-008 — KARAR — TEKRAR — 15-006 (ızgara tanımı sınama ayarı; destek satırı için 15-070)
15-009 — KARAR — RED — aşırı kurulum; YORUM'lar KURALLAR §3'te zaten listeli
15-010 — KARAR — TEKRAR — 15-070 (sadakat satırı)
15-011 — KARAR — VAR — TASARIM 5.5 (ortak risk paketi) + sonuc C-6 (param hash; ortak değer değişince kimlikler değişir)
15-012 — KARAR — VAR — sonuc C-6 (kodda dataclass, hash asdict'ten)
15-013 — KARAR — RED — aşırı kurulum; dataclass'ta yol/ortam alanı zaten yok
15-015 — KARAR — VAR — sonuc C-6 + C-2 (stdlib dataclass, ek kütüphane yok)
15-016 — KARAR — YENİ — TASARIM 5.8 / sonuc C-6: hash kapsamı elle yazılmış KOD_DOSYALARI listesi (aileler, gostergeler, motor, simulator, K1); test ve rapor dışı; her tansu/*.py listede ya da HASH_DISI'nda olmalı (pytest)
15-017 — KARAR — TEKRAR — 15-016
15-018 — KARAR — TEKRAR — 15-016 (motor dosyası listede olduğu için motor değişimi bütün kimlikleri değiştirir)
15-019 — KARAR — VAR — TASARIM 5.8 (parmak izi = kural, parametre, kod) + 5.11 (veri anlık görüntüsü günlükte) + sonuc C-6
15-020 — KARAR — TEKRAR — 15-046 (kod_hash, param_hash, veri_hash ayrı alan)
15-021 — KARAR — VAR — sonuc C-6 (sha256)
15-022 — YANLIŞ — VAR — sonuc C-6 (hash = kod dosyalarının `ast.dump` sha256'sı); ham metin hash'i tasarımda yok
15-023 — KARAR — VAR — sonuc C-6 (AST hash; AST değişirse yeni kimlik)
15-024 — KARAR — VAR — TASARIM 5.3 (elle hesaplı motor sınamaları) + sonuc C-9; davranış hash'i tasarımda yok
15-026 — KARAR — TEKRAR — 15-046 (ortam alanı); sürüm kilidi sonuc C-2
15-027 — KARAR — VAR — sonuc C-2 + pyproject.toml (`==` sabitli bağımlılıklar)
15-028 — KARAR — VAR — sonuc C-2 + pyproject.toml (`requires-python = "==3.14.*"`); ortam.python alanı 15-046'da
15-029 — KARAR — VAR — sonuc C-6 (parametrelerin sıralı JSON sha256'sı)
15-031 — KARAR — VAR — sonuc C-6 (hash yalnız kod + parametre; ad girmez)
15-032 — KARAR — VAR — TASARIM 5.6 (çift seçimi önceden yazılmış kural) + sonuc C-6; çiftlerin günlüğe yazımı 15-046 sonuç alanı
15-033 — KARAR — TEKRAR — 15-006 (tohum ve tekrar sınama ayarı, hash dışı)
15-034 — KARAR — TEKRAR — 15-074 (kural kaydı yoksa ya da hash uyuşmazsa kosu() durur)
15-035 — KARAR — VAR — TASARIM 5.11 (o ana kadarki bütün benzersiz kural kimlikleri) + AGENTS (günlük silinmez)
15-036 — KARAR — VAR — sonuc C-9 (kayıt modülü testleri)
15-037 — KARAR — VAR — sonuc C-6 (AST hash; taşıma kimliği değiştirir, kabul)
15-038 — KARAR — VAR — sonuc C-6 (AST, bayt kodu değil)
15-039 — KARAR — TEKRAR — 15-016 (test dosyaları hash dışı)
15-040 — KARAR — TEKRAR — 15-070 (tur:kayit satırı, aynı dosya)
15-041 — KARAR — VAR — sonuc C-6 (`kayit/deneme.jsonl`) + TASARIM 5.11
15-042 — KARAR — RED — AGENTS ile çelişir: commit pytest yeşilden sonra ajan işi; temiz ağaç şartı (sonuc C-6) kirli kaydı zaten yakalar
15-043 — YANLIŞ — RED — hash zinciri aşırı kurulum; önerilen otomatik commit de 15-042 gibi reddedildi
15-044 — KARAR — YENİ — TASARIM 5.11: her koşu önce olay=basladi, sonra olay=bitti satırı yazar; bitti'siz basladi deneme sayılır
15-045 — KARAR — TEKRAR — 15-044
15-046 — KARAR — YENİ — TASARIM 5.11 alan listesi: tarih (UTC ISO), kosu_id, kural_id, kod_hash, param_hash, veri_hash, param tam JSON kopya, git_commit, tohum, tekrar sayısı, ham p, masraf düzeyi başına sonuç, ortam (Python + kütüphane sürümleri), sema:1, resmi, kirli
15-047 — KARAR — TEKRAR — 15-046 (param kopya + hash)
15-048 — KARAR — TEKRAR — 15-046 (bitti satırında p; Holm oradan okur)
15-049 — KARAR — RED — yedek yok kararı (sonuc D-2, C-10)
15-050 — KARAR — VAR — sonuc C-7 + TASARIM 6.2 (19:30 koşusu veri yeniler, getiri koşusu değil); salt-ekleme sonuc C-6
15-051 — KARAR — TEKRAR — 15-070 (duzeltme satırı)
15-052 — KARAR — YENİ — TASARIM 5.11: Holm'a her kural kimliğinin ilk resmi koşusunun p'si girer; geliştirme koşuları resmi:false yazılır, m'yi şişirmez
15-053 — KARAR — TEKRAR — 15-070 (sadakat satırı)
15-054 — KARAR — TEKRAR — 15-046 (tarih UTC ISO 8601)
15-055 — KARAR — TEKRAR — 15-046 (kosu_id)
15-056 — KARAR — VAR — TASARIM 5.6 (sınama birimi = bütün çift bölmesi) + 5.11 (kural kimliği başına koşu)
15-057 — KARAR — TEKRAR — 15-046 (sema:1)
15-058 — KARAR — VAR — TASARIM 6.7 (Levent yalnız durum.txt'ye bakar; günlüğü açmaz)
15-059 — KARAR — VAR — TASARIM 5.11 (o ana kadarki bütün benzersiz kural kimlikleri)
15-060 — KARAR — VAR — AGENTS (rapor/ git dışı) + sonuc C-10 (.gitignore rapor/) + TASARIM 4 (rapor modülü)
15-061 — KARAR — VAR — TASARIM 5.11 + sonuc C-6 (Holm birimi benzersiz kural kimliği)
15-063 — KARAR — VAR — TASARIM 5.11 + sonuc C-6 (m = benzersiz kural kimliği)
15-064 — KARAR — VAR — TASARIM 1 (P3) ve 5.12.1 (Holm düzeltmeli p < 0,05; ölçüt gevşetilmez)
15-065 — KARAR — YENİ — TASARIM 5.11: Holm'a kural kimliği başına tek p girer: %0,5 masrafta K1 iki türünün büyük p'si (5.12.3 ile uyumlu)
15-066 — KARAR — TEKRAR — 15-065
15-067 — KARAR — VAR — TASARIM 5.12.1 (ileri yürüme yıllarının birleşimi için Holm'lu p; yıllık ayrı sonuç 5.8)
15-068 — KARAR — VAR — TASARIM 4 (istatistik: statsmodels Holm için) + sonuc C-2
15-069 — KARAR — VAR — TASARIM 5.11 (Holm) + 1 (P3)
15-070 — KARAR — YENİ — TASARIM 5.11: tur alanı kayit, deneme, destek (ızgara, yeniden üretim, sınama), sadakat, duzeltme (hedef_kosu_id, yeni değer; asıl satır değişmez); Holm yalnız deneme satırlarını sayar
15-071 — KARAR — TEKRAR — 15-044 (hata veren koşu basladi bırakır, m'de sayılır, p = 1)
15-072 — KARAR — RED — keyfî tahmini "gecmis" sayısı m'yi uydurma yapar; ön deneme zaten kanıt dışı (TASARIM başı, C7) ve kod silindi; kosu() kapısı 15-074'te
15-073 — KARAR — TEKRAR — 15-074 (kosu() günlüksüz sonuç döndürmez); AGENTS günlük kuralı zaten var
15-074 — KARAR — YENİ — TASARIM 4 (`kayit`/`__main__`): getiri gösteren tek yol kosu(); kural kaydı yoksa ya da hash uyuşmazsa tek Türkçe satırla durur; motor iç fonksiyonu
15-075 — KARAR — RED — Streamlit/ekran yok (sonuc C-1); rapor statik HTML, import denetimi gereksiz
15-076 — KARAR — YENİ — TASARIM 4 rapor / 5.11: rapor başlığı m ve Holm hesap tarihini yazar; Holm rapor üretilirken yeniden hesaplanır
15-077 — KARAR — TEKRAR — 15-078 (p = (b+1)/(n+1))
15-078 — YANLIŞ — YENİ — TASARIM 5.7 ve sonuc B-14: B ≥ max(1.000, 200·m) (20·m'de p tabanı 1/(20m+1) eşiğin 0,05/m'ine yalnız sıfırı sıfır farkla geçer, güç yok); p = (b+1)/(n+1); süre ölçülmedi, C-11 bütçesiyle kontrol et
15-079 — KARAR — TEKRAR — 15-070 (destek satırı)
15-080 — KARAR — TEKRAR — 15-079 (önbellek yok, yeniden üretim kontrolü destek satırı)
15-081 — KARAR — VAR — TASARIM 5.8 + 5.11 (tekrar koşusu yeni deneme değil) + 6.4 (19:30 yalnız kart)
15-082 — KARAR — TEKRAR — 15-052
15-083 — KARAR — VAR — TASARIM 5.11 (aynı kuralın tekrar koşusu yeni deneme değildir)
15-084 — KARAR — VAR — TASARIM 5.11; kosu_id benzersizliği 15-046
15-085 — KARAR — VAR — sonuc C-6 (kimlik içerik hash'i; eski değere dönüş eski kimliktir) + TASARIM 5.11
15-086 — KARAR — TEKRAR — 15-070 (duzeltme satırı)
15-087 — KARAR — TEKRAR — 15-070 (ızgara tek destek satırı)
15-088 — KARAR — TEKRAR — 15-046 (bitti satırında yalnız özet)
15-089 — KARAR — TEKRAR — 15-074
15-090 — KARAR — TEKRAR — 15-074 (kapı kosu() içinde; motor testleri sentetik veriyle sonuc C-9)
15-091 — KARAR — TEKRAR — 15-046 (git_commit, param kopyası, tohum, ortam, veri_hash); anlık görüntü sonuc C-4
15-093 — KARAR — VAR — sonuc C-4 (manifest.json sha256, tarihli klasör) + TASARIM 5.11
15-094 — KARAR — VAR — TASARIM 5.11 (tohum günlükte); SeedSequence ayrıntısı uygulama
15-095 — KARAR — TEKRAR — 15-094
15-096 — KARAR — VAR — sonuc C-2 (sürüm kilidi) + 15-046 ortam alanı
15-097 — KARAR — RED — aşırı kurulum; sürümler C-2'de sabit, motor sınamaları 5.3 yeter
15-098 — KARAR — RED — 15-097 reddedildiği için tolerans kuralı gereksiz
15-099 — KARAR — VAR — sonuc C-6 (resmi koşu temiz git ağacı ister) + TASARIM 5.11 (git commit); kirli bayrağı 15-046
15-100 — KARAR — TEKRAR — 15-074 (hash uyuşmazlığında tek satırlık durma; zincir, kilit, önbellek yok)

## Özet

Sayımlar (grep ile, dosya yazıldıktan sonra):
Toplam 94 madde: VAR 40, TEKRAR 35, YENİ 10, RED 9.

YENİ listesi:
- 15-006 — TASARIM 5.8: hash = kod + kural parametreleri; tekrar, blok, tohum, ızgara, masraf senaryosu hash dışı, günlükte ayrı alan.
- 15-016 — TASARIM 5.8 / sonuc C-6: elle yazılmış KOD_DOSYALARI listesi; test ve rapor dışı; pytest her tansu/*.py'nin listede ya da HASH_DISI'nda olduğunu denetler.
- 15-044 — TASARIM 5.11: koşu önce basladi, sonra bitti satırı yazar; bitti'siz basladi deneme sayılır.
- 15-046 — TASARIM 5.11: alan listesi (kosu_id, kural_id, kod_hash, param_hash, veri_hash, param kopya, git_commit, tohum, tekrar, ham p, masraf düzeyi sonuçları, ortam, sema, resmi, kirli).
- 15-052 — TASARIM 5.11: Holm'a ilk resmi koşunun p'si girer; geliştirme koşuları resmi:false.
- 15-065 — TASARIM 5.11: Holm girdisi = %0,5 masrafta K1 iki türünün büyük p'si.
- 15-070 — TASARIM 5.11: tur alanı (kayit, deneme, destek, sadakat, duzeltme); Holm yalnız deneme satırları.
- 15-074 — TASARIM 4: getiri yalnız kosu() üzerinden; kayıt yoksa ya da hash uyuşmazsa durur.
- 15-076 — TASARIM 4 rapor / 5.11: rapor başlığı m ve Holm hesap tarihini yazar.
- 15-078 — TASARIM 5.7 / sonuc B-14: B ≥ max(1.000, 200·m); p = (b+1)/(n+1).

YANLIŞ olup VAR olmayanlar:
- 15-043 — RED: hash zinciri aşırı kurulum; otomatik commit de AGENTS ile çelişir (15-042).
- 15-078 — YENİ: 20·m yerine 200·m (yukarıdaki satır). Süre ölçülmedi; uygulamadan önce sonuc C-11 bütçesiyle denenmeli.

(15-022 YANLIŞ olarak VAR: sonuc C-6 `ast.dump` hash'ini açıkça yazıyor.)
