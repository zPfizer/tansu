# Sorular 17: Rapor, kart, ekran

17-001. TASARIM §3 "tek sayfalık Streamlit Kanıt ekranı" diyor, ama §3 aynı yerde "Streamlit kart paneli" için "gereksiz katman" diyor. Raporu zaten markdown okunuyorsa Streamlit'in ilk sürümde varlık nedeni nedir?

17-002. Levent raporu hangi uygulamada açacak: Not Defteri, VS Code, tarayıcı, Obsidian? Bu seçim markdown'ın (tablo, başlık, görsel) okunabilirliğini nasıl etkiliyor?

17-003. Markdown tablolar Windows'ta varsayılan uygulamada düzgün görünmüyorsa, rapor biçimi olarak HTML ya da PDF neden değerlendirilmedi?

17-004. `tansu/rapor.py` raporu f-string ile birleştiriyor. Yeni tasarımda Jinja2 gibi bir şablon kütüphanesi mi, yoksa pandas `to_markdown` mı kullanılacak ve bu seçimin gerekçesi nedir?

17-005. Şablon kullanılacaksa metin ile hesap nerede ayrılıyor? Şablon içinde yuvarlama ve yüzde biçimlendirme yapılırsa rakamlar iki yerde mi hesaplanmış olur?

17-006. Rapor dosya adı `kanit-<tarih>.md`. Aynı gün ikinci koşu dosyanın üstüne mi yazar, yoksa yeni dosya mı açar? Hangisi deneme günlüğüyle (§5.11) uyumlu?

17-007. Rapordaki her rakamın hangi koşudan, hangi veri anlık görüntüsünden ve hangi kod hash'inden geldiği raporun içinde mi yazacak? Hangi satırda?

17-008. Rapor Levent'in "hiçbir aile geçmedi" sonucunu (§1) ilk satırda mı gösterecek? Bu cümlenin tam metni kim tarafından ve nerede tanımlı?

17-009. Levent'in raporda hangi sayıyı ilk okuyacağı belli mi? İlk ekranda kaç rakam olacak ve hangileri?

17-010. Raporda p değeri, Holm düzeltmeli p, güven aralığı ve "saptanabilecek en küçük etki" birlikte duruyor. Teknik bilgisi olmayan bir okuyucu "ayırt edilemiyor" cümlesini bu rakamlardan hangisine dayanarak anlayacak?

17-011. Kanıt satırı örneği (§6.4) "−%0,2 ± %1,1" yazıyor. ± ne demek: standart hata mı, %95 aralık mı? Kartta bu nasıl açıklanacak?

17-012. Rapor Türkçe yazılırsa istatistik terimleri (bootstrap, Holm, walk-forward) için GLOSSARY'ye girecek karşılıklar kim tarafından belirlenecek?

17-013. Rapor ekran görüntüsü ve grafik içerecek mi? Markdown içinde gömülü PNG mi, dosya bağlantısı mı, yoksa grafiksiz mi?

17-014. quantstats tearsheet HTML üretir ve bu HTML İngilizcedir. Türkçe raporla yan yana nasıl sunulacak, yoksa hiç sunulmayacak mı?

17-015. quantstats tearsheet'i karşılaştırma serisi olarak neyi alacak? Eşit ağırlıklı sepet (K2) bir getiri serisi olarak quantstats'a verilebilir mi, ve verilmezse tearsheet hangi referansa karşı çizer?

17-016. quantstats'ın varsayılan ölçütleri (Sharpe, CAGR) §2'deki "Yüksek Sharpe modeller ilk virajda patlar" ilkesiyle çelişiyor mu? Raporda Sharpe gösterilecek mi?

17-017. quantstats bakımı ve pandas sürüm uyumu güvenilir mi? Kütüphane sürümü bozulursa rapor üretimi durur mu, yoksa tearsheet isteğe bağlı mı?

