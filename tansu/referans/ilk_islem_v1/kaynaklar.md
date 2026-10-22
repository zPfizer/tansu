# İlk işlem günü kaynakları

Bu iki kayıt, TASARIM §5.15 #178 içindeki açık `ilk_islem_v1` seçimine aittir.
Yalnız İş Yatırım kaynak etiketini, tarihli borsa kodunu ve belirtilen görüntüyü bağlar.
Borsa duyurusundaki `.E` pay eki CSV koduna eklenmez. Yeni bir kalıcı pay kimliği tanımlamaz.

- ASTOR: Borsa İstanbul, duyuru 13031, 18.01.2023. [Özgün duyuru](https://www.borsaistanbul.com/duyuru/13031/borsa-istanbulda-gong-astor-enerji-icin-caldi).
  Kaynak geçişi: “18 Ocak 2023 tarihi itibarıyla Borsa İstanbul Yıldız Pazar’da, "ASTOR.E" koduyla işlem görmeye başladı.”
  Kaynak hazırlığındaki geçiş satırları 232–235. İlk işlem günü 18.01.2023, ilk üyelikten öncedir.
- DSTKF: KAP, bildirim 1389178, 04.02.2025 18:10:14. [Özgün bildirim](https://www.kap.org.tr/tr/Bildirim/1389178).
  Kaynak ilk işlem gününü 06.02.2025, pay kodunu DSTKF.E ve şirketi Destek Finans Faktoring A.Ş. olarak bildirir.
  Kaynak hazırlığındaki geçiş satırları 79 ve 124–151. Bildirim ilk işlem ve üyelikten öncedir.

22.10.2026 tarihli sınırlı kaynak hazırlığı iki ilk günü değişmemiş görüntüyle
karşılaştırdı. Kayıtlı takvimde ASTOR için 2025 sonuna kadar 737, DSTKF için 226
kapanış vardır; ilk gün ile ilk kayıt eşleşir ve bu kayıtlı takvime göre iç boşluk yoktur.
ASTOR'un bu takvimde 500'üncü gözlemi 21.01.2025'tir. Bu sayılar çalışma anında
varsayılan veya uygunluk izni değildir; E1 her istekte kendi kesimini doğrular.

Kanıt sınırı: kayıtlı takvim resmî tam tatil/seans arşivi değildir. Bu kaynaklar
bütün kalite, karantina, fiyat düzeltme veya dolum kurallarını kanıtlamaz.
İlk gün kaynağı bulunmayan payın ilk gözlemi resmî başlangıç sayılmaz.
Yeni kaynak veya görüntü yeni sürüm/seçim ve başvuru gerektirir.
