"""Gambar peta ekosistem SO dan grafik pemakaian memori untuk laporan I-1."""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

FONT = "DejaVu Sans"
OUT = "results"


def kotak(ax, x, y, w, h, judul, isi, warna, tepi, ukuran=7.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.015,rounding_size=0.05",
                                facecolor=warna, edgecolor=tepi, linewidth=1.2))
    ax.text(x + w / 2, y + h - 0.16, judul, ha="center", va="top", fontsize=8.6,
            fontfamily=FONT, fontweight="bold", color=tepi)
    ax.text(x + w / 2, y + h - 0.44, isi, ha="center", va="top", fontsize=ukuran,
            fontfamily=FONT, linespacing=1.55, color="#222222")


def panah(ax, x1, y1, x2, y2, label=None, warna="#444444", putus=False, geser=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=12, color=warna, linewidth=1.1,
                                 linestyle="--" if putus else "-"))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.09 + geser, label, ha="center",
                va="bottom", fontsize=6.8, fontfamily=FONT, color=warna, style="italic")


def gambar_peta(d):
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.set_xlim(0, 9.6)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    biru, tepi_biru = "#E8EEF7", "#3B5B8C"
    oranye, tepi_oranye = "#FDF2E0", "#B7791F"
    hop = d["identitas"]
    mem = d["memori_kb"]

    ax.add_patch(FancyBboxPatch((0.12, 0.95), 5.9, 3.4,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                facecolor="#F9FBFF", edgecolor="#9BB3D4",
                                linewidth=1.0, linestyle="--"))
    ax.text(0.28, 4.16, "LAPIS LAHAN DAN TEPI (EDGE)", fontsize=7.8,
            fontfamily=FONT, color="#5A7599", fontweight="bold")

    ax.add_patch(FancyBboxPatch((6.25, 0.95), 3.2, 3.4,
                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                facecolor="#FFFCF7", edgecolor="#D9B48F",
                                linewidth=1.0, linestyle="--"))
    ax.text(6.4, 4.16, "LAPIS CLOUD DAN MOBILE", fontsize=7.8,
            fontfamily=FONT, color="#A6753F", fontweight="bold")

    kotak(ax, 0.28, 1.15, 1.7, 2.75, "1. Mikrokontroler",
          "ESP32 · 12 node\n\nFreeRTOS\nEmbedded / RTOS\nRAM ~520 KB\nTanpa MMU\n\n"
          "Baca sensor 5 detik\nKendali pompa",
          biru, tepi_biru)

    kotak(ax, 2.42, 1.15, 1.9, 2.75, "2. Gateway kebun",
          "Raspberry Pi OS Lite\nServer (headless)\n\n"
          "Teruskan data sensor\nBuffer saat offline\n\n"
          f"Acuan ukur:\n{hop['hostname'][:19]}\n{hop['distro']}",
          biru, tepi_biru)

    kotak(ax, 4.72, 1.15, 1.15, 2.75, "3. Operator",
          "Komputer\noperator\n\nDesktop\n\n"
          f"{os.cpu_count()} CPU\n{mem['MemTotal'] // 1024 // 1024} GiB RAM\n\n"
          "Alat ukur dan\ndasbor",
          biru, tepi_biru)

    kotak(ax, 6.45, 2.7, 2.8, 1.2, "4. Server cloud",
          "Ubuntu Server LTS · Server\nAgregasi multi-gateway,\nbasis data, TLS",
          oranye, tepi_oranye, 7.2)

    kotak(ax, 6.45, 1.15, 2.8, 1.2, "5. Ponsel pemantau",
          "Android · Mobile\nSandbox UID, notifikasi,\nkendali pompa",
          oranye, tepi_oranye, 7.2)

    # aliran data (penuh) dan perintah (putus-putus)
    panah(ax, 1.98, 2.75, 2.42, 2.75, warna="#2F6B3C")
    panah(ax, 2.42, 2.45, 1.98, 2.45, warna="#A03B2C", putus=True)
    ax.text(2.2, 2.86, "data", ha="center", fontsize=6.4, fontfamily=FONT, color="#2F6B3C")
    ax.text(2.2, 2.22, "perintah", ha="center", fontsize=6.4, fontfamily=FONT,
            color="#A03B2C")

    panah(ax, 4.32, 2.75, 4.72, 2.75, warna="#2F6B3C")
    panah(ax, 4.72, 2.45, 4.32, 2.45, warna="#A03B2C", putus=True)

    panah(ax, 5.87, 3.35, 6.45, 3.35, warna="#2F6B3C")
    panah(ax, 6.45, 3.05, 5.87, 3.05, warna="#A03B2C", putus=True)
    ax.text(6.16, 3.46, "HTTPS", ha="center", fontsize=6.4, fontfamily=FONT,
            color="#2F6B3C")

    panah(ax, 8.6, 2.7, 8.6, 2.35, warna="#2F6B3C")
    panah(ax, 8.2, 2.35, 8.2, 2.7, warna="#A03B2C", putus=True)
    ax.text(8.75, 2.43, "REST", fontsize=6.4, fontfamily=FONT, color="#2F6B3C")

    ax.text(0.28, 0.62, "Hijau: data sensor mengalir ke atas (edge → cloud). "
                        "Merah putus-putus: perintah aktuator mengalir balik.",
            fontsize=7.2, fontfamily=FONT, color="#555555", style="italic")
    ax.text(0.28, 0.34, "Kotak 3 adalah mesin tempat angka pada laporan ini diukur; "
                        "kotak 1, 2, 4, dan 5 adalah perannya pada ekosistem.",
            fontsize=7.2, fontfamily=FONT, color="#555555", style="italic")

    ax.set_title("Peta ekosistem sistem operasi pada smart farming",
                 fontsize=11, fontfamily=FONT, fontweight="bold", pad=4)

    fig.tight_layout()
    fig.savefig(f"{OUT}/gambar-peta-ekosistem.png", dpi=220, facecolor="white",
                bbox_inches="tight")
    plt.close(fig)


