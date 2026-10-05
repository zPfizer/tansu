# Sorular 20: Sürüm, belge, bakım

20-001. Depoda `git remote -v` boş; yani tek kopya Levent'in masaüstündeki klasör. Disk bozulursa, fidye yazılımı gelirse ya da klasör yanlışlıkla silinirse hangi kopyadan geri dönülecek?

20-002. Yedek, git'in kendisi dışında nerede ve ne sıklıkla tutulacak? Levent bunu elle mi yapacak, yoksa kimsenin hatırlamasına gerek kalmadan mı çalışacak?

20-003. `.gitignore` tüm `veri/` klasörünü dışarıda bırakıyor. Ham fiyat anlık görüntüleri (TASARIM §4, B2) git'te değilse, "her koşu hangi anlık görüntüyü kullandı" kaydı 6 ay sonra neyi gösterecek?

20-004. Anlık görüntüler "değişmez" olarak tasarlanıyor ama git dışında duruyor. Bir dosyanın sessizce bozulmadığı ya da yeniden indirilip üzerine yazılmadığı nasıl anlaşılacak?

20-005. `rapor/` klasörü `.gitignore`'da yok ve içinde `islemler-20261005.parquet` var. Hangi raporlar git'e girecek, hangileri girmeyecek, ve bu ayrımı kim yapacak?

20-006. TASARIM §5.8 kural kaydının "kodun parmak izini (hash)" içermesini istiyor. Bu hash git commit'i mi, dosya hash'i mi, yoksa başka bir şey mi; ve commit edilmemiş bir değişiklikle koşu yapılırsa ne olacak?

20-007. Deneme günlüğü (§5.11) "kod hash" yazıyor. Git geçmişi `rebase`, `amend` ya da depo yeniden oluşturma ile değişirse eski günlük kayıtlarının hash'leri hâlâ doğrulanabilir mi?

20-008. Tek kişilik depoda dal politikası ne olacak? Her iş için dal mı, doğrudan ana dalda çalışma mı; ve bu seçimi Levent mi ajan mı yapacak?

20-009. Ana dalın adı ne? Mevcut depoda `git branch` çıktısı hiçbir belgede yazılı değil; ajan yanlış dala commit atarsa Levent bunu nasıl fark edecek?

20-010. Ajan commit atmadan önce Levent'in onayını mı alacak, yoksa kendi başına mı commit edecek? Mevcut AGENTS.md bu konuda tek kelime söylemiyor.

20-011. Commit mesajları şu an Türkçe ve serbest biçimli ("Tasarım taslak 5: ..."). 6 ay sonra "hangi commit sonucu değiştirdi" sorusunu cevaplamak için bir mesaj kuralı gerekiyor mu?

20-012. Kural kaydı (§5.8) "sonraki her değişiklik yeni denemedir" diyor. Biçimlendirme, yeniden adlandırma ve yorum değişikliği gibi davranışı değiştirmeyen commit'ler yeni deneme sayılacak mı?

20-013. Git etiketi (tag) kullanılacak mı? "Kural kaydı bu commit'te dondu" ya da "rapor bu koddan üretildi" bilgisini taşıyacak bir mekanizma var mı?

20-014. Windows'ta satır sonu (CRLF/LF) farkı yüzünden aynı dosyanın hash'i farklı çıkabilir. `.gitattributes` ya da `autocrlf` ayarı olmadan kod hash'i güvenilir mi?

20-015. Parquet ve büyük ikili dosyalar bir gün yanlışlıkla `git add .` ile eklenirse depo şişer. Bunu engelleyen bir önlem (hook, boyut sınırı, ajan kuralı) var mı?