17-018. Plotly kullanılacak mı, Streamlit'in yerleşik grafikleri mi, matplotlib mi? Üç seçenekten hangisi "en az altyapı" ölçütünü sağlıyor?

17-019. Grafikler hem markdown raporuna hem Streamlit ekranına girecekse aynı grafik kodu iki yerde mi yazılır? Tek kaynak nasıl sağlanıyor?

17-020. Sermaye eğrisi, düşüş (drawdown) ve yıllık fazla getiri grafiklerinden hangileri ilk sürümde zorunlu? Kabul ölçütü (§5.12) hangi grafiği gerektiriyor?

17-021. Streamlit'in telemetri (usage stats) ayarı varsayılan açıktır. Yerel, tek kişilik bir sistemde bunu kapatan ayar nerede yazılı?

17-022. Streamlit yalnızca 127.0.0.1'e mi bağlanacak? Bunu garanti eden ayar hangi dosyada ve bir güncelleme varsayılanı değiştirirse kim fark edecek?

17-023. Levent Streamlit'i nasıl başlatacak: terminal komutu mu, çift tıklanan .bat dosyası mı, Görev Zamanlayıcı mı? Non-teknik biri için hangisi kabul edilebilir?

17-024. Streamlit sunucusu kapatılmazsa arka planda çalışıp kalır. Levent bunu nasıl fark edecek ve nasıl kapatacak?

17-025. Streamlit portu (8501) başka bir uygulamayla çakışırsa Levent ne görecek? Hata mesajı Türkçe ve anlaşılır olacak mı?

17-026. Streamlit her etkileşimde betiği baştan çalıştırır. "Raporu ve piyasa durumunu okur" (§3) dediğine göre her yenilemede dosyalar yeniden mi okunur, önbellek var mı, ve önbellek bayat veri gösterirse kim uyarır?

17-027. Ekran hesap yapacak mı, yoksa yalnız hazır dosyaları mı gösterecek? Hesap yaparsa Adım/Motor kodunu içe aktarıp ikinci bir sonuç kaynağı oluşturmuş olmaz mı?

17-028. Ekran hangi dosya biçimini okuyacak: markdown, CSV, parquet, JSON? Bu "rapor modülü" ile ekran arasındaki sözleşme (§4 "küçük yüz") nerede tanımlı?

17-029. Rapor modülü markdown ve CSV yazıyor (§4). Ekranın okuyacağı yapısal sonuç (rakamlar, tablolar) markdown'dan ayrıştırılarak mı alınacak? Markdown'ı geri ayrıştırmak kırılgan olmaz mı?

17-030. Rapor ile ekran farklı rakam gösterirse hangisi doğru kabul edilir? Bunu yakalayan bir sınama var mı?

17-031. Ekranın ilk sürümde tek sayfa olması kararı, "kart ekranı bir aile kabul edilince" (§3) eklenecek demek. Eklendiğinde sayfa mimarisi (çok sayfalı Streamlit) yeniden mi yazılacak?

17-032. "Hiçbir aile geçmedi" ekranında tam olarak ne görünecek? Boş ekran mı, her ailenin hangi ölçütte düştüğünü gösteren tablo mu?

17-033. Ekranda ölçüt başına (§5.12 madde 1–6) geçti/kaldı gösterilecek mi? Bu tablonun kaynağı hangi veri yapısı?

17-034. Ekran, deneme aileleri varsayılan olarak gizli (§6.3) kuralına uyacak mı? Gizlenen aileleri göstermek için düğme olacak mı ve düğme P1 ilkesini (yanıltıcı sunum yok) bozar mı?

17-035. Ekranda "Tansu'nun sistemi" gibi okunabilecek bir ifade çıkmaması (P5) nasıl denetleniyor? Metin sabitleri tek yerde mi tutuluyor?

