import os
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from pathlib import Path


@contextmanager
def atomik(yol: Path) -> Iterator[Path]:
    """Yarım dosya bırakmaz: geçici yolu verir; blok hatasız biterse `yol`un yerine koyar, hata olursa geçiciyi siler.

    Geçici ad her çağrıda tektir: aynı dosyayı yazan iki koşu birbirinin geçicisini ezmez."""
    tutamak, ad = tempfile.mkstemp(dir=yol.parent, prefix=yol.name + ".", suffix=".tmp")
    os.close(tutamak)
    gecici = Path(ad)
    try:
        yield gecici
        os.replace(gecici, yol)
    except BaseException:
        with suppress(OSError):
            gecici.unlink(missing_ok=True)
        raise
