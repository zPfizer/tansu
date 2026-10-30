# Tansu'nun Gartley kuralları ve Tansu-tam aday (30.10.2026)

İstek (Levent, 30.10.2026): "Gartley için tansu kaynaklarından tekrar bir kontrol yapabiliriz." İş, kod denetimi
oturumunda (`kanit/gartley-denetim.md`) ayrı bir kol olarak yapıldı.

Tam tablo (Tansu'nun sözleri, gönderi tarihleri ve kimlikleri, not yolları, her notun SHA-256'sı) yereldir ve Git'e
girmez: AGENTS.md, Ek B #12 kararına kadar Tansu alıntılarını, gönderi kimliklerini ve beyin yollarını Git dışında tutar.
Bu dosya yalnız kuralların içeriğini, kodla farkını ve ön kaydı verir.

## Yöntem

- Tabloyu, hiçbir sınama sonucunu görmemesi istenen yeni bir alt ajan kurdu. Tansu havuzunda 115 not tarandı, 60'ı
  kaynak olarak kullanıldı. Yalnız Tansu'nun kendi gönderi metni ve görsel metni kural sayıldı; her satıra kaynak türü
  verildi (kendi metni, görsel metni, başka yazar, belirsiz).
- Çelişkide sonuç kullanılmadı; sabit sıra: (1) kendi metni görsel metninden, görsel metni başkasından önce; (2) sayı ve
  kesin şart veren ifade belirsiz olandan önce; (3) daha yeni gönderi.
- Dürüstlük notu: ajan, okumasına izin verilen yerel kural kartında, SPEC'in bir satırında, `plan.md`'de ve otomatik
  hafıza notunda eski sonuç bilgisi gördü (ör. "93,7 < 95"). Hiçbir kural seçimi bu bilgiye dayanmadı.

## Kural tablosu özeti (kodla karşılaştırma)

| Konu | Tansu'nun kuralı (özet) | Kod (`gartley.py`, `yapi.py`) | Sonuç |
|---|---|---|---|
| Pivot | 15 günlük salınım penceresi (2026, kendi metni); eski görselde yüzde zigzag | `sag_bar_15` varsayılan; dondurulmuş ayar `sag_bar_12` | Aynı (15 bar her yan okuması) |
| X, A, B, C | Ardışık dip-tepe-dip-tepe; X < B < C < A | Aynı; PR 253'ten sonra her nokta bacağının ucu | Aynı |
| AB/XA | 0,618, %3-5 tolerans | 0,618 ± tol × 0,618 | Aynı |
| BC/AB | 0,382 ile 0,886 arası, kesin sınır | Sınırlar tol kadar genişletilmiş | Farklı |
| D | A − 0,786 (A − X) | Aynı | Aynı |
| CD/BC | 1,272 ya da 1,618 (iki nokta) | 1,272-1,618 aralığı (± tol) | Farklı |
| Giriş | D'de alış limiti | D'de limit | Aynı |
| Emir süresi | Tansu vermiyor | 10 gün (varsayım) | Varsayım |
| Teyit | RSI(14) > 50, artan hacim, talep bölgesi, trend kırılımı: bilgi olarak, sayısal şart yok | Ürün kodunda yok; `yontem.py` teyitli girişte var | Tansu-tam'da şart değil |
| Stop | X | X, dokunuş | Aynı |
| Hedefler | Hedef 1 = D + 0,382 (A − D) %50; hedef 2 = D + 0,618 (A − D) kalan | Aynı | Aynı |
| R/R kapısı | Hedef 1'e göre en az 1,5 (ya da 2) | 1,4 (Levent kararı, SPEC Ek B #13) | Farklı; aşağıda |
| 10 gün | D'den sonra 10 günde hareket yoksa "belirsiz" etiketi | Emir süresi olarak 10 | Farklı anlam |
| Yön, zaman dilimi | Ayı yönü ve haftalık da var | Yalnız boğa, günlük | Kapsam dışı |
| Tansu yöntemi betiği | 3 ATR iz stop, açılış stopu, teyit günü kuralı, 10 gün süre stopu, AB=CD q ≤ 0,886 | `yontem.py` | Tansu'nun kuralı değil |

R/R kapısı çelişkisi: D 0,786'da, stop X'te ve hedef 1 A-D'nin 0,382'sindeyken oran her kurulumda 0,382 × 0,786 /
0,214 = 1,403'tür. Tansu'nun yazdığı 1,5 kapısı her kurulumu eler; kural harfiyen uygulanınca işlem olmaz.

## Tansu-tam Gartley (ön kayıt; ayar grubunda ilk koşudan önce gönderildi)

Kural (günlük, yalnız alış):

1. Pivot `sag_bar_15`; X dip, A tepe, B dip, C tepe ardışık; X < B < C < A; her nokta kendi bacağının ucu (PR 253).
2. AB/XA 0,618 ± %5 (oranın payı).
3. 0,382 < BC/AB < 0,886, toleranssız.
4. D = A − 0,786 (A − X); D'deki CD/BC, 1,272'ye ya da 1,618'e %5 içinde yakın.
5. Sinyal C'nin onay günü; ertesi günden D'de alış limiti, 10 işlem günü geçerli (Tansu süre vermiyor: varsayım).
6. Stop X, dokunuş. Hedef 1'de %50, hedef 2'de kalan. İz stop, açılış stopu ve başabaş yok.
7. R/R kapısı 1,4: Tansu'nun 1,5'i bütün kurulumları elediği için Levent'in kayıtlı kararı (SPEC Ek B #13) uygulanır.
   Stop X iken bu kapı hiçbir kurulumu elemez.
8. Para katmanı ve maliyet, öbür adaylarla aynı: `kanit/gartley-para/ayar.json` boyut, nakit ve maliyet bölümleri.

Kod: `kanit/gartley-denetim/tansu_tam.py`. Koşu sırası: önce ayar grubu (371 hisse, 2015-2022), bilgi için. Seçim
yoktur; aday, 2010-2014 son sınavının aday listesine girer (veri temizse). Ayrık grupta koşmaz.

Tansu-tam AB=CD aday değildir: kurallarının çoğu gönderi kimliği olmayan yapıştırılmış metinlerden gelir ve AGENTS.md
kanıt kuralı 3'e göre bir seviyenin tek kaynağı olamaz.