20-016. Git geçmişi zaten ilk sürüm kodunu (Yahoo'lu ön deneme) içeriyor. TASARIM §7 "ön deneme kodu kaldırılır" diyor; kaldırmak dosyayı silmek mi, geçmişten temizlemek mi demek?

20-017. Ön deneme kodunun silinmesinden sonra eski `kanit-20261005.md` raporu repoda kalacak mı? Kalırsa, "rakamları hiçbir kararda kullanılmaz" kuralını bir ajan yanlışlıkla çiğneyebilir mi?

20-018. TASARIM.md bir taslak numarası taşıyor (taslak 5) ama dosya adında sürüm yok. Taslak 6 yazıldığında taslak 5'in tam metnine ulaşmanın tek yolu git geçmişi mi?

20-019. Bir karar değiştiğinde TASARIM.md'yi düzenlemek mi, yoksa `docs/adr/` altına yeni bir ADR yazmak mı gerekiyor? `docs/agents/domain.md` ADR klasörünü anıyor ama klasör henüz yok.

20-020. ADR'ler varsa TASARIM.md ile çelişince hangisi geçerli? "Kod belgeye uyar" kuralındaki "belge" hangisi?

20-021. TASARIM.md içindeki "Sorgu Sn" ve "S2-n" etiketleri, sorgu dosyalarına bağlı. Sorgu dosyaları taşınır ya da yeniden adlandırılırsa bu etiketler ölü referansa dönüşmez mi?

20-022. TASARIM.md şu an 300 satırı aşıyor ve her taslakta büyüyor. Altı ay sonra dönen non-teknik bir sahip bu belgeyi baştan sona okuyabilecek mi, yoksa yalnız özet için ayrı bir sayfa mı gerekecek?

20-023. "Kod belgeye uyar; belge değişmeden davranış değişmez" kuralını denetleyen bir şey var mı? Kodu belgeden ayrıştıran bir değişikliği kim ve nasıl yakalayacak?

20-024. TASARIM.md rakamları (ör. %0,3 masraf, 1.000.000 TL sermaye, 252 gün, 2 ATR) kodda sabit olarak da duracak. Belge ile kod arasında aynı sayı iki yerde yaşıyorsa hangisi tek doğru kaynak?

20-025. Parametre kaydı (§5.10 "ek: parametre kaydı") henüz yok. Bu kayıt belge mi, kod mu, veri dosyası mı olacak; ve kural kaydının hash'i bunu kapsayacak mı?

20-026. GLOSSARY.md'deki terimlerle kod isimleri (ör. `kanit.py`, `nabiz.py`, `aileler.py`) tutarlı olacak mı? Terim değişirse kod, test ve belge birlikte nasıl güncellenecek?

20-027. GLOSSARY.md "Piyasa durumu" diyor, kodda `nabiz.py` var, TASARIM §4 "Nabız kuralı bizimdi" diyor. Eski adların kodda yaşaması ajanları yanlış yönlendirir mi?

20-028. Kod ve belge Türkçe, ama kütüphane API'leri, hata mesajları ve araç çıktıları İngilizce. Değişken ve fonksiyon adları hangi dilde olacak ve bu karma yapı ajanın tutarlılığını nasıl etkiler?

20-029. `.scratch/` klasörü AGENTS.md'de iş takipçisi olarak tanımlı ama depoda yok ve `.gitignore`'da da yok. `.scratch/` git'e girecek mi, girmeyecek mi?

20-030. `.scratch/` içindeki işler git'e girmiyorsa yedeklenmiyor demektir. Giriyorsa, her bilet değişikliği ayrı bir commit mi olacak, yoksa commit geçmişi gürültüyle mi dolacak?

20-031. `issue-tracker.md` her özellik için `spec.md`, `issues/NN-slug.md` ve `map.md` istiyor. Tek kişilik, 3 aileli bir proje için bu yapı gereğinden ağır mı; sade bir `TODO.md` aynı işi görür mü?

20-032. Beş triage etiketinden `needs-info` ve `wontfix` bu projede kim için anlamlı? Raporlayan ile bakımcı aynı kişiyse etiketin faydası ne?

20-033. `ready-for-agent` etiketi "AFK ajan" varsayıyor. Levent'in başında durmadığı bir ajan oturumu bu depoda hangi eylemleri güvenle yapabilir ve hangilerini asla yapmamalı?

20-034. Bilet "Status:" satırı elle güncelleniyor. Ajan unutursa, kapanmış iş açık görünürse ya da tersi olursa bunu kim fark edecek?

20-035. Altı ay sonra Levent dönünce "şu an ne yapılıyordu" sorusunu cevaplayan tek bir dosya var mı? Bu sorunun cevabı `.scratch/` taramak mı olacak?

20-036. Levent teknik değil. Biletleri, ADR'leri, `map.md`'yi okuyup yönetebilir mi; yoksa tüm bu belge katmanı yalnızca ajanlar için mi var ve Levent ona hiç bakmayacak mı?

20-037. AGENTS.md şu an 18 satır ve yalnız belge işaretçileri içeriyor. Ajana "yapma" listesi (veri silme, `git push`, `--force`, bağımlılık ekleme, belge değiştirme) hiçbir yerde yazılı değil; bu eksik bilinçli mi?

20-038. AGENTS.md, ajanın TASARIM.md'yi kendi başına düzenleyip düzenleyemeyeceğini söylemiyor. Bir ajan "kod belgeye uyar" kuralını, belgeyi koda uydurarak mı çözecek?

20-039. Ajanın hangi komutla test çalıştıracağı, hangi Python'u kullanacağı ve `.venv`'in nasıl etkinleştirileceği AGENTS.md'de yok. Yeni bir ajan oturumu bunu her seferinde yeniden mi keşfedecek?

20-040. Windows'ta PowerShell ile Git Bash arasındaki yol ve alıntı farkları ajanların sık hata nedeni. AGENTS.md bu depo için hangi kabuğun kullanılacağını sabitleyecek mi?

20-041. Mevcut tasarım ajanın tek oturumda ne kadar iş yapabileceğini sınırlamıyor. Ajan 40 dosyayı değiştiren bir iş yaparsa, Levent sonucu nasıl gözden geçirecek?

20-042. Teknik olmayan sahip kodu okuyamıyor. Ajanın "bitti" demesini doğrulayan, Levent'in anlayabileceği bir kabul göstergesi (test sayısı, tek bir komut, tek bir ekran) nedir?

20-043. Ajanın yazdığı testler kendi kodunu doğruluyor. Testin yanlış şeyi doğruladığını (kural yerine kodun davranışını sabitlediğini) kim kontrol edecek?

20-044. TASARIM §5.3 "motor sınamaları kod yazılmadan önce" yazılacak diyor. Bu sıra ("önce test, sonra kod") AGENTS.md'de bir kural olarak yazılacak mı, yoksa yalnız belgede mi kalacak?

20-045. Mevcut `pyproject.toml` yalnızca pytest ayarı içeriyor: ad, sürüm, Python sürümü ve bağımlılık listesi yok. Sistemin hangi kütüphanelerle çalıştığı bugün nerede kayıtlı?

20-046. `.venv` içinde Python 3.14 görünüyor. Altı ay sonra Python ya da pandas sürümü değişirse, aynı kodla aynı sonucu alacağımızı gösteren bir kilit dosyası olacak mı?

20-047. Paket yönetimi için `pip`, `uv`, `poetry` ya da başka bir araç mı kullanılacak? Her biri Windows'ta ve non-teknik bir sahip için farklı bir bakım yükü getirir; hangisi seçilecek ve neden?

20-048. Bağımlılıklar (pandas-ta-classic, borsapy, quantstats, statsmodels) küçük ve az bakımlı projeler olabilir. Biri terk edilirse ya da bozulursa kimin, ne zaman fark edeceği belli mi?

20-049. "Güvenilir kütüphane" kriteri nedir? İndirme sayısı, son sürüm tarihi, bakımcı sayısı gibi ölçüt yazılı olmazsa ajan her seferinde farklı bir kütüphane seçmez mi?

20-050. Bir kütüphane sürümü yükseltilirken sonuçların değişmediğini gösteren bir regresyon karşılaştırması olacak mı? Yükseltme sessizce eski raporları tekrarlanamaz hâle getirebilir.

20-051. Linter ve biçimlendirici olarak ruff kullanılacaksa kural kümesi ne olacak? Varsayılan kümeyi mi, geniş bir kümeyi mi seçeceğiz ve kim bu seçimi savunacak?

20-052. Biçimlendirme otomatik çalışacaksa hangi tetikle çalışacak: elle komut, commit öncesi hook ya da ajanın her düzenlemesinden sonra mı? Non-teknik sahip bu aracı hiç çalıştırmayacaksa kim çalıştıracak?

20-053. Pre-commit hook'ları Windows'ta bozulabilir ve sessizce atlanabilir (`--no-verify`). Hook'a güvenmek yerine hangi mekanizma kuralı gerçekten zorunlu kılacak?

20-054. Tip denetimi (mypy ya da pyright) bu projede değer üretir mi? Pandas ağırlıklı kodda tip denetimi çoğunlukla gürültü üretir; bunun bakım maliyeti kimin sırtında?

20-055. Tip denetimi eklenirse hangi katı seviyede çalışacak? Seviye çok gevşekse anlamsız, çok sıkıysa ajan her seferinde `type: ignore` ile susturur; bu sınır nerede?

20-056. Bu araçların (ruff, mypy, pytest, pre-commit) toplamı yeni bir bakım yükü. "Asgari altyapı" ilkesine göre hangisi zorunlu, hangisi isteğe bağlı ve neye göre ayrılacak?

20-057. Test kapsamı için bir sayı hedefi (ör. kapsam yüzdesi) konulacak mı? Sayı hedefi ajanları anlamsız testler yazmaya iter; hedef yoksa nasıl "yeterli" denecek?

20-058. Tek komutla "her şey yolunda mı" sorusunu cevaplayan bir kapı (lint + tip + test) gerekli mi? Varsa komut adı ne, nerede yazılı ve Levent'in bunu çalıştırması mümkün mü?

20-059. CI (GitHub Actions gibi) uzak depo olmadan kullanılamaz. Uzak depo olmadığı için testlerin her commit'te çalıştığı garantisini hangi yerel mekanizma verecek?

20-060. Uzak depo (özel GitHub/GitLab) eklemek yedeği de çözerdi; ama veriler, API anahtarları ve strateji kodu dışarı çıkar. Levent bu iki riskten (kayıp ve sızıntı) hangisini daha önemli sayıyor ve bu açıkça yazılı mı?

20-061. Gizli bilgi (API anahtarı, hesap bilgisi) bu projede şu an yok görünüyor (İş Yatırım anahtarsız). İleride Telegram ya da başka bir servis eklenirse `.env` yönetimi ve `.gitignore` kuralı önceden tanımlı mı?

20-062. Ajanlar kod yazarken dışarıdan paket indirir ve komut çalıştırır. Hangi ağ erişimine izin var; bir ajan kötü niyetli ya da hatalı bir paketi `pip install` ederse bunu fark etmenin yolu nedir?

20-063. Ajan aracı (Claude Code ya da başka) değişirse AGENTS.md ve `docs/agents/*.md` yine çalışır mı? Bu belgeler Matt Pocock skill'lerine mi bağlı, yoksa araçtan bağımsız mı?

20-064. AGENTS.md "Levent'in tek seferlik izniyle" eklenen bir skill bloğu içeriyor (commit `aa6ed79`). Bu izin deseni ne zaman yeniden gerekir ve ajanın kendi başına AGENTS.md'yi değiştirmesi yasak mı?

20-065. `docs/agents/*.md` dosyaları `/wayfinder`, `/domain-modeling`, `/grill-with-docs` gibi harici skill adlarına referans veriyor. Bu skill'ler kaybolur ya da yeniden adlandırılırsa belgeler boşa mı düşer?

20-066. İngilizce şablondan gelen `docs/agents/*.md` dosyaları ile Türkçe TASARIM/AGENTS metni aynı depoda karışık. Bu iki dil ajan davranışında tutarsızlık yaratabilir mi, ve tek bir dile çevrilmeli mi?

20-067. Sorgu dosyaları (`docs/sorgu/sorgu-2.md` ve sonrası) kararların gerekçesini taşıyor. Bunlar kalıcı karar kaydı mı, yoksa tek kullanımlık çalışma kâğıdı mı? Kalıcıysa ADR ile ilişkisi ne?

20-068. Sorgu etiketleri (S2-31, S2-34) TASARIM ve KURALLAR'dan sorgu metnine bağlanıyor. Sorgu-4 çalışmasının 20 ayrı soru dosyası ürettiği düşünülürse, 2.000 soruyu yönetmenin pratik yolu ne?

20-069. Bu soru kümesinin cevapları nereye yazılacak ve nasıl kalıcı karara dönecek? Cevaplar yalnız TASARIM'a işlenirse, "neden böyle" bilgisi 6 ay sonra nereden okunacak?

20-070. Belge sayısı artıyor: TASARIM, KURALLAR, kurallar/A–E, arastirma, sorgu, agents, GLOSSARY. Yeni bir ajanın ya da Levent'in hangi sırayla ve hangi kısmını okuması gerektiğini tek bir yer söylüyor mu?

20-071. `docs/kurallar/A–E` dosyaları 238 notluk beyin havuzuna dayanıyor. Bu havuz git deposunun dışında. Havuz değişirse ya da kaybolursa kural kataloğunun kaynak izi nasıl doğrulanacak?

20-072. `docs/arastirma/veri-kaynaklari.md` canlı servislerin (İş Yatırım uçları, borsapy) davranışını anlatıyor. Bu servisler değiştikçe belge eskiyecek; "son doğrulama tarihi" ve yeniden doğrulama sorumlusu tanımlı mı?

20-073. Veri sağlayıcı bir uç noktayı kapatırsa ya da formatı değiştirirse (TASARIM §8.1 kullanım koşulları bilinmiyor), günlük işleyiş (§6) sessizce mi duracak, yoksa Levent'e açık bir mesaj mı çıkacak?

20-074. Günlük akış 19:30'da çalışacak. Bilgisayar kapalıysa, uykudaysa ya da Windows güncellemesi sırasındaysa, Levent "bugün kart yok" ile "sistem çalışmadı" arasındaki farkı nasıl anlayacak?

20-075. Zamanlanmış görev Windows Görev Zamanlayıcı ile mi kurulacak? Bunun kurulumu, ayarı ve bozulduğunda onarımı belgelenecek mi, ve non-teknik sahip bunu yapabilir mi?

20-076. Altı ay sonra Levent geri döndüğünde veri deposu 6 aylık boşluk içerir. Sistem eksik günleri otomatik doldurur mu, yoksa elle bir "toparlama" komutu mu gerekir; ve bu komut Levent'in anlayacağı bir yerde yazılı mı?

20-077. Altı aylık aranın ardından Levent'in ilk 15 dakikada yapabileceği şey ne olmalı? Bunu tarif eden bir "geri dönüş rehberi" şimdiden yazılı olmalı mı?

20-078. Bus factor bir: tek kişi, o da teknik değil. Levent hastalanır, ilgisini kaybeder ya da ajan aracı değişirse sistemi başka biri ya da yeni bir ajan hangi belgeyle devralabilir?

20-079. Sistem tamamen ajanlarla geliştiriliyorsa, Levent hiçbir kodu okuyamıyorsa, bir ajanın kodda gizli bir hata (ör. sızıntı, ileri bakış) bırakması durumunu kim yakalayacak? Bağımsız denetim ritüeli var mı?

20-080. Önceki turlarda bağımsız eleştirmenler (B1–M12) bulgu üretti. Bu eleştiri süreci bir kez mi yapıldı, yoksa her büyük değişiklikten sonra tekrarlanması zorunlu bir kapı mı?

20-081. Ön deneme kodu (`tansu/*.py`, 425 satır ve 3 test dosyası) "büyük ölçüde değiştirilecek". Hangi parçalar silinecek, hangileri taşınacak? Bu karar bir bilette mi, ADR'de mi yoksa TASARIM'da mı yazılı olacak?

20-082. Testler `pythonpath = ["."]` ile çalışıyor; paket kurulmamış. Modüler yapıya geçerken `src/` düzeni ve `pip install -e .` kullanılacak mı, ve non-teknik sahip için bu ek adım neden değer?

20-083. Modüler yapı TASARIM §4'te 11 modül öneriyor. Her modül ayrı paket, ayrı dosya ya da ayrı klasör mü olacak? Çok fazla küçük dosya ajanın bağlamını ve review yükünü artırmaz mı?

20-084. Modüller arası sınırın ("dışarıya küçük yüz") kodda nasıl korunacağı belli değil. Bir ajan modül içi bir fonksiyonu başka modülden çağırırsa bunu yakalayacak bir kural (import denetimi vb.) olacak mı, yoksa yalnız belge mi?

20-085. Sürümleme: sistem ve kurallar için bir sürüm numarası olacak mı? "v0.3 koşusu" ya da "kural kaydı r2" gibi bir isim olmadan Levent geçmişteki bir sonucu nasıl adlandıracak?

20-086. Değişiklik günlüğü (CHANGELOG) tutulacak mı, yoksa `git log` yeterli mi? Non-teknik sahip `git log` çıktısını okuyabilir mi?

20-087. Bir koşunun sonucu (rapor) sonradan değiştirilirse ya da yeniden üretilirse "ilk rapor" ile "yeni rapor" arasındaki fark nasıl kayıt altına alınacak? Deneme günlüğü bunu yeterince kapsıyor mu?

20-088. Deneme günlüğü (§5.11) Holm düzeltmesinin temelini oluşturuyor. Bu günlük silinir, bozulur ya da yedekten dönülürse p değerlerinin dürüstlüğü kaybolur; günlüğün kendi korunması ve yedeklenmesi nasıl tanımlanacak?

20-089. Deneme günlüğü git'te mi, veri klasöründe mi duracak? Git'teyse her koşu bir commit mi gerektirir; dışındaysa "elle silerek denemeyi gizleme" riski nasıl kapanır?

20-090. Ajanın kural parametrelerini sonuca bakarak değiştirmesini (§5.8 YORUM yasağı) teknik olarak engelleyen bir şey var mı, yoksa tamamen güvene mi dayanıyor? Kural kaydından sonra dosya salt-okunur mu olacak?

20-091. `ruff` ve `pytest` hataları ajan tarafından "düzeltilirken" test beklentisinin kendisi değiştirilebilir. Testin silinmesi ya da zayıflatılması hangi mekanizmayla Levent'in önüne gelecek?

20-092. Her ajan oturumu bağlamı sıfırdan başlıyor. Bir önceki oturumda alınan "neden böyle yaptık" kararı hangi dosyaya yazılırsa ertesi oturum onu bulur? Bunun için bir devir-teslim notu kuralı var mı?

20-093. TASARIM.md'deki "kod belgeye uyar" kuralı, belgede bir hata varsa ajanı hatalı davranışı uygulamaya iter. Belge hatası bulunca ajanın izleyeceği yol (dur, bilet aç, Levent'e sor) yazılı mı?