17-036. Streamlit ve bağımlılıkları (tornado, pyarrow, protobuf vb.) büyük bir kurulum getirir. Tek kişilik bir tarayıcı kısayoluyla aynı iş, statik bir HTML dosyasıyla görülemez mi?

17-037. Statik HTML raporu (örn. quantstats'ın kendi çıktısı veya markdown'dan dönüştürülmüş) Streamlit'in yerini tamamen alabilir mi? Streamlit'in yapabilip HTML'in yapamadığı tek şey nedir?

17-038. Streamlit sürümü sık değişir. Sürüm sabitleme (pyproject.toml, kilit dosyası) yapılacak mı? Şu an `pyproject.toml` yalnız pytest ayarı içeriyor; bağımlılıklar nerede tanımlı?

17-039. Streamlit ekranının testi nasıl yapılacak? `streamlit.testing.v1.AppTest` mi, elle bakış mı, hiç test yok mu?

17-040. Ekran Windows'ta Türkçe karakterli kullanıcı yolu (örn. Masaüstü) veya boşluklu yol altında çalışırsa dosya okuma bozulur mu? Yollar nerede tanımlı?

17-041. Kart CSV'sinin sütunları nelerdir ve sırası nedir? §6.4 hisse, aile, giriş bölgesi, stop, hedef, pozisyon değeri, kanıt satırı sayıyor; bunlar ayrı sütun mu, tek metin mi?

17-042. CSV şeması sürümlü mü? Sütun eklenir ya da yeniden adlandırılırsa eski günlerin dosyaları ve bunları okuyan kod nasıl etkilenir?

17-043. Kart CSV'si Excel'de açılacaksa ayırıcı ne olacak: virgül mü noktalı virgül mü? Türkiye bölgesel ayarında Excel virgülü ondalık ayırıcı sayar ve virgüllü CSV'yi tek sütuna yığar.

17-044. Ondalık ayırıcı CSV içinde nokta mı virgül mü olacak? Makine okuması (ekran) ve Excel okuması aynı dosyayla nasıl ikisini birden karşılayacak?

17-045. UTF-8 BOM eklenecek mi? BOM olmadan Excel Türkçe karakterleri (ş, ğ, İ) bozar; BOM varsa pandas ile geri okurken ilk sütun adı kirlenebilir.

17-046. Hisse kodu (örn. "ASELS") ve tarih alanları Excel'de otomatik biçimlendirilir (tarih dönüşümü, bilimsel gösterim). Tarih biçimi ISO (2026-10-05) olursa Excel Türkçe'de bunu doğru yorumlar mı?

17-047. CSV kart dosyası Levent tarafından Excel'de açılıp kaydedilirse biçim bozulur (noktalı virgül, kodlama). Sistem bunu fark eden bir kontrol yapacak mı?

17-048. Excel'de açık duran dosya Windows'ta kilitlenir. Sistem 19:30 koşusunda aynı CSV'yi yazmaya çalışırsa ne olur (PermissionError)? Koşu başarısız sayılır mı?

17-049. Günlük kart CSV'si her gün yeni dosya mı (`kartlar-20261005.csv`), yoksa tek dosya mı? Tek dosyada geçmiş günler ne olur?

17-050. Kart CSV'si boş olabilir (hiçbir aile Canlı değil). Boş dosya mı yazılacak, hiç dosya yazılmayacak mı, yoksa "kart yok" nedeni yazan bir satır mı olacak?

17-051. Kart üretilmeyen günlerde (§5.1 son madde, §6.1 tazelik sorunu) Levent bunu nasıl anlayacak? Eksik dosya ile "sinyal yok" ayırt edilebilir mi?

17-052. Pozisyon değeri "sermayenin yüzdesi ve 1.000.000 TL için adet" (§6.4). Levent'in gerçek sermayesi 1.000.000 TL değil. Kart başka sermaye için nasıl yeniden hesaplanacak, ve bu hesabı Levent mi yapacak?

