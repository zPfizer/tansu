# Git geçmişi: eski ve yeni SHA eşlemesi (29.10.2026)

`yeniden-kurulus` geçmişi 29.10.2026'da yeniden yazıldı. Karar ve gerekçe: `kanit/acik-sorular.md` "Verilen kararlar", Git geçmişi maddesi.
Yalnız `tansu/gostergeler.py` dokuz commit'te değişti; son ağaç aynı kaldı (`4b24876`). Aşağıdaki 46 commit yeni SHA aldı; e1bdb7d'den önceki commit'ler ve `main` değişmedi.

Kanıt ve ayar dosyalarındaki eski SHA'lar eski geçmişi gösterir; yeni karşılığı bu tablodadır. Örnekler:

- `stratejiler/ayarlar/gartley.json` ve `ortalama-kesisim.json` içindeki `kod_surumu` `96b5107` = yeni `b33040f`.
- `kanit/faz5.md` içindeki dondurulmuş Gartley kodu `1bd7b15` = yeni `2fcddfb`; veri yolu `96b5107` = yeni `b33040f`; PR 208 `186fe6f` = yeni `81b19a2`.
- `kanit/faz4.md` içindeki `84df495` = yeni `35bc68b`; `kanit/faz5.md` içindeki `f7c022e` = yeni `71b42a8`, `d91f82d` = yeni `597ae59`.

Ağaç farkı sütunu, yeniden yazmanın değiştirdiği dosyayı gösterir; `-` ağacın aynı kaldığını gösterir.

