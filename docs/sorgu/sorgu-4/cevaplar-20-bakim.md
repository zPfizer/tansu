# Cevaplar 20: Sürüm, belge, bakım

Doğrulanan olgular (git, venv, dosya sistemi ile): uzak depo yok; tek dal `master`; `core.autocrlf=true`; `.gitattributes` yok; `.gitignore` yalnız `.venv/ veri/ __pycache__/ *.pyc .pytest_cache/`; `rapor/*.parquet` ve `rapor/*.md` git'te İZLENİYOR; `.scratch/` yok; `pyproject.toml` yalnız pytest ayarı; Python 3.14.7; kurulu: pandas 3.0.6, pytest 9.1.1, statsmodels, scipy, pyarrow, borsapy, pandas-ta-classic, duckdb; ruff, mypy, pyright, pre-commit, quantstats kurulu DEĞİL. `tansu/*.py` 266 satır, testler 159 satır (425 toplam).

20-001 — KARAR — Uzak depo yok, tek kopya var. Karar: günlük ve otomatik, harici diske ya da OneDrive klasörüne `git bundle` + `veri/` kopyası. Bunu §6 günlük akışının son adımı yap.
20-002 — KARAR — Haftada bir, Görev Zamanlayıcı ile, harici sürücüye `robocopy` ile tüm klasör (`.venv` hariç). Levent'in elle yapması gerekmez.
20-003 — YANLIŞ — `veri/` ignore'da; anlık görüntü kaydı (dosya adı + hash) git'te olmalı. Fix: `kayit/anlik.csv` (tarih, dosya, sha256) git'e girer; ham dosyalar yedekle korunur.
20-004 — KARAR — Anlık görüntü yazılırken `hashlib.sha256` (stdlib) kayıt dosyasına yazılır; koşu başında yeniden hesaplanır, uyuşmazsa durur. Yazma salt-okunur bayrağı da konur.
20-005 — YANLIŞ — Parquet zaten git'te (`git ls-files` doğruladı). Fix: `rapor/*.parquet` `.gitignore`'a; `rapor/*.md` git'e girer. Karar tek kuraldır, kimsenin seçmesi gerekmez.
20-006 — KARAR — Hash = `git rev-parse HEAD` commit'i. Çalışma ağacı kirliyse (`git status --porcelain` boş değil) koşu reddedilir; kural kaydı koşusu için zorunlu, deneme için günlüğe "kirli" yazılır ve Holm'e sayılır.
20-007 — KARAR — Doğrulanamaz. Kural: `rebase`/`amend`/`--force` yasak (AGENTS.md'ye yazılır); yedek paketi geçmişi korur.
20-008 — KARAR — Doğrudan `master`'da çalış. Tek kişi, uzak depo yok; dal yönetimi yük. Ajan büyük işte geçici dal açabilir, bitince birleştirir.
20-009 — OLGU — Doğrulandı: tek dal `master`. AGENTS.md'ye bir satır: "ana dal master". Yanlış dal riski dal politikasıyla (20-008) kapanır.
20-010 — KARAR — Ajan, testler geçince kendi commit atar; `push`, `--force`, `reset --hard` yasak. Onay sorarsa Levent'in cevap verecek bilgisi yok, anlamsız yük.
20-011 — KARAR — Hayır, serbest Türkçe yeter. Tek kural: sonucu değiştiren commit mesajı "SONUÇ:" ile başlar. Gerisini deneme günlüğü (commit hash'li) taşır.
20-012 — KARAR — Hayır. Yeni deneme = çıktı rakamını değiştiren değişiklik. Ölçüt otomatik: aynı girdiyle çıktı hash'i değişti mi. Kozmetik commit günlüğe girmez.
20-013 — KARAR — Evet, tek tür: `kural-kaydi-N` etiketi. Başka etiket yok. Rapor başlığı commit hash'ini yazar (20-006).
20-014 — YANLIŞ — Kod hash'i git commit olduğundan CRLF'ten etkilenmez, ama dosya hash'i kullanılırsa etkilenir. Fix: dosya hash'i kullanma; `.gitattributes` içine `* text=auto eol=lf` ekle.
20-015 — YANLIŞ — Önlem yok ve parquet zaten girmiş (20-005). Fix: `.gitignore`'a `*.parquet`; AGENTS.md'ye "`git add .` yasak, dosya adıyla ekle". Hook yok.
20-016 — KARAR — Dosyayı sil, geçmişi temizleme. Geçmiş yedekte kalır ve ön deneme kaydı olarak değerli. Geçmiş yeniden yazmak 20-007 ile çelişir.
20-017 — KARAR — Kalır, ama başlığına "KANIT DEĞİL" satırı eklenir; zaten TASARIM satır 13 bunu yazıyor. Daha güvenlisi: `rapor/` yerine `docs/arastirma/` altına taşı ve adı `on-deneme-kanit.md` olsun.
20-018 — CEVAPLI — Evet, tek yol git geçmişi (`git show <commit>:docs/TASARIM.md`); commit mesajları "Tasarım taslak N" ile aranabilir. Yeterli.
20-019 — KARAR — TASARIM.md düzenlenir. ADR yazılmaz; "neden" bilgisi sorgu dosyalarında kalır. `docs/agents/domain.md`'deki ADR anımı kullanılmayan şablon metnidir.
20-020 — ZAYIF SORU — ADR olmayacağı için çelişme yok (20-019). "Belge" = `docs/TASARIM.md`.
20-021 — KARAR — Sorgu dosyaları taşınmaz ve yeniden adlandırılmaz (kural). Ölü referans oluşursa `git log --follow` bulur. Ek araç gerekmez.
20-022 — KARAR — Hayır, 306 satır tam okunmaz. Tek bir "durum" paragrafı (10 satır) TASARIM.md'nin tepesine; Levent yalnız onu okur.
20-023 — YANLIŞ — Denetleyen yok; sahte denetim kurma. Fix: sayılar kodda tek yerde sabit (`tansu/sabitler.py` değil, ilgili modülde) ve test bu sayıyı TASARIM'daki değerle karşılaştırır (20-024).
20-024 — KARAR — Tek doğru kaynak TASARIM.md. Kodda sabitin yanına "TASARIM §5.4" yorumu; bir test sabitleri metinden regex ile okuyup karşılaştırabilir (sonraki iş, şimdi değil).
20-025 — KARAR — Veri dosyası: `kural-kaydi.toml` (stdlib `tomllib`), git'te, kural kaydı hash'i commit olduğu için otomatik kapsanır.
20-026 — ZAYIF SORU — Kod adları yeniden yazılacak (§7 adım 1); şimdi dondurmak anlamsız. Yeniden adlandırma sırasında GLOSSARY güncellenir, tek commit.
20-027 — CEVAPLI — Evet yanıltır (`nabiz.py`, GLOSSARY "Piyasa durumu"). Fix: modül `piyasa_durumu.py` olarak yeniden adlandırılır; zaten kod yeniden yazılıyor.
20-028 — KARAR — Mevcut koddaki gibi: alan terimleri Türkçe (GLOSSARY'den), genel programlama terimleri İngilizce. Kural: GLOSSARY'de olan terim Türkçe yazılır.
20-029 — KARAR — Girecek. `.scratch/` git'te izlenir; bilet dosyaları küçük metin, yedeklenmesi gerekir.
20-030 — KARAR — Her bilet değişikliği ayrı commit olmaz; iş commit'iyle birlikte gider. Gürültü olmaz.
20-031 — YANLIŞ — Aşırı yapı. Fix: tek `TODO.md` (kökte, 20 satır sınırı); spec zaten TASARIM.md. `issues/NN-slug.md` yalnız bir iş 1 oturuma sığmazsa.
20-032 — ZAYIF SORU — `needs-info`/`wontfix` tek kullanıcıda anlamsız. Yalnız `ready-for-agent` ve `ready-for-human` kullanılır; TODO.md'de iki başlık yeter.
20-033 — KARAR — Güvenli: dosya düzenleme, test, commit. Asla: `git push`/`--force`/`reset --hard`, `veri/` silme, bağımlılık ekleme, TASARIM/KURALLAR/AGENTS düzenleme, kural parametresi değiştirme.
20-034 — ZAYIF SORU — TODO.md (20-031) ile "Status:" satırı yok. Satır silinince iş biter; yanlış durum riski kalmaz.
20-035 — KARAR — Evet: TODO.md'nin ilk bölümü "Şimdi ne yapılıyor" (3 satır). `.scratch/` taranmaz.
20-036 — CEVAPLI — Hayır, Levent bilet/ADR/`map.md` yönetmez. Onun belgeleri: TASARIM tepe özeti, TODO.md, geri dönüş rehberi (20-077). Gerisi ajan içindir.
20-037 — YANLIŞ — AGENTS.md satır 1-18 yalnız işaretçi; yasak listesi yok (doğrulandı). Fix: AGENTS.md'ye "Yapma" bölümü (20-033 listesi) eklenir; Levent izni gerekir (20-064).
20-038 — YANLIŞ — Yazılı değil, ajan belgeyi koda uydurabilir. Fix: AGENTS.md: "Belge ile kod çelişirse dur, Levent'e sor; TASARIM.md'yi ajan Levent onayı olmadan değiştirmez."
20-039 — YANLIŞ — Yok. Fix: AGENTS.md'ye bir satır: `.venv\Scripts\python.exe -m pytest` (doğrulandı: pytest 9.1.1 kurulu).
20-040 — KARAR — PowerShell sabit. Python komutları `-c`/stdin ile; yol ayracı `\`. AGENTS.md'ye bir satır.
20-041 — KARAR — Kural: ajan bir oturumda en çok 10 dosya değiştirir; fazlası bölünür. Levent'in gözden geçirmesi tek komutla (20-058), kod okuyarak değil.
20-042 — KARAR — Kabul göstergesi: `python -m pytest` çıktısı "N passed" ve 0 failed; ajan bunu son mesajında yapıştırır.
20-043 — YANLIŞ — Kimse kontrol etmiyor. Fix: ilke "test TASARIM'daki kuraldan türer, koddan değil"; her test kuralın §numarasını docstring'inde taşır. Bağımsız ajan denetimi büyük değişiklikten sonra (20-079).
20-044 — KARAR — AGENTS.md'ye yazılır: "Motor kuralı için önce test, sonra kod." Tek satır.
20-045 — OLGU — Doğrulandı: bağımlılık listesi hiçbir yerde yok; yalnız `.venv` içinde (pandas 3.0.6, pyarrow 25.0.1, statsmodels 0.15.0 vb.). Fix: 20-046.
20-046 — KARAR — Evet: `pip freeze > requirements.lock` git'e. Stdlib pip yeter; ek araç yok.
20-047 — KARAR — `pip` + `requirements.lock`. Zaten `.venv` içinde; `uv`/`poetry` yeni araç, kazancı yok.
20-048 — KARAR — Kimse fark etmez. Fix: yalnız kullanılan 3-4 kütüphane; bozulursa test kırılır. Ek izleme yok. Not: quantstats kurulu değil (doğrulandı), tasarım ona dayanıyor; ekleme kararı o iş geldiğinde.
20-049 — KARAR — Ölçüt iki satır: son sürüm 12 ay içinde ve pandas/numpy'ın doğrudan bağımlılığı olmayan yeni paket yalnız Levent onayıyla. Ajan kendi başına paket eklemez (20-033).
20-050 — KARAR — Evet, tek karşılaştırma: yükseltmeden önce ve sonra `kanit` raporunun çıktı hash'i. Fark varsa yükseltme geri alınır. `requirements.lock` commit'te.
20-051 — KARAR — ruff kurulu değil (doğrulandı). Şimdilik kurma. Gerekirse varsayılan küme, savunan yok.
20-052 — KARAR — Otomatik biçimlendirme yok. Gerekirse ajan oturum sonunda bir kez çalıştırır.
20-053 — KARAR — Hook yok. Zorunluluk: ajan commit'ten önce pytest çalıştırır (AGENTS.md); yetmezse Levent'in kapı komutu (20-058).
20-054 — YANLIŞ — Tip denetimi eklenmesin. Pandas kodunda gürültü; mypy/pyright kurulu değil (doğrulandı).
20-055 — ZAYIF SORU — Tip denetimi yok (20-054).
20-056 — KARAR — Zorunlu: pytest (kurulu). Hiçbiri başka: ruff, mypy, pre-commit, uv yok. Ölçüt: araç, testin yakalayamadığı ve gerçekleşmiş bir arıza türünü önlüyorsa eklenir.
20-057 — KARAR — Kapsam yüzdesi hedefi yok. "Yeterli" = TASARIM §5.3 motor sınamaları (belirli listelenmiş durumlar) var ve geçiyor.
20-058 — KARAR — Kapı = `.venv\Scripts\python.exe -m pytest`. AGENTS.md'de yazılı; Levent çalıştırabilir, çıktıda "passed" arar. Lint/tip yok.
20-059 — KARAR — Yerel mekanizma yok ve gerekmiyor: ajan commit öncesi pytest çalıştırır (20-053). Garanti istenirse `git log` ile test sayısı raporu; CI kurma.
20-060 — KARAR — Sızıntı riski daha düşük (veri herkese açık, kod kişisel); kayıp daha önemli. Karar yazılsın: uzak depo yok, yedek yerel/harici (20-001). Özel uzak depo isteğe bağlı, Levent'in sonraki kararı.
20-061 — KARAR — Şimdi yok. Anahtar gelince: `.env` `.gitignore`'a o gün eklenir; önceden kural yazma (YAGNI).
20-062 — KARAR — Paket eklemek yasak (20-033); fark etme yolu `requirements.lock` farkı (`git diff`). Ağ sınırı ayrıca tanımlanmaz.
20-063 — CEVAPLI — AGENTS.md çoğunlukla araçdan bağımsız metin; `docs/agents/*.md` Matt Pocock şablonuna bağlı. Temel iş (TASARIM, GLOSSARY, AGENTS) bağımsız çalışır.
20-064 — KARAR — Evet, ajan AGENTS.md'yi kendi başına değiştirmez; her değişiklik Levent'in açık izniyle. Bu izin deseni (commit `aa6ed79`) doğrulandı.
20-065 — KARAR — Boşa düşmez; belge işaretçidir. Skill yoksa ajan metni normal talimat olarak okur. Müdahale gerekmez.
20-066 — ZAYIF SORU — Ajanlar iki dili sorunsuz okur. Çeviri maliyeti faydayı aşar.
20-067 — KARAR — Kalıcı karar kaydı. ADR yok (20-019); sorgu dosyaları değiştirilmez, TASARIM'daki etiket onlara işaret eder.
20-068 — KARAR — 2.000 soru yönetilmez. Cevaplar TASARIM'a karar olarak işlenir (en çok ~30 karar); soru ve cevap dosyaları arşivdir, okunmaz.
20-069 — KARAR — Cevap dosyası `docs/sorgu/sorgu-4/` altında kalır, commit edilir. "Neden" için TASARIM'daki etiket (S4-n) o dosyaya işaret eder.
20-070 — YANLIŞ — Tek bir yer yok. AGENTS.md satır 3-4 yalnız TASARIM, KURALLAR, GLOSSARY'yi anıyor. Fix: AGENTS.md'ye 5 satırlık okuma sırası: TASARIM → KURALLAR → GLOSSARY; gerisi gerektiğinde.
20-071 — KARAR — Havuz doğrulanmaz; kural dosyaları kendi kaynak notlarını (kimlik) zaten taşıyor. Havuz yedeği beyin tarafında (kapsam dışı).
20-072 — KARAR — Belgenin başına "son doğrulama: tarih" satırı; yeniden doğrulama ilk veri koşusunda ajan işi (günlük tazelik kontrolü zaten §6 adım 1).
20-073 — CEVAPLI — §6 adım 1: "Sorun varsa kart üretilmez" ama Levent'e mesaj yazılı değil. Fix: aşağıda 20-074.
20-074 — KARAR — Her gün 19:30'da bir durum dosyası: `durum.txt` ("TAMAM 2026-10-05" ya da "HATA: neden"); kart yoksa bile yazılır. Dosya yaşı eskiyse çalışmamıştır.
20-075 — KARAR — Evet, Görev Zamanlayıcı (`schtasks`). Kurulumu tek komutla, geri dönüş rehberine (20-077) yazılır; Levent kuramaz, ajan kurar.
20-076 — KARAR — Sistem eksik günleri otomatik doldurur (veri güncelleme "son tarihten bugüne" indirir); elle komut gerekmez.
20-077 — KARAR — Evet: `GERI-DON.md`, 10 satır: 1) `.venv\...pytest` çalıştır, 2) durum.txt'e bak, 3) TODO.md'nin ilk bölümü.
20-078 — KARAR — Devralan için okuma sırası = 20-070 + GERI-DON.md; ek belge yok.
20-079 — KARAR — Bağımsız denetim ritüeli: her büyük aşamadan sonra (§7 adımları) taze bir ajan oturumu kodu TASARIM'a karşı denetler. Sızıntı/ileri bakış için tek test sınıfı yazılır.
20-080 — KARAR — Her büyük değişiklikten sonra, kapı olarak değil, §7 adımı sonunda. Zorunlu yapma; sıklık iş yüküyle orantılı.
20-081 — KARAR — TASARIM §7 adım 1 zaten silmeyi söylüyor. Karar TASARIM'da kalır; ayrı bilet/ADR gerekmez. Hangi parçanın kalacağı o iş yazılırken belli olur.
20-082 — KARAR — Hayır. `pythonpath=["."]` yeter; `src/` ve `pip install -e` ek adım, kazanç yok.
20-083 — KARAR — Her modül tek `.py` dosyası, `tansu/` altında düz. Alt klasör yok.
20-084 — KARAR — Yalnız belge. Fonksiyon adında `_` önekiyle iç olanlar işaretlenir. Import denetim aracı yok.
20-085 — KARAR — Sürüm numarası yok. İsim = git etiketi `kural-kaydi-N` (20-013). Rapor commit hash'ini taşır.
20-086 — KARAR — CHANGELOG yok; `git log` yetmez Levent için ama o okumaz. TODO.md "Yapıldı" bölümü (son 10) yeter.
20-087 — KARAR — Rapor dosya adı tarih taşır ve üzerine yazılmaz (yeni gün yeni dosya). Fark = iki dosya. Deneme günlüğü her koşuyu zaten yazar (§5.11).
20-088 — KARAR — Günlük `kayit/denemeler.csv` olarak git'te ve haftalık yedekte. Satır silinmesi `git diff` ile görünür.
20-089 — CEVAPLI — Git'te (20-088). Her koşu commit gerektirmez; ama silme/değiştirme sonraki commit'te diff'te görünür. Gizleme riski kalır, ajan kuralıyla "günlük yalnız eklenir" yazılır.
20-090 — KARAR — Teknik engel yok, güvene dayanır. Ucuz önlem: `kural-kaydi.toml` kayıttan sonra `attrib +R` ve etiket (20-013). Değişirse commit diff'i ve etiket farkı gösterir.
20-091 — KARAR — Mekanizma: ajan teste dokunduğunda son mesajında "test değişti: neden" yazar (AGENTS.md kuralı). Levent `git diff --stat tests/` ile bakabilir.
20-092 — KARAR — TODO.md'nin "Karar notu" bölümü; oturum sonunda ajan buraya 3 satıra kadar yazar. AGENTS.md'ye eklenir.
20-093 — YANLIŞ — Yazılı değil (20-038). Fix: belge hatası bulunca ajan durur, TODO.md'ye `ready-for-human` satırı yazar, kodu belgeye uydurmaz.
20-094 — KARAR — Hiçbiri otomatik değil, şimdilik disiplin. Tek aday: sabitlerin TASARIM ile testle karşılaştırılması (20-024).
20-095 — ZAYIF SORU — Tablo gereksiz: yalnız pytest zorunlu (20-056) ve ona maliyet yok. Ajan aboneliği ayrı iş kararıdır.
20-096 — CEVAPLI — Evet, çalışmalı: günlük akış (§6) saf Python + `schtasks`; ajan gerektirmiyor. Bunu TASARIM §6'ya gereksinim olarak bir cümleyle yaz.
20-097 — KARAR — Ölçüt: "araç, gerçekleşmiş bir arıza türünü testin yakalayamadığı yerde önlüyorsa eklenir" (20-056).
20-098 — KARAR — Ajan çözer: test, hata, biçim, `TODO.md` içi. Levent: parametre, kural, belge, bağımlılık, silme. Bu AGENTS.md'ye 2 satır (20-033).
20-099 — KARAR — Üç adım: `schtasks /delete`, `veri/` ve `rapor/` zip'i yedeğe, TODO.md'ye "ARŞİV" yaz. GERI-DON.md'ye eklenir.
20-100 — KARAR — Altyapı büyümesini durduran: yeni araç yalnız 20-097 ölçütüyle. Haftalık bakım süresi sınırı: 15 dakika (Levent'in izlemesi); aşılırsa araç çıkar.

## Özet

Doğrulama sayıları (100 soru): CEVAPLI 6, KARAR 71, YANLIŞ 11, OLGU 1, ZAYIF SORU 11. (Bazı satırlar karışık; sayımda satırın başlığındaki hüküm esas alındı. Sayımlar elle yapıldı, ±2 hata payı vardır.)

En önemli 10 kurulum kararı:

1. Yedek: haftalık otomatik `robocopy` ile tüm klasör (`.venv` hariç) harici sürücüye; `git bundle` ile geçmiş (20-001, 20-002).
2. Parquet git'ten çıkar: `.gitignore`'a `*.parquet`; `rapor/*.md` izlenir (20-005, 20-015). Şu an parquet zaten girmiş.
3. `.gitattributes`: `* text=auto eol=lf` (20-014).
4. Kod hash'i = `git rev-parse HEAD`; kirli çalışma ağacında kural kaydı koşusu reddedilir (20-006).
5. `rebase`, `--force`, `amend`, geçmiş temizleme yasak; `git add .` yasak (20-007, 20-016, 20-015).
6. AGENTS.md'ye eklenecekler: "Yapma" listesi, Python/pytest komutu, PowerShell, ana dal `master`, "belge hatasında dur ve sor", okuma sırası (20-037, 20-038, 20-039, 20-040, 20-070, 20-093). Levent izni gerekir.
7. `requirements.lock` (`pip freeze`); `uv`/`poetry`/ruff/mypy/pre-commit yok (20-046, 20-047, 20-054, 20-056).
8. Kapı = `.venv\Scripts\python.exe -m pytest`; ajan commit öncesi çalıştırır (20-058, 20-059).
9. Levent'e dönük üç dosya: TASARIM tepe özeti, `TODO.md` (şimdi + karar notu + yapıldı), `GERI-DON.md`; `.scratch/` yerine `TODO.md` (20-031, 20-035, 20-077).
10. Her gün `durum.txt` ("TAMAM tarih" ya da "HATA neden") 19:30'da yazılır; günlük akış ajansız çalışır; deneme günlüğü, anlık görüntü kaydı (sha256) ve `kural-kaydi.toml` git'te, yalnız ekleme (20-003, 20-004, 20-025, 20-074, 20-088, 20-096).
