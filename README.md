# TANSU

TANSU, BIST için günlük sinyal ve geçmiş sınama sistemidir. Tansu'nun kaynaklarından
esinlenen kuralları, para koymadan önce sınar. Sistem emir vermez; hangi kuralın
sağlandığını gösterir. Kararı ve parayı Levent yönetir.

## Yeni olanlar

Son sürüm: v0.1

[Değişiklik günlüğü](CHANGELOG.md)

- GitHub deposunun adı tansu oldu; eski adres yeni adrese yönleniyor.
- Değişiklik başlıkları kapattıkları işin numarasıyla başlıyor; otomatik kabul denetimi bu eşleşmeyi kontrol ediyor.
- Açık işler, çalışma sırasına göre numaralanmış ve sağlayacakları sonuçla adlandırılmış sürüm hedeflerine bağlandı.
- GitHub ana sayfasından işlere, hedeflere, değişikliklere, yayımlanan sürüme ve kontrol sonuçlarına ulaşılabiliyor.
- Bilgisayarda yalnız değişen işle ilgili testler çalışıyor. Tüm testler GitHub'da çalışıyor.

## GitHub'da ilerleme

- [Issues](../../issues) ve [milestone'lar](../../milestones): işler ve hedef sürümler.
- [Açık pull request'ler](../../pulls): süren değişiklikler.
- [Birleşen pull request'ler](../../pulls?q=is%3Apr+is%3Amerged): master'a giren işler.
- [Releases — v0.1](../../releases/tag/v0.1): yayımlanan sürüm.
- Actions: [ci](../../actions/workflows/ci.yml) testleri, biçimi ve lint'i;
  [dod](../../actions/workflows/dod.yml) PR gövdesini denetler.

Büyük iş bir issue ve PR ile; Levent'in sohbette istediği küçük değişiklik, yeşil CI koşusuyla doğrudan master'a girer.

## Ana belgeler

- [AGENTS.md](AGENTS.md): proje girişi ve çalışma kuralları.
- [Tasarım](docs/TASARIM.md): davranış, kararlar ve uygulama sırası (§7).
- [İş kuralları](docs/agents/): görev, kod, git ve issue tracker kuralları.