| Eski | Yeni | Ağaç farkı | Konu |
|---|---|---|---|
| `e1bdb7d2fd8a94ae3215ed0068af4ba5badef93b` | `338b7dbfee0d584f47cace8d8ecbc5b13a447c8d` | `tansu/gostergeler.py` | Göstergeler: doğrusal ağırlıklı ortalama (wma) |
| `decb3184abc2575ae11e9d71e88f43cd05f5ade0` | `351e39f8c78859f8c707dc382884800c23e1faca` | `tansu/gostergeler.py` | Strateji: ortalama-kesisim (SPEC 11 madde 15, sınıf b) |
| `6a124378b3fcebe38570e46af780cc93d184e64c` | `061931f705d677708c3c502fc022f6e9f986adeb` | `tansu/gostergeler.py` | durum.csv: ortalama-kesisim taslak satırı |
| `07e8f6892e9a7f1b4f13fdddf9d868bbad86823a` | `7b3b43623578d2a2ba528a7b6f1a2aa4b6cdc73d` | `tansu/gostergeler.py` | Sınama ve rapor: ölçü birimi (R ya da %) ve sınıf b ileri getiri tablosu |
| `02c486b817759ff41ff6d1a1a29294a5ec48b8e7` | `a307e1aae4ed0bbe559d61d57c233c24f769d525` | `tansu/gostergeler.py` | İnceleme: fiyatsız satır kesişimi bölmez; yorum temizliği |
| `e5e6cfac4cbd960c567c8ac11e275c75ad6e1773` | `99653c3e4e4fb580530f5708d6e9aedcb79f17b8` | `tansu/gostergeler.py` | Faz 4a kanıtı: ortalama-kesisim sınaması |
| `202c3ff936d165a4d3165ff636a527cbf6dcfec3` | `2cffca7a8f739584ac2d5427d5a7ab9fb1737d6c` | - | İnceleme: MFE/MAE yalnız tam 10 günlük pencerede; wma belgesinde kaynak alıntısı yok |
| `dce474d26f1682a2901f8690e4bf47e5d91cfb15` | `68ec02e15642b4e097c31716a02014f59fe32ef2` | - | Faz 4a: ortalama-kesisim, piyasa girişi ve sınıf b ölçümü (#197) |
| `28fff53f04a0ed16d21a331aa548051135562372` | `f49ee89c2cb3b95209867c93912e6cd9b9b5045f` | `tansu/gostergeler.py` | Strateji: kaynak_tarihleri (SPEC 5.6 açıklama satırı) |
| `425d8ab7e944e5311c0e738b666ae1c18a528aa9` | `96320984b49fd013fc5584c947e1f3d5ab233361` | `tansu/gostergeler.py` | Sınama: pencere, içeride kapanma, sağlam seçim ve 2026 kesimi testleri |
| `299d86380cfc61111eb97f3001676b7c547615b6` | `9ba0de51ee868d55ba1425636b4ff8e503586550` | `tansu/gostergeler.py` | Ayar ve ileri yürüme: ızgara, sağlam seçim, saklı dönem, tek sina/ayarla akışı (SPEC 5.7) |
| `525060aabcc667fc47021f74e2c8884f35b3c4e3` | `575f815cdaadd6af085fb4523ad8236d6f8e4b92` | - | Merge remote-tracking branch 'origin/yeniden-kurulus' into faz-4b-ayar |
| `d9b2a9074dce67ca81c9a3570aaf165b63826af8` | `4feccb73649a78c85d47563e17b65168e6dd075f` | - | Saklı dönem: veri ayın son iş gününe ulaştıysa ay tamdır |
| `d6a90bfa71bacc384244ac0f678cec6ac26b6058` | `b36e1b454f627bf7b2a71661e8179eb9231497a7` | - | Yorum temizliği (ayar, sınama, rapor) |
| `e0cf2d58fa05183921694602481e6a36766e9366` | `3490be3cd62eb56e0f895c409838f592663949e3` | - | islem: tek kurulum yürütücüsü (oyna) ve tek R hesabı (sonuc) |
| `02ee69a4d2c9b58f311f79c8f5ba74e40e14748a` | `6c218ebade793d7281279579ccb753f37a4081e1` | - | islem: rastgele giriş için tek kurulum girişi (rastgele) |
| `0aa674aa2dc3fa635ed34623a411f628738e139a` | `1102350535294123870175ee050f62177788d093` | - | montecarlo: bootstrap, sıra karıştırma ve düşüş (SPEC 5.8 madde 1-2) |
| `84df495f91a5c107d260598cbb2ff3689d27c549` | `35bc68bce8bbd8df52f6488e88e5cbb2fb70ae68` | - | İnceleme: gartley pivot tek eksen; json ızgaradan önce ve rapordan sonra; saklı dönem yoksa yazılır |
| `216a0ef43b5e229fdeb76b51d2a34a3e5ecb1070` | `29c3a698f5b67edcf6e9ae241e41787d077004d3` | - | Faz 4b kanıtı: iki stratejinin ayarı, ileri yürüme ve saklı dönem |
| `71717f60daf363d3a583eb2bedc3151e015ab867` | `17d5405d26dd1ab566b550913542a31e382f0c8d` | - | Merge remote-tracking branch 'origin/faz-4b-ayar' into faz-5-montecarlo |
| `f7c022ed988edaca94f283d60758e72278f43bad` | `71b42a8e0e5199cde40a5fcc4baa5f0e61e4be33` | - | Faz 4b: ayar, ileri yürüme ve saklı dönem (#198) |
| `7f640596b15e6aea95f824b987b22018e7f241f3` | `c2d47cbe21aeb885560bfc8fc5e454c14a014c85` | - | Tek düşüş tanımı: sinama.dusus dizi de alır, montecarlo onu kullanır |
| `14ebb9ec10ebb79707a37b5e6065b39336d18ed0` | `f77a4a30215f8479eee83cfa88f7ab00728cde9e` | - | montecarlo: hesapla, üç tablo ve rastgele giriş kıyası (SPEC 5.8 madde 3) |
| `390e819d9f394ac2e9698a91ac1d7ab9d39b4a08` | `3024b582323032b4fc28469364f831d251235ab2` | - | Rapor: Monte Carlo bölümü ve onay bayrakları (SPEC 5.8-5.10); sina ve ayarla hesaplar |
| `ed0297bd846bd039ecf20da4132d426bb2acb3c4` | `714cdc11f469fb34821a98ee8b5259826e53063b` | - | Merge remote-tracking branch 'origin/yeniden-kurulus' into faz-5-montecarlo |
| `d91f82d139a025a785bb286f056b13118d59bc2e` | `597ae595ff3dda2713712d6c51a063c95e5f471f` | - | Monte Carlo inceleme düzeltmeleri: boş havuz, sıfır ATR şablonu, NaN düşüş |
| `58a15d925811e180d991f50a8a1d5828fbfdd295` | `6f58c88145d7378271d47cb386ac87efcdf2a337` | - | Faz 5 kanıtı ve gerçek veri çıktıları: Monte Carlo ve bayraklar |
| `a706428371069e03f7a67d20b75630377da97886` | `cdabbfd705fd5f9b31ada8f781109453f88bceff` | - | Faz 5 kanıtı: yanlılık sınamasının sınırını yaz |
| `ec5c4bb09cb0f950f054d1116640bd2988aceb53` | `6569e3c6062ab7190d17184026d41afda9b269ab` | - | Faz 5: Monte Carlo, rastgele giriş kıyası ve onay bayrakları (#199) |
| `4a7a6a3fefb98083b8662c5b895422598acfbdd2` | `5cb89671820703112a3646100205652ce9e7e42d` | - | Alt limit kilidinde dokunulan stop ilk kilitsiz güne kalır (SPEC 5.4 adım 1) |
| `185fbafe0251a82dbd519c36e72964d03b934637` | `02a157e1caa20862c484e5cbf201ad902754b6b3` | - | Stop düzeltmesinin kanıtı: gerçek veri sayıları değişmedi |
| `b8bd97c6f0d98f87b4e99b88dfd8e21dae5378ee` | `c327c7875d36d5964176f1ec72a594560f7bb8dd` | - | Temizlik: açık sorulardaki Tansu alıntısı çıktı, strateji alt paketi dağıtımda |
| `f4cd8326805eed04f620d7b887b8b29c51d8a9a1` | `bd8bd6d6deae7a6866f0ee3f314fb87c616afb79` | - | Açık sorular: Levent'in 28.10 cevabından sonraki kararlar |
| `666cb3480c3dab0fdea54acb9f14f22ee81f60b7` | `d046e70a0984c0ad15f5016f7eb5ddb85af7b3c0` | - | Stop düzeltmesi incelemesi: çok günlü kilit ve bekleyen çıkış testleri, kanıt metni |
| `620601276706409f69a130608fdb86cd37afcf72` | `551feda66d40fefe4d774ffe871eec57255e2fc0` | - | Temizlik: açık sorulardaki Tansu alıntısı ve strateji alt paketi (#201) |
| `ff42114b443442dffa19e5558433be8374af68c8` | `644779c449da8ca687369ac80eb1cd46638f0984` | - | Motor: alt limit kilidinde dokunulan stop bekleyen çıkış olur (#200) |
| `a287e84b65c6430dfaed7825f898559e362e8294` | `b99aef79affec27016ac340a7e1bd9b7017cdd7e` | - | Gartley: R/R kapısı Tansu'nun yazılı kuralıyla (Ek B #13) (#202) |
| `b336f643e7e12f452ad9b4a7f91df7905e068ffc` | `1e6e439babf893d15ad7ec06469398798123768e` | - | Belge: Gartley soruları Tansu'nun metinleriyle cevaplandı (#203) |
| `8b6461b90c3379c97fb633e600fed8cb3505604d` | `2e2aca72ed81c41a3ce929fb5fa199ce303303b9` | - | Evren: bütün stratejiler bütün BIST'te sınanır (#205) |
| `b97eca05c126722bbc927f94478eb617af128f0d` | `f1c11eb3d49751da646f931bfcc0a00a43102b9e` | - | Veri: günlük güncelleme yalnız yeni günleri indirir (#206) |
| `1bd7b151ebc60883b405c985ae371311702cc2d6` | `2fcddfbce76ff95965ac2d27361e70df4b7f8608` | - | Gartley: bütün BIST ölçümü, neden analizi, kapı 1,40 ve n günlük pivotlar (#204) |
| `96b51071c4e49beea02071c8422d2bc8d97c8127` | `b33040f7c2bbc092e373c72e2b8509005fe4da21` | - | Veri yolu: kopan bağlantı, bozuk gün ve eksik gün sonrası ATR (#207) |
| `f51b4bb741c7ab20370a2151e8cd3cdabb4ddb7e` | `83ec77dcbb88d68a0b3a16e878d86da0b1c1ec50` | - | Ayar: iki strateji bütün BIST'te yeniden ayarlandı (2021-2025) (#209) |
| `186fe6f7d260054eb43590415a3dea055a2cfcea` | `81b19a21d1f2aaa9e5aa0ac209ceea84289e2aee` | - | Kanıt: Gartley yeniden ölçümü, ürün komutu ve sağlamlık denetimi (şart 2 sınırda geçmez) (#208) |
| `2f50da102e842282825f349eb04f699da887a8d2` | `56216071a27dfdfae853c5016e6a8cae359c879a` | - | Sahip kararı 13: Gartley R/R kapısı hedef1'e göre 1,40 (#210) |
| `70ce0ca16c108f0039df67c833e3a25dcad02f54` | `236718cc284d29d22be389c46c89b8e8ee53c4b1` | - | Sahip kararı 6: çift evreni bütün BIST (#211) |
