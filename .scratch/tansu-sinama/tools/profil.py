"""Profil: `profil.py <aile|hepsi> <hisse|0> <isci,...>`; günlük anlık görüntü 20261014-1930. Kayıt yazmaz (yalnız calistir)."""

import sys
import threading
import time

import psutil

from tansu import tansusinama as ts
from tansu import veri


def olc(ana, cpu, tepe, dur):
    psutil.cpu_percent()
    while not dur.wait(0.5):
        cpu.append(psutil.cpu_percent())
        try:
            rss = [c.memory_info().rss for c in ana.children(recursive=True)]
        except psutil.NoSuchProcess:
            continue  # çocuk süreç okuma sırasında bitti; bir sonraki turda okunur
        if rss:
            tepe[0] = max(tepe[0], max(rss) / 2**30)
            tepe[1] = max(tepe[1], len(rss))


def main():
    aile, hisse, iscilar = sys.argv[1], int(sys.argv[2]) or None, sys.argv[3].split(",")
    aileler = ts.AILELER if aile == "hepsi" else (aile,)
    anlik = veri.oku("20261014-1930", r"C:\Users\levent\Desktop\TANSU\veri\gunluk")
    sektor, _ = ts.sektor_oku(r"C:\Users\levent\Desktop\TANSU\veri")
    ana = psutil.Process()
    print(f"ana süreç bellek (anlık okunduktan sonra): {ana.memory_info().rss / 2**30:.2f} GB")
    print("| aile | hisse | iş | işçi | süre sn | sn/iş | ort. CPU % | işçi başı tepe bellek GB | süreç |")
    for isci in map(int, iscilar):
        cpu, tepe, dur = [], [0.0, 0], threading.Event()
        th = threading.Thread(target=olc, args=(ana, cpu, tepe, dur))
        th.start()
        t0 = time.perf_counter()
        s = ts.calistir(anlik, sektor, aileler, isci=isci, hisse=hisse, ilerleme=lambda x: None)
        sure = time.perf_counter() - t0
        dur.set()
        th.join()
        n = sum(f["ozet"]["toplam"] for f in s["aileler"].values())
        ort = sum(cpu) / len(cpu) if cpu else float("nan")
        print(
            f"| {aile} | {hisse or 'hepsi'} | {n} | {isci} | {sure:.1f} | {sure / max(n, 1):.3f} | "
            f"{ort:.0f} | {tepe[0]:.2f} | {tepe[1]} |"
        )


if __name__ == "__main__":
    main()