17-053. Kartta adet tam sayıya yuvarlanıyor mu? BIST'te lot 1 hisse; yuvarlama %1 risk kuralını kaç puan bozuyor ve bu rapora yazılıyor mu?

17-054. Kartta "giriş bölgesi" yazıyor, ama işlem ertesi günün AOF fiyatından yapılıyor (§5.3) ve AOF kart üretildiğinde bilinmiyor. Giriş bölgesi nasıl hesaplanıyor ve ne kadar yanıltıcı olabilir?

17-055. Kartta "AL" ya da buna benzer emir dili kullanılmaması (P1) hangi mekanizmayla garanti ediliyor? Sütun adları ve durum etiketleri sabit bir listeden mi geliyor?

17-056. Kart durum etiketleri AKTİF / TAMAMLANDI / BOZULDU (§2) ile AKTİF / STOP / HEDEF / BOZULDU (§6.5) iki farklı liste. Hangisi geçerli, ve TAMAMLANDI ile HEDEF aynı şey mi?

17-057. Kartın kimliği nedir: hisse+aile+sinyal tarihi mi? Aynı hissede açık pozisyonken gelen sinyal kart üretir mi (§5.3 "yeni işlem açmaz")? Kimlik çakışırsa ne olur?

17-058. Kartın kanıt satırı CSV'ye metin olarak mı gömülür, yoksa ayrı sütunlarda sayı olarak mı? Kanıt satırı sonradan yeniden hesaplanınca eski kartın satırı da değişir mi?

17-059. Kart CSV'si okuma amaçlı bir çıktı mı, yoksa sistemin kendi girdisi de mi? Açık kartlar CSV'den mi okunacak (Levent düzenlerse bozulur) yoksa ayrı bir durum deposundan mı?

17-060. Açık kart durum deposu için ne kullanılacak: CSV, JSON, SQLite, parquet? DuckDB "yok" listesinde (§3); SQLite stdlib olduğu halde neden seçeneklerde anılmıyor?

17-061. Açık kartlar her akşam Adım fonksiyonuyla güncelleniyor (§6.5). Güncelleme yarıda kesilirse (elektrik, uyku) durum deposu yarım yazılmış kalır mı? Atomik yazma var mı?

17-062. Aynı günün koşusu iki kez çalışırsa açık kartlar iki kez mi güncellenir? Güncelleme idempotent mi, ve bu hangi testle doğrulanıyor?

17-063. 19:30 koşusu hiç yapılmayan günler (PC kapalı, hafta sonu, tatil) olursa durum deposu eksik günleri nasıl yakalar? Adım fonksiyonu atlanan günleri geriye dönük işler mi?

17-064. Kâğıt üstü canlı dönem (§5.8) en az 6 ay sürer ve işlem sayısı 30'a ulaşana kadar uzar. Bu dönemin işlem kaydı hangi dosyada tutuluyor ve silinmesi ya da bozulması halinde dönem sıfırlanır mı?

17-065. Açık kart durumu ile kâğıt üstü canlı işlem günlüğü aynı depo mu, ayrı mı? İkisi ayrılırsa tutarsız olabilir; birleşirse silme riski artar.

17-066. Deneme günlüğü (§5.11) ve kural kaydı (§5.8) bu çıktı katmanının parçası mı, yoksa başka bir dalın mı? Rapor bunları nereden okuyor ve biçimi kim tanımlıyor?

17-067. Durum deposunun yedeği var mı? Tek kişilik Windows PC'de disk bozulursa kâğıt üstü dönem ve deneme günlüğü kaybolur; sorumlu kim?

17-068. Çıktılar (rapor, CSV, parquet, durum) hangi klasörlerde tutulacak? Şu an `rapor/` içinde markdown, parquet ve sorgu notu karışık duruyor; klasör yapısı belirlendi mi?

17-069. Çıktı dosyaları git içinde mi, dışında mı? Üretilen rapor ve parquet dosyalarının sürüm kontrolüne alınması hem şişirir hem de "kanıt" dosyalarının sonradan değiştirilmesini kolaylaştırır.

