import pytest

from tansu.__main__ import main


def test_yardim_alti_komutu_listeler(capsys):
    with pytest.raises(SystemExit) as cikis:
        main(["--help"])
    assert cikis.value.code == 0
    yardim = capsys.readouterr().out
    for komut in ("veri", "sina", "ayarla", "onayla", "tara", "durum"):
        assert komut in yardim
