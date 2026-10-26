# Faz 2: veri katmanı

Tarih: 26.10.2026. Dal: `faz-2-veri` → `yeniden-kurulus`.

## Yapılanlar

- `uyelik_hazirla`: her üyelik sürümü kendi tarih aralığını taşır (`UYELIK_SURUMLERI`); 2026 tarihi artık `UyelikKapsamHatasi` vermez.
- `tansu/referans/bist30_2026_v1/`: 2025 sonunda açık 30 satır + 2026Q2 (+VAKBN −ULKER) + 2026Q4 (+TRMET −DSTKF), resmi bağlantılar `kaynaklar.md` içinde.
- `veri.gunluk(anlik, sembol)` (SPEC 3.7) ve `veri.uyelik_araliklari` (KOZAL → TRALT, KOZAA → TRMET).
- `tansu veri`: 2021'den beri BIST 30'a girmiş 47 pay + SOKE, 2019'dan; son 10 görüntü tutulur.
- Kaynak düzeltmesi: tek uzun istek boş dönerse fiyat yıl yıl istenir.

## Koşular

1. 20:02 koşusu: 14 dakika ilerlemedi, durduruldu (`kanit/acik-sorular.md`).
2. 20:18 koşusu (görüntü 20261026-2018), inmeyenler:
```
AKSEN   -           -               0  inmedi
ALARK   -           -               0  inmedi
DOHOL   -           -               0  inmedi
```
3. 20:42 koşusu (görüntü 20261026-2042): yalnız ALARK inmedi. Neden: İş Yatırım ALARK için 01.01.2019-26.10.2026 tek isteğine boş gövde döndürdü (0 bayt); 2019, 2020 ve 2021'den bugüne istekleri geldi. Düzeltme: yıllık yedek istek (test: `test_uzun_aralik_bos_yanit_verirse_yil_yil_ister`).
4. Son koşu:

```
$ .venv\Scripts\python.exe -X utf8 -m tansu veri
anlık görüntü 20261026-2108; silinen eski görüntü: 0
sembol  ilk_tarih   son_tarih   satir  durum
AEFES   2019-01-02  2026-10-26   1955  tamam
AKBNK   2019-01-02  2026-10-26   1955  tamam
AKSEN   2019-01-02  2026-10-26   1955  tamam
ALARK   2019-01-02  2026-10-26   1955  tamam
ARCLK   2019-01-02  2026-10-26   1955  tamam
ASELS   2019-01-02  2026-10-26   1955  tamam
ASTOR   2023-01-18  2026-10-26    941  tamam
BIMAS   2019-01-02  2026-10-26   1955  tamam
BRSAN   2019-01-02  2026-10-26   1955  tamam
CIMSA   2019-01-02  2026-10-26   1955  tamam
DOAS    2019-01-02  2026-10-26   1955  tamam
DOHOL   2019-01-02  2026-10-26   1955  tamam
DSTKF   2025-02-06  2026-10-26    430  tamam
EKGYO   2019-01-02  2026-10-26   1955  tamam
ENKAI   2019-01-02  2026-10-26   1954  tamam
EREGL   2019-01-02  2026-10-26   1955  tamam
FROTO   2019-01-02  2026-10-26   1955  tamam
GARAN   2019-01-02  2026-10-26   1955  tamam
GUBRF   2019-01-02  2026-10-26   1955  tamam
HALKB   2019-01-02  2026-10-26   1955  tamam
HEKTS   2019-01-02  2026-10-26   1955  tamam
ISCTR   2019-01-02  2026-10-26   1955  tamam
KCHOL   2019-01-02  2026-10-26   1955  tamam
KONTR   2020-10-19  2026-10-26   1507  tamam
KRDMD   2019-01-02  2026-10-26   1955  tamam
MGROS   2019-01-02  2026-10-26   1955  tamam
ODAS    2019-01-02  2026-10-26   1955  tamam
OYAKC   2019-01-02  2026-10-26   1955  tamam
PETKM   2019-01-02  2026-10-26   1955  tamam
PGSUS   2019-01-02  2026-10-26   1955  tamam
SAHOL   2019-01-02  2026-10-26   1955  tamam
SASA    2019-01-02  2026-10-26   1955  tamam
SISE    2019-01-02  2026-10-26   1955  tamam
SOKE    2023-01-12  2026-10-26    945  tamam
TAVHL   2019-01-02  2026-10-26   1955  tamam
TCELL   2019-01-02  2026-10-26   1955  tamam
THYAO   2019-01-02  2026-10-26   1955  tamam
TKFEN   2019-01-02  2026-10-26   1955  tamam
TOASO   2019-01-02  2026-10-26   1955  tamam
TRALT   2019-01-02  2026-10-26   1955  tamam
TRMET   2019-01-02  2026-10-26   1955  tamam
TSKB    2019-01-02  2026-10-26   1955  tamam
TTKOM   2019-01-02  2026-10-26   1955  tamam
TUPRS   2019-01-02  2026-10-26   1955  tamam
ULKER   2019-01-02  2026-10-26   1955  tamam
VAKBN   2019-01-02  2026-10-26   1955  tamam
VESTL   2019-01-02  2026-10-26   1955  tamam
YKBNK   2019-01-02  2026-10-26   1955  tamam
```

## 2026 üyeliği ve günlük tablo

```
2026-03-31 30 AEFES AKBNK ASELS ASTOR BIMAS DSTKF EKGYO ENKAI EREGL FROTO GARAN GUBRF ISCTR KCHOL KRDMD MGROS PETKM PGSUS SAHOL SASA SISE TAVHL TCELL THYAO TOASO TRALT TTKOM TUPRS ULKER YKBNK
2026-04-01 30 AEFES AKBNK ASELS ASTOR BIMAS DSTKF EKGYO ENKAI EREGL FROTO GARAN GUBRF ISCTR KCHOL KRDMD MGROS PETKM PGSUS SAHOL SASA SISE TAVHL TCELL THYAO TOASO TRALT TTKOM TUPRS VAKBN YKBNK
2026-10-26 30 AEFES AKBNK ASELS ASTOR BIMAS EKGYO ENKAI EREGL FROTO GARAN GUBRF ISCTR KCHOL KRDMD MGROS PETKM PGSUS SAHOL SASA SISE TAVHL TCELL THYAO TOASO TRALT TRMET TTKOM TUPRS VAKBN YKBNK
2027-01-04: bist30_2026_v1: üyelik kapsamı eksik: 2027-01-04
TRALT gunluk: 2019-01-02 - 2026-10-26 1955 satir, 1454 uye gun
```

## Testler

```
$ .venv\Scripts\python.exe -X utf8 -m pytest -q
126 passed in 3.87s
```

CI (PR #195): testler geçti.
