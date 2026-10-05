# Sorular 15: Yapılandırma, kural kaydı, deneme günlüğü

15-001. Parametreler şu an kodda sabit (`kanit.py`'de `MASRAF = 0.002`, `STOP_ATR`, `aileler.py`'de `0.012`, `20`, `1.5`). Yeni sistemde bir parametrenin "kodda mı, dosyada mı" durduğuna hangi ölçüt karar verecek?

15-002. TASARIM 5.10 "parametre kaydı" ekinden söz ediyor, ama ek yok. Bu kayıt nerede, hangi biçimde (TOML, YAML, dataclass, tablo) duracak ve kim yazacak?

15-003. Parametre dosyasını Levent elle düzenleyecek mi, yoksa yalnız kod mu değiştirecek? Teknik olmayan bir sahip için yanlış girilmiş bir değer (virgül/nokta, "0,012" ile "0.012") nasıl yakalanacak?

15-004. TOML ve YAML arasında seçim yapılırsa, YAML'ın örtük tür dönüşümleri (ör. "no", "1e3", tarih) bir parametreyi sessizce bozarsa ne olacak? TOML'un `null` olmaması buna engel mi?

15-005. Dataclass, pydantic ya da düz sözlük: parametre şeması tek yerde mi tanımlanacak? Şemada olmayan bir anahtar dosyada görünürse sistem hata verecek mi, yoksa yok sayacak mı?

15-006. Aynı parametre hem kuralın (ör. EMA bandı %1,2) hem de sınama düzeninin (ör. 20 günlük blok, 1.000 tekrar) parçası olabilir. Hangi parametre "kural" sayılıp hash'e girer, hangisi "sınama ayarı" sayılıp dışarıda kalır?

15-007. Masraf (%0,1/%0,3/%0,5), likidite %2, pozisyon %10, 1.000.000 TL gibi simülatör ayarları kural kaydına dahil mi? Masraf senaryosu değişirse bu yeni deneme mi olur, aynı deneme mi?

15-008. TASARIM 5.10 "küçük rastgele ızgara" diyor. Izgara tanımı (hangi parametre, hangi aralık) kuralın parçası mı, ayrı bir kayıt mı? Izgaranın her hücresi ayrı deneme sayılacak mı?

15-009. YORUM etiketli değerler (KURALLAR.md: "her YORUM sınamada deneme sayısına girer") parametre dosyasında nasıl işaretlenecek? İşaret yoksa "kaynaktan gelen" ile "bizim doldurduğumuz" değer ayırt edilebilir mi?

15-010. Sadakat kontrolü sırasında seçilen YORUM değerleri (pencere 60 mı 120 mi, pivot ayarı) sonradan kural kaydına nasıl girecek? Kontrol sırasında denenen adaylar deneme günlüğüne yazılacak mı?

15-011. Aileye özgü parametreler ile risk paketi (2 ATR, SMA250) ortak parametreler aynı dosyada mı, ayrı dosyada mı? Ortak bir değer değişirse üç ailenin üçü de yeni deneme mi sayılacak?

15-012. Parametre dosyasında "varsayılan değer" kavramı olacak mı? Dosyada eksik bir anahtar kodun içindeki varsayılanla doldurulursa, hash'lenen şey dosya mı yoksa doldurulmuş son hâl mi?

15-013. Ortam bilgileri (veri klasörü yolu, Windows kullanıcı adı, saat dilimi) yapılandırmadan ayrı tutulacak mı? Yol değiştiğinde kural hash'i değişmemeli; bu ayrım nasıl güvence altına alınacak?

15-014. Parametre dosyası git'te mi duracak? AGENTS.md ve docs/agents/issue-tracker.md'ye göre depo yönetimi nasıl işliyor; git yoksa dosyanın geçmiş sürümü nereden kurtarılacak?

15-015. Tek kişinin kullandığı bir sistemde yapılandırma için ayrı bir kütüphane (pydantic-settings, hydra, dynaconf) gerçekten gerekli mi, yoksa `tomllib` + dataclass yeterli mi? "Minimum altyapı" ölçütü bunu nasıl cevaplıyor?

15-016. Hash tam olarak neyi kapsayacak: yalnız aile fonksiyonunun kaynak kodunu mu, çağırdığı yardımcıları (ema, atr) mı, motoru ve Adım fonksiyonunu mu? TASARIM 5.8 yalnızca "kodunun parmak izi" diyor.