def gambar_memori(d):
    mem = d["memori_kb"]
    total = mem["MemTotal"] / 1024
    tersedia = mem["MemAvailable"] / 1024
    terpakai = total - tersedia
    swap = mem["SwapTotal"] / 1024

    fig, ax = plt.subplots(figsize=(6.6, 2.1))
    ax.barh([0], [terpakai], color="#A03B2C", edgecolor="white", height=0.5,
            label=f"Terpakai {terpakai:.0f} MiB")
    ax.barh([0], [tersedia], left=[terpakai], color="#3B5B8C", edgecolor="white",
            height=0.5, label=f"Tersedia {tersedia:.0f} MiB")
    ax.set_yticks([])
    ax.set_xlim(0, total * 1.02)
    ax.set_xlabel("Memori (MiB)", fontfamily=FONT, fontsize=8.5)
    ax.tick_params(labelsize=7.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.legend(frameon=False, fontsize=7.5, ncol=2, loc="lower center",
              bbox_to_anchor=(0.5, 1.05))
    ax.set_title(f"Pemakaian RAM {d['identitas']['hostname']} "
                 f"(MemTotal {total:.0f} MiB, swap {swap:.0f} MiB)",
                 fontsize=9, fontfamily=FONT, fontweight="bold", pad=30)
    fig.tight_layout()
    fig.savefig(f"{OUT}/gambar-memori.png", dpi=220, facecolor="white")
    plt.close(fig)


def main():
    os.makedirs(OUT, exist_ok=True)
    with open("results/peta.json", encoding="utf-8") as f:
        d = json.load(f)
    gambar_peta(d)
    gambar_memori(d)
    print("gambar:", [f for f in sorted(os.listdir(OUT)) if f.endswith(".png")])


if __name__ == "__main__":
    main()
