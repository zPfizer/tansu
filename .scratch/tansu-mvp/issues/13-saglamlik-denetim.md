# 13: Sağlamlık ızgarası, boru hattı denetimi ve geleceği görmeme testi

**What to build:**
- `sinama` her ailenin önceden yazılmış ızgarasını (KURALLAR §3) koşar ve pozitif hücre oranını raporlar.
  Şart: ≥ %60.
- Boru hattı iki kez denetlenir: sentetik boş veriyle (yanlış kabul ≤ %5) ve enjekte edilmiş etkiyle (güç).
- Bir test "veriyi t'de kes, t öncesi sinyaller ve evren değişmesin" der.

**Blocked by:** 12

**Status:** ready-for-agent

- [ ] Izgara hücreleri `tur=destek` olarak günlüğe yazılır ve Holm m'ye girmez. Pozitif = K1'e göre ortalama
      fazla getiri > 0, %0,3 masrafla.
- [ ] Boru hattı denetimi bir komutla koşar. Sonucu rapora ve `docs/`'a yazılır. Yanlış kabul > %5 ise
      ilk resmi koşu yapılmaz.
- [ ] Geleceği görmeme testi parametriktir. Kapsadığı yerler: evren, göstergeler, iki ailenin sinyalleri,
      çift seçimi, likidite medyanı, faiz hizalaması.
- [ ] Süre ölçülür ve yazılır: 200 ve tam B tekrarının süresi. TASARIM'daki bütçe 200 tekrar için ≤ 5 dk.
      Aşılırsa önce algoritma hızlandırılır.