15-017. Hash'e giren kod sınırı dinamik olarak (import grafiği) mı belirlenecek, yoksa elle yazılmış bir dosya listesiyle mi? Liste unutulursa bir yardımcıdaki değişiklik kayıtsız geçer.

15-018. Motor, Adım ve simülatör kod değişiklikleri kural hash'ine girerse, motordaki küçük bir hata düzeltmesi bütün ailelerin kaydını geçersiz kılar mı? Bu istenen davranış mı?

15-019. Veri anlık görüntüsü hash'e girecek mi? TASARIM 5.11 günlüğe "veri anlık görüntüsü" yazıyor ama 5.8 hash'te yalnız kural, parametre, kod diyor. Aynı kural farklı veriyle koşulursa aynı kayıt mı, farklı kayıt mı?

15-020. Hash tek bir birleşik değer mi olacak, yoksa üç ayrı hash (kod, parametre, veri) mi? Birleşik olursa bir değişikliğin hangi bileşenden geldiği sonradan nasıl anlaşılacak?

15-021. Hash algoritması olarak SHA-256 yeterli mi? Günlükte tam değer mi, kısaltılmış değer mi tutulacak ve kısaltma çakışma riski doğurur mu?

15-022. Kod hash'i kaynak metin üzerinden alınırsa boşluk, yorum satırı ve biçimlendirme (ruff/black) değişikliği hash'i bozar. Bu, "kod değişmedi ama yeni deneme sayıldı" sonucunu kabul edilebilir kılıyor mu?

15-023. Alternatif olarak AST üzerinden hash alınırsa yorumlar ve boşluklar etkisiz olur; ama değişken yeniden adlandırma hâlâ hash'i değiştirir. Hangi değişiklik "anlamlı" sayılacak ve bu çizgiyi kim çekecek?

15-024. Davranış hash'i (aynı sabit veride aynı sinyal günleri çıkıyor mu) kaynak hash'inden daha anlamlı olabilir mi? Bunun için bir "altın veri" paketi gerekir; Levent bu bakımı yapabilir mi?

15-025. Kaynak metin hash'inde satır sonu farkı (Windows CRLF ile LF) ve dosya kodlaması (UTF-8 BOM) hash'i değiştirebilir. Windows 11'de git `autocrlf` ayarı bunu sessizce etkiler mi?

15-026. Hash, kütüphane sürümlerini (pandas, numpy, pandas-ta-classic, statsmodels, quantstats) kapsayacak mı? pandas-ta-classic'in bir ATR hesabını değiştiren güncelleme, kod aynı kaldığı hâlde sonucu değiştirir.

15-027. Kütüphane sürümleri kilit dosyasıyla (uv.lock, requirements) sabitlenecek mi? pyproject.toml şu an yalnız pytest ayarı içeriyor; bağımlılıklar hiçbir yerde bildirilmemiş.

15-028. Python sürümü (3.11 / 3.12 / 3.13) hash'e ya da günlüğe girecek mi? Sürüm yükseltmesi kayan nokta ve sıralama davranışını değiştirmezse bile kayıtsız kalması kabul edilebilir mi?

15-029. Parametre hash'i için sözlük anahtar sırası, kayan noktaların yazılışı (0.012, 1.2e-2, 0.0120) ve tamsayı/kayan nokta farkı (20 ile 20.0) kanonik hâle nasıl getirilecek? Biçim farkı sahte "yeni kural" üretmemeli.

15-030. Hash'lenen parametre kümesi dosyadaki ham metin mi, ayrıştırılmış nesne mi? Yorum satırı eklemek TOML dosyasında hash'i değiştirmeli mi?

15-031. Kuralın "adı" (aile adı, sürüm etiketi) hash'e girecek mi? Aynı kod ve parametreyle iki farklı ad verilirse bir kayıt mı, iki kayıt mı oluşur?

15-032. Çift rotasyonunda çift seçim kuralı (her yıl başı, p < 0,05, en iyi 5) kuralın parçası. Seçilen çiftler her yıl veriden türetilir; bu türetilmiş liste hash'e mi girer, yoksa yalnız türetme kuralı mı?

15-033. Rastgele tohum (seed) ve tekrar sayısı (200 / 1.000) kural hash'ine mi, sınama ayarına mı ait? Tohum değişince p değeri değişir; bu yeni deneme mi?

15-034. Hash hesabını kim, ne zaman çalıştıracak: her koşuda otomatik mi, yoksa 5.8'deki "kural kaydı" adımında elle mi? Otomatikse kayıtlı hash ile koşu anındaki hash uyuşmadığında ne olacak?