20-094. Belge-kod uyumunu sağlamak için hangi kontrol otomatik olacak: sabit-parametre tutarlılığı, bozuk bağlantı, terim sözlüğü ihlali? Hiçbiri otomatik değilse uyum yalnız disiplinle mi korunacak?

20-095. Araç maliyeti: ruff, mypy/pyright, pre-commit, uv, CI, ajan abonelikleri. Her birinin yıllık para, öğrenme ve arıza maliyeti Levent için yazılı bir tabloda değerlendirilecek mi, yoksa araçlar tek tek alışkanlıkla mı eklenecek?

20-096. Ajan aboneliği ya da model erişimi bir gün kesilirse sistem tek başına çalışmaya devam edebilir mi? Günlük akış (§6) ajan olmadan çalışmalı mı, ve bu açıkça bir gereksinim mi?

20-097. "Asgari altyapı" ilkesiyle "bakım için yeterince belge/test/araç" ilkesi çatışıyor. Bu çatışmayı çözecek açık bir ölçüt (ör. "şu araç yalnız şu arıza türünü önlüyorsa eklenir") yazılı olacak mı?

20-098. Hangi sorunlar Levent'e sormadan ajan tarafından çözülebilir, hangileri her zaman Levent'in kararı? Bu sınır `ready-for-agent` / `ready-for-human` etiketlerinde somut örneklerle tanımlı mı?

20-099. Sistem bir gün emekli edilirse (ör. hiçbir aile kabul edilmedi ve Levent ilgisini kaybetti), "arşivle ve durdur" için ne gerekir? Zamanlanmış görevi kaldırma ve sonuçları arşivleme adımları yazılı mı?

20-100. Bu projede "bakım bitti, yeni özellik başlayabilir" kararını hangi ölçüt verecek? Bakım yükü sınırı (ör. haftada kaç dakika) Levent için tanımlanmadıysa, altyapı büyümesini durduracak olan nedir?
