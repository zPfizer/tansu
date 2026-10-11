# 06: TASARIM değişmez kurallarının hepsi testle korunur

**What to build:** Kodda olan ama testi olmayan her değişmez kural, dış davranıştan sınayan bir testle korunur. Kural bozulunca CI kırmızı olur.

**Blocked by:** 07 (yalnız rapor üstüne yazmama kuralı; testler ve kod düzeltmesi 07'ye taşındı, bu dalın kart testlerini engellemez)

**Status:** done (bu dalın kart testleri teslim edildi; rapor kuralı ve iki kırmızı test orkestratör kararıyla 07'ye taşındı)

- [x] Bu dalın kart durumları ve kapanmış kartın yalnız kapanış günü görünmesi için kırmızı/yeşil test var (`/tdd`); önceki kuralların kanıtı Comments'te, rapor kuralının kod sapması ve testleri 07'de.
- [x] Yokluk kuralları (Yahoo/TradingView yok, valör yok, fiyat yamanmaz) için mevcut kaynak ve davranış testleri yeşil: `tests/test_kaynak.py:339`, `tests/test_simulator.py:396`, `tests/test_veri.py:417`.
- [x] `pytest -q` yeşil; test gevşetilmedi (AGENTS.md test kuralları).

## Kalan iki kural

- [x] Kart durumları ve kapanmış kartın yalnız kapanış günü görünmesi: günlük CSV yüzünde kırmızı/yeşil kanıt.
- [x] Rapor üstüne yazmama: HTML ve işlem CSV'sinin iki kırmızı testi aynen 07'ye taşındı; düzeltme ve yeşil kanıt 07'nin işidir.

## Comments

10.10: 18 test yazıldı (Codex Sol), Claude koştu ve mutasyonla denetledi: 16 testte kural bozulunca test kırmızı
(sırayla kod değişikliği uygulanıp geri alındı). Mutasyonla denetlenmeyen 3 test: piyasa durumu, karantina yamanmaz,
çift bölmesinde stop/hedef yok (dış davranış testleri; doğrudan kırıcı tek satır bulunamadı).
Kalan: kart durumları (bilet 02 değiştirebilir, ondan sonra); rapor üstüne yazmama (kod TASARIM'dan farklı, bilet 07).
/code-review (10.10, Codex iki eksen): literal sabit ihlali düzeltildi. Kısmi kalanlar (sonraki tur): aynı gün testinde
giriş ve kapanış fiyatı aynı (kapanışla değerleme hatası yakalanmaz); olay oranının koşu sonucuna aktarılması; dinamik
geri import; borsapy fiyat çağrısının davranış testi; simülatörde evren çıkışı; yalnız seçilmiş çiftlere eklenen stop.

10.10 (06b): Yalnız kalan iki kurala test eklendi; üretim kodu ve önceki testlerin assert'leri değişmedi.
Kart: `tests/test_gunluk.py:305`, stop, kilitli tabanda bekleyen stop, SMA250 çıkışı ve giriş iptali.
Durum etiketi ve kapanmış kartın ertesi güne taşınması ayrı ayrı yalnız bellekte bozularak denetlendi:

```powershell
.venv\Scripts\python.exe -c "import pytest; from tansu import gunluk; gunluk._durum = lambda p: 'AKTİF'; raise SystemExit(pytest.main(['-q', '-p', 'no:cacheprovider', '--basetemp=.codex-tmp', 'tests/test_gunluk.py', '-k', 'kart_durumlari']))"
```

Çıkış 1: `4 failed, 12 deselected in 0.87s` (yanlış durum etiketi).

```powershell
.venv\Scripts\python.exe -c "import inspect, pytest; from tansu import motor; exec(inspect.getsource(motor.tara).replace('        kapanan = None', '        # kapanan korunur'), motor.__dict__); raise SystemExit(pytest.main(['-q', '-p', 'no:cacheprovider', '--basetemp=.codex-tmp', 'tests/test_gunluk.py', '-k', 'kart_durumlari', '--tb=line']))"
```

Çıkış 1: `4 failed, 12 deselected in 0.84s` (ertesi gün CSV boş değil).

```powershell
.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=.codex-tmp tests/test_gunluk.py -k kart_durumlari
```

Çıkış 0: `4 passed, 12 deselected in 1.00s` (gerçek kod).
Rapor: `tests/test_simulator.py:74`, iki farklı gerçek simülasyonun dolu işlem listesiyle aynı koşu kimliği yeniden yazılır.
İki boş CSV'nin sahte yeşil vermemesi ayrıca assert ile korunur.

```powershell
.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=.codex-tmp tests/test_simulator.py -k rapor_ayni --tb=short
```

Çıkış 1: `2 failed, 18 deselected in 1.07s`; ilk dosyaların baytları değişti.

```powershell
.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=.codex-tmp
.venv\Scripts\ruff.exe check tansu tests .github
.venv\Scripts\ruff.exe format --check tansu tests .github
```

Tam pytest çıkış 1: `2 failed, 309 passed in 52.54s`; iki hata rapor regresyon testlerinde.
Ruff check çıkış 0: `All checks passed!`; format çıkış 0: `44 files already formatted`.
Rapor için yeşil kanıt ve `Status: done` verilemedi: kullanıcı üretim kodu değişikliğini yasakladı;
üstüne yazma hatası bilet 07'de zaten kayıtlı. Commit kullanıcı talimatıyla orkestratöre bırakıldı.

10.10 (06b öz inceleme düzeltmesi): Spec ekseni karantina kartının eksik olduğunu buldu; aynı parametrik teste
karantina vakası eklendi (`tests/test_gunluk.py:314`). Yüz temiz geçmiş günle tek bozuk gün veri kapısının altında
kalır; gerçek günlük CSV'de AKTİF, AKTİF, BOZULDU, kart yok sırası literal olarak denetlenir.
Yukarıdaki durum mutasyonu komutuna `--tb=line` eklendi: çıkış 1, `5 failed, 12 deselected in 0.78s`.
Yukarıdaki kapanış taşıma mutasyonu aynı komutla yeniden koştu: çıkış 1, `5 failed, 12 deselected in 1.02s`.
Yukarıdaki kart yeşil komutu yeniden koştu: çıkış 0, `5 passed, 12 deselected in 1.03s`.
Öz inceleme son diff'te Standards ekseninde yeni ihlal bulmadı; Spec ekseninde yalnız raporun yeşil engeli kaldı.
İnceleme yüzü `git diff master -- tests/test_gunluk.py tests/test_simulator.py` (çıkış 0).
Commit yasak olduğu için `git diff master...HEAD` boş; inceleme çalışma değişikliklerinden yapıldı.
Ruff check ve format komutları son test değişikliğinden sonra yeniden geçti (çıkış 0).
Son tam pytest, yukarıdaki aynı komutla: çıkış 1, `2 failed, 310 passed in 51.64s`.
İki hata raporun HTML/CSV üstüne yazma testleridir; kartın beş vakası yeşildir.

10.10 (orkestratörün kapsam düzeltmesi): Raporun iki kırmızı testi ve yeniden koşulan hata özeti aynen
07'ye taşındı. Bu dalın kabulü kart testleri ve bu devirdir; rapor kuralı için yeşil iddiası yoktur.
Önceki kapsamın tamamında kırmızı kanıt iddiası yoktur; yukarıdaki mutasyonla denetlenmeyen kurallar kaydı korunur.
Durum `done`; rapor kuralının bağımlılığı 07'dir. Üretim kodu değişmedi; `tests/test_simulator.py` master ile aynıdır.

Bu koşunun kanıtı:
- `/tdd` kırmızı: yukarıdaki durum mutasyonu (`--tb=line` ile), çıkış 1, `5 failed, 12 deselected in 0.74s`;
  kapanış taşıma mutasyonu, çıkış 1, `5 failed, 12 deselected in 1.07s`. Yalnız bellekte değişiklik.
- `/tdd` yeşil: `.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=.codex-tmp`,
  çıkış 0, `310 passed in 50.01s`; kartın beş vakası dahil.
- Ruff check ve format: yukarıdaki aynı komutlar, ikisi çıkış 0; `All checks passed!`, `44 files already formatted`.
- `/code-review`: `git diff master -- tests/test_gunluk.py tests/test_simulator.py .scratch/belge-hizasi/issues/06-degismez-kural-testleri.md .scratch/belge-hizasi/issues/07-kod-sapmalari.md`, çıkış 0.
  Sabit nokta master: `4c3199ee7b8888306ca694cf00b6c8f1cafe5003`; commit farkı boş olduğundan çalışma farkı incelendi.
  İki paralel bağımsız alt ajan: Standards 0 bulgu, Spec 0 bulgu. Spec denetçisi taşınan bloğu özgün okuma ile karşılaştırdı.
- Commit adımı: `git add -- tests/test_gunluk.py .scratch/belge-hizasi/issues/06-degismez-kural-testleri.md .scratch/belge-hizasi/issues/07-kod-sapmalari.md`,
  çıkış 1: `fatal: Unable to create 'C:/Users/levent/Desktop/TANSU/.git/index.lock': Permission denied`.
  Commit yapılamadı; izin engeli aşılmadı. Push, PR ve merge yapılmadı; bu işler orkestratöre aittir.
- `.codex-tmp` temizliği: yalnız depo içindeki mutlak hedef doğrulandıktan sonra `Remove-Item -LiteralPath $hedef -Recurse -Force -ErrorAction Stop`
  araç politikası tarafından reddedildi (`blocked by policy`); işlem çalışmadı, çıkış kodu yok. Klasör kaldı; alternatif silme yolu denenmedi.
- `/retro`: önceki kapsam hatası bu devirle düzeltildi; standartlar dosyasındaki mevcut "Olmayanı var gibi yazma" kuralı geçerlidir.
  Tüm belge hizası işi bitmediği ve PR birleşmediği için spec/bilet arşivlenmedi. Genel bitiş kanıtı eksik: commit ve geçici klasör temizliği.