15-035. Kayıtlı bir kuralın kodu sonradan değişirse (hata düzeltmesi) eski kayıt "geçersiz" mi sayılır, "yerini yeni kayıt alır" mı? Eski kaydın Holm'daki payı ne olur?

15-036. Hash'in hangi değişiklikte değişip hangisinde değişmemesi gerektiğine dair bir sınama seti olacak mı (boşluk ekle, yorum ekle, ad değiştir, sabiti değiştir)? Bu set olmazsa hash kuralı denetlenemez.

15-037. Refaktör sırasında bir fonksiyon başka modüle taşınırsa kaynak hash'i değişir. TASARIM 4 "içi değişse de dışı değişmez" diyor; hash bu söze uyuyor mu?

15-038. Kod hash'i Python bayt kodundan (`__code__.co_code`) alınırsa Python sürümüne bağlı olur. Bu seçenek hiç değerlendirilecek mi, yoksa kaynak metin mi şart?

15-039. Test dosyaları hash'e girecek mi? Motor sınamaları (5.3) kuralın doğruluğunun kanıtı; sınama değişirse kayıt etkilenmeli mi?

15-040. Kural kaydı bir dosya mı (ör. `kayit/<aile>.toml`), günlükteki bir satır mı, yoksa git etiketi mi? TASARIM 5.8 ve GLOSSARY "Kural kaydı" tanımı bunu söylemiyor.

15-041. Deneme günlüğü hangi biçimde saklanacak: CSV, JSON Lines, SQLite, Parquet? TASARIM DuckDB'yi "gereksiz katman" sayıyor; SQLite stdlib'de var, bu "minimum" ölçütüne uyar mı?

15-042. Günlük "yalnız eklenir" (append-only) olmalı. Bunu zorlayan nedir: dosya izni, SQLite tetikleyicisi, git geçmişi, zincirleme hash? Levent bir satırı elle silerse ya da düzenlerse bunu kim fark edecek?