17-070. Eski raporlar ve CSV'ler ne zaman silinir ya da arşivlenir? Yıllar içinde günlük dosyalar birikince Levent klasörde ne arayacak?

17-071. Levent bir önceki günün raporunu veya kartını nasıl bulacak? Bir dizin ya da "son" bağlantısı (örn. `son.md`) var mı?

17-072. Dosya adlarında tarih biçimi `YYYYMMDD` (şimdiki kod). Windows Gezgini'nde sıralama için yeterli mi ve Türkçe kullanıcıya okunur mu?

17-073. Parquet çıktısı (`islemler-*.parquet`) Levent tarafından açılabilir değil. Bu dosya kullanıcı çıktısı mı, ara ürün mü? İkincisi ise `rapor/` klasöründe ne işi var?

17-074. İşlem listesi Levent'in denetleyebileceği bir biçimde (Excel) sunulacak mı? "Nerede yanıldığımı anlarım" (§1) hedefi bunu gerektirmiyor mu?

17-075. "Nerede yanıldığımı anlarım" hedefi için tek tek işlemlerin (giriş, çıkış, neden çıktı: stop/hedef/bozulma) görülebildiği bir çıktı tasarlandı mı?

17-076. Rapor içinde "stop önce" kötümser varsayımın etkisi (§5.3) ve karantinaya alınan hisse-dönemler yazılacak. Bu bölümler raporun neresinde, ve hiç karantina yoksa bölüm gizlenir mi?

17-077. Veri kalitesi sorunları (borsapy farkları, karantina, bulunamayan kapanmış semboller) kullanıcıya ayrı bir "uyarılar" bölümünde mi, yoksa dağınık mı gösterilecek? Levent bunları nasıl ciddiye alacak?

17-078. Rapor, mutlak getirilerin "üst sınır" olduğunu (§5.2) hangi biçimde gösterecek? Mutlak getiri sütunu hiç gösterilmezse Levent'in ilk sorusu "ne kadar kazanırdım" cevapsız kalmaz mı?

17-079. Kabul ölçütünün altı maddesi (§5.12) raporda tek bir geçti/kaldı satırına mı indirgenecek? Dördüncü ölçüt gibi kısmi sonuçlar kullanıcıya nasıl açıklanacak?

17-080. Masraf %0,1 / %0,3 / %0,5 senaryoları (§5.4) raporda tablo mu, ayrı rapor mu? Senaryolar çoğalınca rapor kaç sayfa olur ve Levent kaçını okur?

17-081. Yıllık ileri yürüme sonuçları (§5.8) 11 yıl × aile × masraf = çok sayıda satır. Bunun özeti ve ayrıntısı hangi katmanda, ve ayrıntı ekranda mı raporda mı?

17-082. Parametre sağlamlığı (§5.10) için "pozitif hücre oranı" tek sayı. Kullanıcı "hangi hücreler negatifti" sorusunu nasıl cevaplayacak: ısı haritası, tablo, hiçbiri?

17-083. Piyasa durumu etiketine göre ayrı sonuç tablosu (§4) raporda yer alıyor. Etiketin tanımı Levent için anlamlı mı (yükseliş/yatay/düşüş gibi) yoksa teknik kod mu?

17-084. Rapor ve ekranda sayı biçimi: yüzde için virgül (%0,2) kullanılıyor, ama kod `f"{x:.2%}"` nokta üretir. Yerelleştirme için `locale`, Babel ya da elle değiştirme hangisi ve Windows'ta locale ayarı güvenilir mi?

17-085. Para tutarı biçimi: 1.000.000 TL mi 1,000,000 TL mi? Binlik ayırıcı rapor, CSV ve ekranda tutarlı olacak mı?

