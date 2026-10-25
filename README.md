# TANSU

TANSU, BIST için günlük sinyal ve geçmiş sınama sistemidir. Tansu'nun kaynaklarından
esinlenen kuralları, para koymadan önce sınar. Sistem emir vermez; hangi kuralın
sağlandığını gösterir. Kararı ve parayı Levent yönetir.

## GitHub'da ilerleme

Issue, yapılacak işin kaydıdır. PR, değişikliklerin ana projeye girmeden önce kontrol edildiği pakettir.

- [Issues](../../issues) ve [milestone'lar](../../milestones): işler ve hedef sürümler.
- [Açık pull request'ler](../../pulls): süren değişiklikler.
- [Birleşen pull request'ler](../../pulls?q=is%3Apr+is%3Amerged): main dalına giren işler.
- [Releases — v0.1](../../releases/tag/v0.1): yayımlanan sürüm.
- Actions: [ci](../../actions/workflows/ci.yml) testleri, biçimi ve lint'i;
  [dod](../../actions/workflows/dod.yml) PR gövdesini denetler.

Ne zaman issue açılacağı ve küçük belge düzeltmelerinin hangi PR yolunu kullanacağı [issue ve PR kuralında](docs/agents/issue-tracker.md#issue-and-pr-rule) yazılıdır.

## Ana belgeler

- [AGENTS.md](AGENTS.md): Claude ve Codex için ortak proje girişi ve çalışma kuralları.
- [CLAUDE.md](CLAUDE.md): ortak yönergeleri içeri alan Claude girişi.
- [Tasarım](docs/TASARIM.md): davranış, kararlar ve uygulama sırası (§7).
- [İş akışı](docs/agents/is-kurallari.md): kapsam, ortak adımlar, inceleme ve teslim.
- [Kod ve test kuralları](CODING_STANDARDS.md), [bitti ölçütleri](DEFINITION_OF_DONE.md).
- [İş takibi](docs/agents/issue-tracker.md): issue biçimi, durumlar ve etiketler.
- [Kural dizini](docs/KURALLAR.md): aile tanımlarına ve Tansu kaynaklarına giriş.
- [Değişiklik günlüğü](CHANGELOG.md): önemli değişiklikler.