15-043. Hash zinciri (her satır önceki satırın hash'ini içerir) tek kişilik bir sistemde aşırı mühendislik mi? Alternatif olarak günlüğün git'te commit'lenmesi yeterli olur mu?

15-044. Günlük satırı ne zaman yazılır: koşu başlamadan önce mi, bittikten sonra mı? Koşu yarıda çökerse (elektrik, bellek) o deneme sayılır mı sayılmaz mı?

15-045. "Başlamadan yaz" seçilirse sonuç sütunu sonradan güncellenir ve günlük artık salt-eklemeli olmaz. "Bittikten sonra yaz" seçilirse beğenilmeyen koşu hiç yazılmadan atılabilir. Hangisi seçilecek ve neden?

15-046. Günlükte hangi alanlar zorunlu: 5.11 tarih, aile, çıkış, parametre, veri anlık görüntüsü, kod hash diyor. Ham p değeri, etki büyüklüğü, tekrar sayısı, tohum, masraf senaryosu ve koşu süresi neden listede yok?

15-047. Günlükte parametreler tam kopya olarak mı, yalnız hash olarak mı tutulacak? Yalnız hash tutulursa bir yıl sonra hangi değerlerin denendiği geri kazanılabilir mi?

15-048. Sonuçlar (getiri, p değeri) günlüğe yazılacak mı? Yazılırsa günlük hem "ne denendi" hem "ne çıktı" kaydı olur; yazılmazsa Holm için p değerleri nereden gelecek?

15-049. Günlük dosyası yedeklenecek mi ve nerede? Tek PC'de disk bozulursa Holm'un bütün geçmiş deneme sayısı kaybolur ve sayı sıfırdan başlar; bu sessiz bir iyimserlik olur.

15-050. Günlüğe aynı anda iki koşu yazmaya çalışırsa (iki terminal, zamanlanmış 19:30 görevi ve elle koşu) dosya kilitleme ya da çakışma nasıl ele alınacak?

15-051. Günlük düzeltme gerektiren bir hata içerirse (yanlış aile adı, yanlış tarih) düzeltme nasıl yapılacak? "Düzeltme satırı" mı eklenir, yoksa düzeltmeye hiç izin verilmez mi?

15-052. Geliştirme koşuları (200 tekrar) ile son rapor koşuları (en az 1.000 tekrar) aynı günlüğe mi yazılır? Geliştirme koşuları da deneme sayılırsa Holm hızla katılaşır; sayılmazsa asıl hata kapısı açılır.

15-053. Sadakat kontrolü (KURALLAR §4) "getiriye bakmaz" ama birden çok aday formül dener. Bu denemeler günlüğe girecek mi? Girerse p değeri olmayan satırlar Holm'a nasıl dahil edilecek?

15-054. Günlükteki zaman damgası hangi saat dilimiyle yazılacak ve saat kaynağı nedir? Windows saatini Levent değiştirirse "kayıttan sonrası" ayrılmış dönem ölçütü (5.8) bozulur mu?

15-055. Günlük satırı bir koşu kimliği (UUID, sıra numarası) taşıyacak mı? Aynı koşunun rapor dosyaları, CSV'leri ve günlük satırı birbirine nasıl bağlanacak?

15-056. Günlükte "aile" birimi ile "çift bölmesi" birimi arasında fark var (TASARIM 5.6: sınama birimi bütün çift bölmesi). Bir günlük satırı neyi temsil eder: bir aile mi, bir bölme mi, bir hücre mi?

15-057. Günlük hangi sürümde ve hangi şemayla başlar? Şema sonradan değişirse (yeni sütun) eski satırlar nasıl okunur? Şema sürüm numarası olacak mı?

15-058. Günlük okunabilirliği: Levent günlüğü hiç açıp bakacak mı? Bakacaksa CSV/Excel uyumu, Türkçe karakter kodlaması ve ondalık ayırıcı ("0,05" ile "0.05") sorun çıkarır mı?

15-059. Silinen ya da arşivlenen bir ailenin günlük satırları kalır mı? Bir aile tasarımdan tamamen çıkarılırsa onun denemeleri Holm'dan düşer mi, düşmez mi?

15-060. Günlük, rapor çıktıları (markdown + CSV) ile aynı klasörde mi duracak? Raporlar yeniden üretilebilir ve silinebilir; günlük ise silinemez. Bu iki şey birbirine karışmayacak mı?

15-061. Holm düzeltmesinin "aile" mi, "deneme" mi, "hipotez" mi birimi üzerinden çalışacağı kesin değil. Aynı ailenin üç parametreli üç koşusu üç hipotez mi, tek hipotez mi sayılır?

15-062. TASARIM 5.11 "o ana kadarki bütün denemelerle Holm" diyor. Bu, sonradan eklenen denemelerin eski bir ailenin düzeltilmiş p değerini geriye dönük büyüttüğü anlamına mı geliyor? Eskiden "Canlı" olmuş bir aile geri düşebilir mi?

15-063. Holm, hipotez sayısı m'yi bilmek ister. m, günlükteki satır sayısı mı, benzersiz kural hash sayısı mı, benzersiz aile sayısı mı? Üç tanım çok farklı düzeltme çarpanı verir.

15-064. Holm'un bağımsızlık gerektirmeden çalışması iyi, ama denemeler güçlü biçimde ilişkili (aynı veri, benzer parametre). Aşırı katı bir düzeltme gerçek bir kuralı elerse bu kabul edilen bir bedel mi?

15-065. Holm'a hangi p değerleri girecek: her koşunun ham p'si mi, K1 rastgele kurala göre p mi, K2'ye göre p mi? Bir koşuda birden çok karşılaştırma (K1a, K1b, K2, üç masraf düzeyi) varsa bunların her biri ayrı bir test mi?

15-066. Masraf düzeyleri (%0,1, %0,3, %0,5) aynı hipotezin üç görünümü. Üçü de günlüğe ayrı deneme olarak yazılırsa m şişer; tek deneme yazılırsa hangi düzeyin p'si Holm'a girer?

15-067. 5.12.1 "ileri yürüme yıllarının birleşiminde" p değeri istiyor. Yıllık sonuçlar ayrı p değerleri olarak da günlüğe düşecek mi? Düşerse birleşik p ile yıllık p'ler aynı Holm sepetine karışmamalı; bunu ne ayıracak?

15-068. Holm hesabını yapan kod, günlüğü okuyup p değerlerini toplayacak. Bu hesabı `statsmodels.multipletests` mi yapacak, kendi kodumuz mu? "Güvenilir kütüphane" ilkesi burada geçerli mi, ve sürüm değişirse sonuç değişir mi?

15-069. Holm yerine Benjamini–Hochberg (FDR) ya da Bonferroni neden seçilmedi? Seçim 5.11'de "Holm" olarak sabit; bu karar kaç hipotezden sonra yeniden gözden geçirilecek?

15-070. Yan koşu türleri (ızgara sağlamlığı 5.10, rastgele kural tekrarları, sınama koşuları) günlükte "deneme" dışı mı işaretlenecek? Bir koşunun "deneme mi, destek mi" olduğunu tanımlayan alan olacak mı?

15-071. Başarısız ya da hata veren koşular (veri eksik, karantina nedeniyle boş sonuç) günlükte "deneme" sayılır mı? Sonuç üretmeyen bir koşu Holm'a p'siz girerse ne yapılacak?

15-072. Bir ailenin ilk kez kayda geçmesinden önce yapılan serbest keşif koşuları (geliştirme sırasında Levent ya da bir ajan çalıştırdı) günlüğe girmediyse m eksik sayılmış olmaz mı? Bu "gizli deneme" nasıl önlenecek?

15-073. Ajanlar (Codex, Claude) kod yazıp koşu yapabiliyor. Bir ajanın ara denemesinin günlüğe yazılması zorunlu mu, ve bu zorunluluğu kod mu sağlıyor, yoksa yalnız bir talimat mı?

15-074. Günlüğe yazmadan sonuç gösteren bir giriş noktası (ör. bir notebook, `python -c`, Streamlit "Kanıt" ekranı) olursa, deneme sayısını atlatan bir yol açılmış olur. Sonuç üreten tek bir koşu fonksiyonu mu bulunacak?

15-075. Streamlit "Kanıt" ekranı (TASARIM 3) rapor okuyor; ekranda parametre oynatıp sonuç gösteren bir kontrol olursa bu da deneme mi? "Sadece okur" sınırı nasıl korunacak?

15-076. Holm sonucu hangi dosyada ve hangi anda saklanır? Her rapor üretiminde yeniden mi hesaplanır, yoksa günlükte bir "Holm anlık görüntüsü" mü tutulur? Yeniden hesaplanırsa geçmiş raporlar tekrar üretildiğinde farklı p gösterir.

15-077. Holm sıralamasında eşit p değerleri (ör. 1.000 tekrarlı rastgele kuralda p = 0,001 tabanı) nasıl ele alınacak? Rastgele testte p tabanı 1/(n+1) iken Holm eşiği α/m'ye inerse hiçbir aile geçemez hâle gelir.

15-078. Tekrar sayısı n = 1.000 iken en küçük p ≈ 0,001. m = 60 olduğunda Holm eşiği 0,05/60 ≈ 0,0008 olur ve kabul matematiksel olarak imkânsızlaşır. Tekrar sayısı, deneme sayısına göre nasıl ölçeklenecek?

15-079. Aynı kodu ve parametreyi bir daha çalıştırmak (yeniden üretim kontrolü) günlüğe yeni bir satır ekler mi? Eklerse "yeniden üretimi doğrulamak" Holm'u şişirir; eklemezse nasıl ayırt edilecek?

15-080. Aynı kural hash'i + aynı veri anlık görüntüsü + aynı tohum için ikinci bir koşu olduğunda sistem bunu "tekrar" diye tanıyıp mevcut sonucu mu gösterecek, yoksa yeniden mi hesaplayacak? Önbellekleme anahtarı ne olacak?

15-081. Aynı kural hash'i ama farklı veri anlık görüntüsü (veri her gün güncelleniyor, 6. adım 19:30) yeni deneme mi? Her akşamki veri yenilemesi kural sayısını artırmadan ama p değerlerini değiştirerek günlüğü şişirir mi?

15-082. Aynı kural + aynı veri + farklı tohum ("rastgeleyi bir daha çevirip daha iyi p bulma") yeni deneme sayılacak mı? Tohumu seçerek p değerini oynamaya karşı bir kural var mı?

15-083. Levent yanlışlıkla çift tıklayıp iki kez koşturursa ya da bir koşu sırasında pencereyi kapatırsa, tekrarlanan satırlar kopya olarak mı işaretlenir, yoksa Holm'a iki kez mi girer? "Tek deneme" kimliğinin tanımı nedir?

15-084. Benzersiz deneme tanımı (kural hash + parametre hash + veri hash + sınama ayarı) bir "deneme kimliği" olarak üretilirse, günlüğe aynı kimlikle ikinci yazma reddedilecek mi? Reddedilirse sonraki geçerli yeniden koşular nasıl kaydedilecek?

15-085. Parametreyi çok küçük değiştirip geri almak (0,012 → 0,013 → 0,012) iki yeni deneme mi, bir yeni deneme mi? Geri alınan değer eski kayıtla aynı hash'e dönerse günlük bunu nasıl yorumlar?

15-086. Sahip "bir şeyi denedim ama iptal ettim" derse deneme geri alınabilir mi? Geri alma imkânı salt-eklemeli ilkeyle çelişir; imkân yoksa yanlışlıkla başlatılan koşu kalıcı olarak Holm'u ağırlaştırır.

15-087. Parametre ızgarası (5.10) 50 hücre koşturursa, her hücre ayrı hash alır. Izgara tek bir "sağlamlık denemesi" olarak mı günlüğe girecek, yoksa 50 ayrı deneme olarak mı? Hangisi ailenin Holm sepetini büyütür?

15-088. Rastgele kural karşılaştırmasının (K1) 1.000 tekrarı birer deneme değil, tek bir testin parçası. Bu tekrarlar günlükte hiç yer almayacak mı, yoksa özet satırıyla mı tutulacak?

15-089. Kural kaydı (5.8) "sadakat kontrolü bitince, ilk getiri koşusundan önce" yapılıyor. "İlk getiri koşusu" tanımı nasıl denetlenecek: kodda getiri hesaplayan her koşu kayıt şartı arar mı, yoksa bu yalnız süreç kuralı mı?

15-090. Kayıt öncesi getiri koşusunu engelleyen bir kapı (kayıt yoksa motor sonuç vermez) konacak mı? Kapı eklenirse geliştirme sırasında her motor sınaması bu kapıya takılır; muaf tutulacak koşular nasıl tanımlanacak?

15-091. Bir koşunun bugün aynı sonucu üretip üretmediğini bir yıl sonra doğrulamak için hangi nesneler saklanmalı: ham veri anlık görüntüsü, kütüphane sürümleri, kod sürümü, parametre, tohum? Bu listeden hangisi eksikse yeniden üretim iddiası boş kalır?

15-092. Veri anlık görüntüsü "tarihli ve değişmez" (TASARIM 4). Disk kullanımı: 100+ hisse × 11 yıl × her gün yeni anlık görüntü ne kadar yer tutar? Hangi sıklıkta ve hangi biçimde (Parquet, CSV) tutulacak, ve eskileri silinirse eski koşular yeniden üretilebilir mi?

15-093. Anlık görüntü kimliği nasıl üretilecek: tarih mi, içerik hash'i mi? Aynı gün iki kez indirme farklı veri getirirse (İş Yatırım geçmişi sonradan değiştirebiliyor) iki ayrı kimlik mi olacak?

15-094. Rastgele sayı üretimi: tohum nerede tutulacak (parametre dosyası, günlük, kodda sabit)? Her koşu için yeni mi üretilecek, yoksa sabit bir ana tohumdan mı türetilecek? Türetme yöntemi (`numpy.random.SeedSequence`) hangi kararla seçiliyor?

15-095. Küresel `np.random.seed` yerine her koşuya bir `Generator` geçirilmezse, koşu sırası ya da paralel iş sayısı sonucu değiştirir. Paralelleştirme (çok çekirdek) olacaksa tohum bölme nasıl yapılacak?

15-096. Aynı tohum, farklı numpy ya da Python sürümünde farklı sayı dizisi üretebilir. Üreteç algoritması (PCG64) sabit tutulsa bile bir kütüphane güncellemesinden sonra 15-091'deki yeniden üretim iddiası ne kadar geçerli kalır?

15-097. Yeniden üretim testi bir kez mi yapılacak, yoksa sürekli (her sürümde) mi? Altın bir koşunun çıktısını (ör. bir ailenin p değeri) saklayıp her değişiklikte karşılaştıran otomatik bir sınama olacak mı, ve bu sınamayı kim güncelleyecek?

15-098. Kayan nokta farkları (Windows'ta farklı BLAS/CPU) iki koşunun son basamaklarını ayırırsa "tam aynı" iddiası nasıl tanımlanacak: bit düzeyi mi, 1e-9 toleransı mı? Hash'e giren sonuçlar yuvarlanacak mı?

15-099. Geçmiş bir koşu yeniden üretilirken kullanılacak kod sürümü nasıl bulunacak? Günlükte yalnız hash varsa o hash'e karşılık gelen kaynak metin nerede arşivlenmiş olacak, yoksa hash tek başına işe yaramaz mı?

15-100. Bütün bu kayıt altyapısı (parametre dosyası, hash, günlük, Holm, anlık görüntü, tohum) hangi noktada "minimum" sınırını aşar? Levent bir hata durumunda (ör. "hash uyuşmuyor") neyi, hangi ekranda görecek ve neyi yapacak?