17-086. Tarih biçimi raporda ve ekranda 05.10.2026 mı, 2026-10-05 mi? CSV'de ISO, raporda Türkçe olursa aynı veri iki biçimde görünür; hangisi tek gerçek kaynak?

17-087. Rapor "Tansu'dan esinlenen yorumumuz" uyarısını (P5) her çıktıda mı taşıyacak? Kart CSV'sinde bu uyarı nerede durur: sütun, ilk satır, ayrı dosya?

17-088. Sistem hata verirse (veri çekilemedi, quantstats çöktü, disk dolu) Levent ne görecek? Hata dosyaya mı, ekrana mı, hiçbir yere mi yazılır ve Türkçe mi?

17-089. 19:30 koşusu başarısız olursa Levent bunu nasıl öğrenecek? Telegram "yok" listesinde (§3); e-posta, Windows bildirimi ya da bir durum dosyası var mı?

17-090. 19:30 koşusu nasıl tetiklenecek: Windows Görev Zamanlayıcı mı, elle mi? PC uykudaysa görev kaçırılır; "kaçırılan koşuyu çalıştır" ayarı kimde ve belgede mi?

17-091. Rapor üretimi (uzun: 1.000 rastgele tekrar) ile günlük kart üretimi (kısa) aynı komutta mı çalışacak? Levent hangi komutu, hangi sıklıkla çalıştıracak ve komutlar kaç tane?

17-092. Rapor modülü (§4) hesap sonuçlarını girdi olarak alıyor. Sonuçların bir veri sınıfı/şeması (pydantic, dataclass, dict) tanımlı mı, yoksa rapor DataFrame'lerin sütun adlarına mı bağımlı?

17-093. Çıktı şeması testi nasıl yapılacak: örnek bir sonuçtan rapor ve CSV üretip beklenen dosyayla (golden file) karşılaştırma mı, yalnız sütun adı kontrolü mü? Test-audit ilkesine göre bu gerçekten değer katıyor mu?

17-094. Önceki rapor (`rapor/kanit-20261005.md`) "kanıt değildir" (§ başı) ama klasörde duruyor. Eski ve geçersiz raporlar yeni sistemde nasıl işaretlenir ya da silinir ki Levent yanlışlıkla okumasın?

17-095. Rapor, farklı kod hash'iyle üretilmiş iki koşunun sonuçlarını yan yana karşılaştırabilecek mi? Levent "dünkü rapordan ne değişti" sorusunu nasıl yanıtlayacak?

17-096. Rapor yalnız son koşuyu mu gösterir, yoksa deneme günlüğündeki bütün denemeleri (Holm düzeltmesi için) mi listeler? Deneme sayısı arttıkça Levent'in okuyacağı sayfa sayısı nasıl sınırlanıyor?

17-097. Rapor ve ekran Levent'in hiçbir yardım almadan anlayabileceği düzeyde mi yazılacak? Bunu ölçecek bir sınama (örn. Levent'e raporu okutup üç soru sorma) tasarlandı mı?

17-098. Sözlükteki terimler (Fazla getiri, Kanıt, Ayrılmış dönem) raporda ilk geçtiği yerde mi açıklanıyor, yoksa rapor GLOSSARY'ye mi bağlantı veriyor? Markdown dosyaları arası bağlantı Windows'ta tıklanabilir olur mu?

17-099. Kullanıcı arayüzü olarak üç ayrı çıktı (markdown rapor, CSV, Streamlit) tek bir "ne yapmalıyım" akışında nasıl birleşiyor? Levent akşam hangi sırayla hangisini açacak ve bu sıra belgede yazılı mı?

17-100. Çıktı katmanı için "en az altyapı" ölçütüne göre en küçük çalışan sürüm nedir: yalnız markdown + CSV mi? Streamlit, quantstats, plotly ve durum deposundan her biri çıkarılırsa Levent'in §1'deki ihtiyacından tam olarak hangisi karşılanmaz hale gelir?
