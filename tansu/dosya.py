import os
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from pathlib import Path


@contextmanager
def atomik(yol: Path) -> Iterator[Path]:
    """Yarım dosya bırakmaz: geçici yolu verir; blok hatasız biterse `yol`un yerine koyar, hata olursa geçiciyi siler."""
    gecici = yol.with_name(yol.name + ".tmp")
    try:
        yield gecici
        os.replace(gecici, yol)
    except BaseException:
        with suppress(OSError):
            gecici.unlink(missing_ok=True)
        raise
