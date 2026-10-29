"""Peta ekosistem SO untuk smart farming, dibaca dari mesin tempat skrip berjalan.

Klasifikasi dan diagram tidak ditebak: nilai RAM, kernel, dan jumlah CPU diambil
dari /proc dan /etc, bukan ditulis tangan.
"""
import json
import os
import platform
import shutil

KOMPONEN = [
    ("Mikrokontroler sensor (ESP32)", "FreeRTOS", "Embedded/RTOS",
     "Penjadwalan deterministik, RAM ratusan KB, tanpa MMU"),
    ("Gateway kebun (Raspberry Pi)", "Raspberry Pi OS Lite", "Server",
     "Headless, meneruskan data sensor, buffer lokal"),
    ("Server cloud pertanian", "Ubuntu Server LTS", "Server",
     "Agregasi multi-gateway, basis data, TLS"),
    ("Ponsel pemantau petani", "Android", "Mobile",
     "Sandbox UID, notifikasi, kontrol pompa"),
    ("Komputer operator (mesin ini)", "elementary OS (Linux)", "Desktop",
     "Alat ukur dan dasbor operator"),
]


def baca_meminfo():
    info = {}
    with open("/proc/meminfo", encoding="utf-8") as f:
        for baris in f:
            kunci, nilai = baris.split(":", 1)
            info[kunci.strip()] = int(nilai.strip().split()[0])
    return info


def identitas():
    osr = {}
    with open("/etc/os-release", encoding="utf-8") as f:
        for baris in f:
            if "=" in baris:
                k, v = baris.rstrip().split("=", 1)
                osr[k] = v.strip('"')
    return {
        "hostname": platform.node(),
        "kernel": platform.release(),
        "arsitektur": platform.machine(),
        "distro": osr.get("PRETTY_NAME", "tidak diketahui"),
        "id_distro": osr.get("ID", "?"),
        "python": platform.python_version(),
    }


def hitung_beban(jumlah_node=12, jeda_detik=5, ukuran_baris=160):
    """Perkiraan volume data harian dari sejumlah node sensor."""
    baris_per_node = 86400 // jeda_detik
    total_baris = jumlah_node * baris_per_node
    total_byte = total_baris * ukuran_baris
    return {
        "jumlah_node": jumlah_node,
        "jeda_detik": jeda_detik,
        "baris_per_node": baris_per_node,
        "total_baris": total_baris,
        "data_kib": total_byte / 1024,
        "data_mib": total_byte / (1024 * 1024),
    }


def main():
    ident = identitas()
    mem = baca_meminfo()
    beban = hitung_beban()

    total_mib = mem["MemTotal"] / 1024
    tersedia_mib = mem["MemAvailable"] / 1024
    terpakai_mib = total_mib - tersedia_mib
    persen = terpakai_mib / total_mib * 100

    disk = shutil.disk_usage("/")
    disk_total_gib = disk.total / 1024**3
    disk_pakai_gib = disk.used / 1024**3

    print("=== PEMETAAN EKOSISTEM SO SMART FARMING ===")
    print(f"Mesin pengukuran : {ident['hostname']}")
    print(f"Distro           : {ident['distro']}")
    print(f"Kernel           : {ident['kernel']} ({ident['arsitektur']})")
    print(f"Python           : {ident['python']}")
    print()
    print(f"{'Perangkat':<34} {'Sistem operasi':<24} {'Jenis':<15} Fungsi utama")
    print("-" * 118)
    for perangkat, so, jenis, fungsi in KOMPONEN:
        print(f"{perangkat:<34} {so:<24} {jenis:<15} {fungsi}")

    print()
    print("=== PENGUKURAN SUMBER DAYA (data nyata) ===")
    print(f"MemTotal         : {mem['MemTotal']} kB ({total_mib:.1f} MiB)")
    print(f"MemAvailable     : {mem['MemAvailable']} kB ({tersedia_mib:.1f} MiB)")
    print(f"Terpakai         : {terpakai_mib:.1f} MiB ({persen:.2f}% dari total)")
    print(f"SwapTotal        : {mem.get('SwapTotal', 0)} kB")
    print(f"CPU logis        : {os.cpu_count()}")
    print(f"Penyimpanan /    : {disk_pakai_gib:.0f} GiB terpakai dari {disk_total_gib:.0f} GiB")

    print()
    print(f"=== PERKIRAAN BEBAN {beban['jumlah_node']} NODE SENSOR ===")
    print(f"Jeda pembacaan   : {beban['jeda_detik']} detik")
    print(f"Baris per node   : {beban['baris_per_node']} baris/hari")
    print(f"Total baris/hari : {beban['total_baris']} baris/hari")
    print(f"Volume data/hari : {beban['data_mib']:.2f} MiB/hari")
    print(f"Volume 30 hari   : {beban['data_mib'] * 30:.1f} MiB")

    with open("results/peta.json", "w", encoding="utf-8") as f:
        json.dump({"identitas": ident,
                   "memori_kb": {k: mem[k] for k in
                                 ("MemTotal", "MemAvailable", "MemFree", "Buffers",
                                  "Cached", "SwapTotal")},
                   "cpu_logis": os.cpu_count(),
                   "disk_gib": {"total": round(disk_total_gib, 1),
                                "terpakai": round(disk_pakai_gib, 1)},
                   "beban": beban,
                   "komponen": [{"perangkat": p, "so": s, "jenis": j, "fungsi": f}
                                for p, s, j, f in KOMPONEN]},
                  f, indent=2)
    print("\ntersimpan: results/peta.json")


if __name__ == "__main__":
    main()
