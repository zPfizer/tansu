# 02: Tansu'nun fikri olan yerde YORUM kalmaz

**What to build:** Tansu'nun fikirleri esastır; YORUM yalnız Tansu'nun o konuda fikri yoksa geçerlidir (Levent 10.10,
KURALLAR "Okuma kuralları"). KURALLAR, TASARIM ve kart düzenindeki her YORUM ve her Tansu'dan ayrılma bu ilkeye göre
denetlenir: Tansu'nun fikri varsa kural ona çevrilir; uygulanamıyorsa nedeni KURALLAR'a yazılır.

**Blocked by:** 01

**Status:** done (PR #5, ce0fe60)

- [ ] KURALLAR, TASARIM ve `docs/kurallar/A–E`'deki her YORUM listelendi. Her biri için Tansu havuzunda (not ve görsel) o konuda fikir arandı;
      sonuç üç sınıftan biri: Tansu sessiz (YORUM kalır) · Tansu'nun fikri var (kural Tansu'ya çevrilir) · Tansu'nun fikri var ama
      uygulanamaz (neden yazılır). Kaynak yeri her satırda.
- [ ] Başlangıç listesi, sözlüğün Tansu denetiminden (10.10): çift seçiminde aynı sektör şartı (Tansu farklı sektörden de çift kurar);
      EMA sıkışmasında girişin sıkışma bittikten sonra olması (Tansu'nun ön sinyali sıkışma sürerken çıkar, parametrelerini vermedi);
      işlem fiyatı AOF (Tansu ertesi gün açılış kullanır; İş Yatırım verisinde açılış yok); gün sonu stopunda ertesi gün çıkış;
      kart durumlarının pozisyona bağlanması; likidite ölçüsü; sabit parametre ile Tansu'nun walk-forward ayarı; şok filtresi.
      İkinci tur (aynı denetim): mum (Tansu'da açılışlı; veride açılış yok), ATR'de Wilder yumuşatması, adedin aşağı yuvarlanması,
      β için log fiyata OLS, stop ve gün sonu stopunun adları (NotebookLM infografiği), harmonik D hedefi, ilk girişe kadar nakit. Üçüncü tur: "bozulma" Tansu'da formasyonun geçersizleşmesidir; projede SMA250 altı kapanışın (kart durumu BOZULDU) adı olması uygun mu.
      Denetim çıktısı: `$TEMP/codex-sozluk-tansu-cikti.md`, `codex-sozluk-tansu-cikti2.md` (10.10).
- [ ] Kurala çevrilen her değişiklik TASARIM/KURALLAR'a karar etiketiyle yazıldı; kural kaydından sonra değiştiyse yeni deneme sayıldı.
      Kod değişikliği gerekiyorsa bilet 07 gibi ele alınır (önce davranışı gösteren test).
- [ ] Levent'e yalnız Tansu'nun fikrinin okunuşu belirsiz kalan yerler soruldu.
- [ ] Bağımsız denetçi aynı listeyi havuza karşı yeniden okudu; Tansu'nun fikri olduğu halde YORUM kalan yer yok.

## Comments

- 14.10: Status, commit ce0fe60 (PR #5, 10.10) ile eşlendi. Kutular madde madde doğrulanmadı; kanıt `denetim/tansu-sapma.md` ve
  `denetim/tansu-sapma-dogrulama.md`. Bulgu: YONETIM uygunluk denetimi 14.10 (bilet 09).
