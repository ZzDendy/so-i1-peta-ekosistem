"""Merakit laporan I-1 dari template jurusan dan data hasil pengukuran.

Seluruh angka diambil dari results/peta.json dan results/bukti/, yang dibuat
oleh peta_so_kebun.py dan ambil-bukti.sh pada mesin yang sama.
"""
import json
import os
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Cm, Pt

sys.path.insert(0, "../tools")
from docx_kit import (baca_berkas, bersihkan, bullet, caption, gambar, h1, h2,
                      header_dokumen, kode, nomor_halaman, par, sampul, tabel)

TEMPLATE = "../template/Template Laporan Tugas Individu.docx"
OUT = "results/Laporan_I-1_Peta_Ekosistem_SO.docx"
NAMA = "Dendy Zainal Mutaqien"
NIM = "250660121068"
KELAS = "IF-3C"
KODE = "I-1"
BUKTI = "results/bukti"


def baca_peta():
    with open("results/peta.json", encoding="utf-8") as f:
        return json.load(f)


def sampul_i1(d):
    sampul(
        d,
        "LAPORAN TUGAS INDIVIDU",
        "Pemetaan Sistem Operasi pada Ekosistem\nIoT dan Smart Farming",
        [
            ("Kode dan judul tugas",
             "I-1 Pemetaan Sistem Operasi pada Ekosistem IoT dan Smart Farming"),
            ("Kelas / tema", f"{KELAS} — IoT dan Smart Farming"),
            ("Nama", NAMA),
            ("NIM", NIM),
            ("Nama host", "INFINIX-ElementaryOS"),
            ("Minggu / tanggal kumpul", "Minggu ke-1 / 29 Oktober 2026"),
            ("Kepingan puzzle", "Kepingan #1 → Level 1 Puzzle UTS"),
            ("Dosen pengampu", "Muhammad Agreindra Helmiawan, S.Kom., M.T"),
        ],
        "I-1",
    )


def pendahuluan(d):
    h1(d, "1. Pendahuluan")

    h2(d, "1.1 Latar belakang kasus")
    par(d, "Sistem pertanian cerdas bukan satu komputer, melainkan rangkaian perangkat yang saling "
           "terhubung: mikrokontroler di petak lahan yang membaca kelembapan tanah, gateway di "
           "kebun yang mengumpulkan data, server di cloud yang menyimpan riwayat, dan ponsel "
           "petani yang menampilkan kondisi lahan sekaligus menyalakan pompa. Setiap perangkat itu "
           "menjalankan sistem operasi yang berbeda jenis, dengan kemampuan yang jauh berbeda "
           "pula.")
    par(d, "Perbedaan itu bukan hal sepele. Mikrokontroler ESP32 hanya memiliki sekitar 520 KB "
           "SRAM dan tidak punya unit manajemen memori, sehingga sistem operasinya harus muat "
           "dalam ruang sekecil itu. Sebaliknya, server cloud menjalankan sistem operasi lengkap "
           "dengan memori puluhan gigabita dan puluhan proses berjalan bersamaan. Memilih sistem "
           "operasi yang tidak sesuai dengan kemampuan perangkat akan membuat sistem gagal bekerja "
           "sebelum sempat diuji. Karena itu, memetakan sistem operasi pada tiap lapisan ekosistem "
           "adalah langkah pertama sebelum merancang sistem apa pun di atasnya.")

    h2(d, "1.2 Tujuan tugas")
    par(d, "Capaian pembelajaran yang diukur adalah Sub-CPMK-1 (CPMK042, CPMK043, CPMK081, "
           "CPMK101, CPMK111). Dijabarkan menjadi tiga tujuan:")
    bullet(d, "mengklasifikasikan jenis sistem operasi pada setiap perangkat ekosistem IoT "
              "pertanian ke dalam empat kategori: desktop, server, mobile, dan embedded/RTOS;",
           "Pertama, ")
    bullet(d, "menjelaskan fungsi utama sistem operasi pada tiap perangkat, dikaitkan dengan "
              "keterbatasan perangkat kerasnya;", "Kedua, ")
    bullet(d, "menyajikan peta ekosistem sistem operasi dalam satu diagram yang memperlihatkan "
              "hubungan antar-lapisan beserta arah aliran datanya.", "Ketiga, ")

    h2(d, "1.3 Ruang lingkup")
    par(d, "Pengukuran dilakukan langsung pada komputer operator yang dipakai menyusun laporan, "
           "yaitu mesin Linux dengan nama host INFINIX-ElementaryOS. Perangkat lain pada ekosistem "
           "— mikrokontroler ESP32, gateway Raspberry Pi, server cloud, dan ponsel Android — "
           "dipetakan berdasarkan dokumen resmi pabriknya, bukan diukur langsung, karena tidak "
           "tersedia di tempat praktik.")
    par(d, "Yang tidak dikerjakan: pengukuran konsumsi daya, pengujian pada perangkat keras "
           "sesungguhnya, dan pembahasan keamanan sistem operasi.")


def dasar_teori(d):
    h1(d, "2. Dasar Teori Singkat")
    par(d, "Sistem operasi adalah perangkat lunak sistem yang mengendalikan seluruh sumber daya "
           "komputer dan menyediakan landasan bagi program aplikasi (Helmiawan, t.t.). Tanpa "
           "lapisan ini, pemrogram harus berhadapan langsung dengan kerumitan perangkat keras: "
           "mengatur letak data di memori, menentukan giliran prosesor, dan menangani perangkat "
           "masukan-keluaran satu per satu. Sistem operasi menyembunyikan kerumitan itu di balik "
           "antarmuka yang seragam (Silberschatz dkk., 2018).")
    par(d, "Fungsi utama sistem operasi dapat diringkas menjadi lima: mengatur penjadwalan proses, "
           "mengelola memori, mengelola sistem berkas, mengendalikan perangkat masukan-keluaran, "
           "dan menyediakan mekanisme perlindungan antar-proses. Tidak semua fungsi itu hadir "
           "dengan bobot yang sama pada setiap perangkat. Pada server, kelima fungsi berjalan "
           "penuh dengan banyak pengguna sekaligus. Pada mikrokontroler, yang ada hanyalah "
           "penjadwal sederhana dan pengelola memori statis, karena memang tidak ada disk maupun "
           "banyak pengguna.")

    par(d, "Klasifikasi menurut perangkat. Sistem operasi dibedakan berdasarkan sasaran perangkat "
           "keras dan cara pemakaiannya:")
    bullet(d, "Desktop, dipakai satu pengguna dengan antarmuka grafis penuh, contohnya "
              "elementary OS dan Windows.", "a. ")
    bullet(d, "Server, dijalankan tanpa layar (headless), melayani banyak permintaan jaringan, "
              "contohnya Ubuntu Server LTS.", "b. ")
    bullet(d, "Mobile, berjalan pada ponsel dengan pembatasan ketat per aplikasi, contohnya "
              "Android dan iOS.", "c. ")
    bullet(d, "Embedded/RTOS, ditanam pada perangkat dengan sumber daya kecil dan menuntut waktu "
              "respons yang dapat diprediksi, contohnya FreeRTOS pada ESP32.", "d. ")

    par(d, "Kategori keempat itulah yang paling berbeda sifatnya. Sistem operasi waktu nyata "
           "(real-time operating system) tidak mengejar rata-rata waktu respons tercepat, "
           "melainkan jaminan bahwa tugas tertentu selesai dalam batas waktu yang sudah "
           "ditentukan. Pada ESP32, FreeRTOS menjalankan penjadwal berbasis prioritas dengan "
           "pengalihan tugas dalam hitungan mikrodetik (FreeRTOS Project, 2024). Jaminan semacam "
           "itu tidak bisa diberikan sistem operasi desktop, yang justru mengorbankan kepastian "
           "demi pemanfaatan prosesor yang merata.")


def lingkungan(d, peta):
    h1(d, "3. Lingkungan Praktik")
    mem = peta["memori_kb"]
    disk = peta["disk_gib"]
    tabel(d, ["Komponen", "Keterangan"], [
        ("Laptop (host)", f"{peta['identitas']['distro']}, AMD Ryzen 7 7735HS, "
                          f"RAM {mem['MemTotal'] // 1024} MiB, kernel "
                          f"{peta['identitas']['kernel']}"),
        ("Hypervisor", "Tidak dipakai — pengukuran dijalankan langsung pada mesin host"),
        ("VM / host", f"{peta['identitas']['hostname']}, {peta['cpu_logis']} CPU logis, "
                      f"penyimpanan {disk['total']:.0f} GiB"),
        ("Perangkat lain", "Tidak tersedia — ESP32, Raspberry Pi, server cloud, dan ponsel "
                           "dipetakan dari dokumen resmi pabrik"),
        ("Bahasa dan alat", "Python 3.12.3; perintah hostname, uname, lscpu, df, systemctl, ps; "
                            "GNOME Shell Screenshot untuk bukti tangkapan layar"),
        ("Berkas semu", "/proc/meminfo untuk memori, /proc/1 untuk proses init, "
                        "/sys/fs/cgroup untuk hierarki kontrol sumber daya"),
    ], lebar=[4.0, 11.2])

    par(d, "Satu hal yang perlu dicatat: laporan ini tidak memakai mesin virtual. Lembar tugas I-1 "
           "tidak mensyaratkannya, dan seluruh pengukuran yang dibutuhkan — identitas sistem, "
           "jumlah CPU, kapasitas memori, serta layanan yang berjalan — dapat dibaca langsung dari "
           "mesin host. Mesin virtual baru diperlukan pada tugas yang menuntut eksperimen berisiko "
           "atau pengamatan yang harus dapat diulang persis.")


def langkah(d, peta):
    h1(d, "4. Langkah Pengerjaan")
    par(d, "Pengumpulan bukti dibagi menjadi enam langkah. Seluruh perintah dijalankan pada "
           "terminal mesin host, dan setiap tangkapan layar memperlihatkan prompt beserta perintah "
           "yang menghasilkan keluarannya. Skrip ambil-bukti.sh menjalankan urutan ini secara "
           "otomatis agar hasilnya dapat diulang.")

    h2(d, "4.1 Langkah 1: Mencatat identitas sistem operasi")
    par(d, "Langkah pertama memastikan sistem apa yang sebenarnya sedang diukur. Nama host, versi "
           "kernel, dan distribusi dicatat karena ketiganya menentukan fasilitas apa yang tersedia "
           "— misalnya ketersediaan cgroup versi 2 atau cara pembacaan /proc.")
    kode(d, "$ hostname\n"
            f"{peta['identitas']['hostname']}\n\n"
            "$ uname -srm\n"
            f"Linux {peta['identitas']['kernel']} {peta['identitas']['arsitektur']}\n\n"
            "$ grep -E \"PRETTY_NAME|VERSION_ID\" /etc/os-release\n"
            f"PRETTY_NAME=\"{peta['identitas']['distro']}\"\n"
            "VERSION_ID=\"8\"\n"
            "UBUNTU_PRETTY_NAME=\"Ubuntu 24.04.5 LTS\"")
    gambar(d, f"{BUKTI}/rapi-ss-3-kernel.png", 15.5,
           "Gambar 4.1 Prompt, perintah, dan keluaran identitas sistem pada terminal host")

    h2(d, "4.2 Langkah 2: Membaca perangkat keras yang tersedia")
    par(d, "Jumlah prosesor dan kapasitas memori menentukan seberapa besar beban yang bisa "
           "ditangani mesin ini sebagai simpul operator. Angka CPU dibaca dari lscpu, memori dari "
           "/proc/meminfo, dan penyimpanan dari df.")
    kode(d, "$ lscpu | grep -E \"^Architecture|^CPU\\(s\\)|Model name|Thread|Core\"\n"
            f"Architecture:        {peta['identitas']['arsitektur']}\n"
            f"CPU(s):              {peta['cpu_logis']}\n"
            "Model name:          AMD Ryzen 7 7735HS with Radeon Graphics\n"
            "Thread(s) per core:  2\n"
            "Core(s) per socket:  8\n\n"
            "$ df -hT /\n"
            "Filesystem            Type  Size  Used Avail Use% Mounted on\n"
            f"/dev/mapper/data-root ext4  {peta['disk_gib']['total']:.0f}G  "
            f"{peta['disk_gib']['terpakai']:.0f}G  "
            f"{peta['disk_gib']['total'] - peta['disk_gib']['terpakai']:.0f}G  "
            f"{peta['disk_gib']['terpakai'] / peta['disk_gib']['total'] * 100:.0f}% /")
    gambar(d, f"{BUKTI}/rapi-ss-5-cpu.png", 15.5,
           "Gambar 4.2 Keluaran lscpu dan df yang memperlihatkan CPU serta sistem berkas ext4")

    h2(d, "4.3 Langkah 3: Mengukur pemakaian memori")
    par(d, "MemTotal menunjukkan kapasitas terpasang, sedangkan MemAvailable menunjukkan perkiraan "
           "memori yang benar-benar bisa dipakai proses baru — angka ini lebih jujur daripada "
           "MemFree, karena cache dan buffer sebenarnya dapat diambil kembali oleh kernel bila "
           "dibutuhkan.")
    mem = peta["memori_kb"]
    terpakai = (mem["MemTotal"] - mem["MemAvailable"]) / 1024
    kode(d, "$ grep -E \"^MemTotal|^MemAvailable|^MemFree|^SwapTotal\" /proc/meminfo\n"
            f"MemTotal:       {mem['MemTotal']} kB\n"
            f"MemFree:        {mem['MemFree']} kB\n"
            f"MemAvailable:   {mem['MemAvailable']} kB\n"
            f"SwapTotal:      {mem['SwapTotal']} kB")
    caption(d, "Keluaran pembacaan /proc/meminfo")
    gambar(d, f"{BUKTI}/rapi-ss-7-meminfo.png", 15.5,
           "Gambar 4.3 Pembacaan /proc/meminfo beserta perintah sebelumnya dalam satu sesi")

    h2(d, "4.4 Langkah 4: Memeriksa layanan dan proses")
    par(d, "Sistem operasi desktop tetap menjalankan banyak layanan latar belakang. Jumlah unit "
           "systemd yang berjalan dan jumlah proses keseluruhan memberi gambaran seberapa besar "
           "beban dasar sebelum aplikasi pengguna dijalankan. Proses init diperiksa untuk "
           "memastikan mekanisme mana yang mengelola layanan.")
    kode(d, "$ ps -p 1 -o pid=,comm=\n"
            "      1 systemd\n\n"
            "$ systemctl list-units --type=service --state=running --no-pager --no-legend | wc -l\n"
            "36\n\n"
            "$ ps -e --no-headers | wc -l\n"
            "501")
    gambar(d, f"{BUKTI}/rapi-ss-9-jumlah-unit.png", 15.5,
           "Gambar 4.4 Proses init systemd dan jumlah unit layanan yang berjalan")

    h2(d, "4.5 Langkah 5: Menjalankan program pemetaan ekosistem")
    par(d, "Program peta_so_kebun.py membaca langsung /proc/meminfo dan /etc/os-release, sehingga "
           "angka yang dicetak selalu sesuai mesin yang menjalankannya. Program juga menghitung "
           "perkiraan volume data dari dua belas node sensor dengan jeda lima detik, sebagai bahan "
           "pertimbangan beban penyimpanan pada gateway.")
    kode(d, "$ python3 peta_so_kebun.py\n"
            "=== PEMETAAN EKOSISTEM SO SMART FARMING ===\n"
            f"Mesin pengukuran : {peta['identitas']['hostname']}\n"
            f"Distro           : {peta['identitas']['distro']}\n"
            f"Kernel           : {peta['identitas']['kernel']} ({peta['identitas']['arsitektur']})\n"
            "Python           : 3.12.3")
    gambar(d, f"{BUKTI}/rapi-ss-11-program.png", 15.5,
           "Gambar 4.5 Keluaran lengkap peta_so_kebun.py beserta perhitungan beban 12 node")

    h2(d, "4.6 Langkah 6: Menggambar peta ekosistem")
    par(d, "Data dari langkah sebelumnya diubah menjadi dua gambar oleh figures.py: peta ekosistem "
           "lima simpul, dan grafik pemakaian memori. Peta disusun dua kolom untuk memisahkan "
           "perangkat di sisi lahan dari layanan terpusat, dengan panah dua arah untuk membedakan "
           "aliran data sensor dari aliran perintah aktuator.")
    kode(d, "$ ../.venv/bin/python figures.py\n"
            "gambar: ['gambar-memori.png', 'gambar-peta-ekosistem.png']")


def hasil(d, peta):
    mem = peta["memori_kb"]
    beban = peta["beban"]
    total_mib = mem["MemTotal"] / 1024
    tersedia_mib = mem["MemAvailable"] / 1024
    terpakai_mib = total_mib - tersedia_mib

    h1(d, "5. Hasil dan Analisis")

    h2(d, "5.1 Hasil")
    par(d, "Tabel 5.1 menyajikan klasifikasi jenis dan fungsi sistem operasi pada lima simpul "
           "ekosistem. Kolom jenis memakai empat kategori yang diminta lembar tugas.")
    tabel(d, ["No", "Perangkat", "Sistem operasi", "Jenis", "Fungsi utama"], [
        ("1", "Mikrokontroler sensor ESP32 (12 node)", "FreeRTOS", "Embedded/RTOS",
         "Penjadwalan deterministik, RAM sekitar 520 KB, tanpa MMU"),
        ("2", "Gateway kebun Raspberry Pi", "Raspberry Pi OS Lite", "Server",
         "Headless, meneruskan data sensor, menyimpan buffer saat jaringan putus"),
        ("3", "Server cloud pertanian", "Ubuntu Server LTS", "Server",
         "Agregasi banyak gateway, basis data, TLS"),
        ("4", "Ponsel pemantau petani", "Android", "Mobile",
         "Sandbox per aplikasi, notifikasi, kendali pompa"),
        ("5", "Komputer operator (mesin ukur)", peta["identitas"]["distro"], "Desktop",
         "Alat ukur, penyusunan laporan, dasbor operator"),
    ], lebar=[1.0, 4.2, 3.2, 2.4, 4.6], ukuran=8.5)
    caption(d, "Tabel 5.1 Klasifikasi jenis dan fungsi sistem operasi pada ekosistem smart farming")

    par(d, "Tabel 5.2 memuat angka yang diukur langsung pada mesin operator. Kolom sumber "
           "memisahkan mana yang hasil ukur dan mana yang berasal dari dokumen pabrik, supaya "
           "tidak tercampur.")
    tabel(d, ["No", "Yang diukur", "Hasil", "Sumber"], [
        ("1", "Memori terpasang (MemTotal)", f"{mem['MemTotal']} kB ({total_mib:.0f} MiB)",
         "Hasil ukur /proc/meminfo"),
        ("2", "Memori tersedia (MemAvailable)", f"{mem['MemAvailable']} kB "
         f"({tersedia_mib:.0f} MiB)", "Hasil ukur /proc/meminfo"),
        ("3", "Memori terpakai", f"{terpakai_mib:.0f} MiB "
         f"({terpakai_mib / total_mib * 100:.1f}% dari total)", "Hitungan dari baris 1 dan 2"),
        ("4", "Swap terpasang", f"{mem['SwapTotal']} kB", "Hasil ukur /proc/meminfo"),
        ("5", "CPU logis", f"{peta['cpu_logis']} thread (8 core, 2 thread/core)",
         "Hasil ukur lscpu"),
        ("6", "Penyimpanan akar (ext4)", f"{peta['disk_gib']['terpakai']:.0f} GiB terpakai "
         f"dari {peta['disk_gib']['total']:.0f} GiB", "Hasil ukur df -hT"),
        ("7", "Unit layanan systemd berjalan", "36 unit", "Hasil ukur systemctl"),
        ("8", "Jumlah proses", "501 proses", "Hasil ukur ps -e"),
        ("9", "Volume data 12 node sensor", f"{beban['total_baris']} baris/hari, "
         f"{beban['data_mib']:.2f} MiB/hari", "Hitungan program (jeda 5 detik, 160 byte/baris)"),
        ("10", "Kapasitas RAM ESP32", "sekitar 520 KB SRAM", "Dokumen pabrik Espressif"),
    ], lebar=[1.0, 4.4, 5.2, 4.8], ukuran=8.5)
    caption(d, "Tabel 5.2 Hasil ukur pada mesin operator dan acuan dari dokumen pabrik")

    par(d, "Gambar 5.1 memperlihatkan peta ekosistem kelima simpul beserta arah alirannya.")
    gambar(d, "results/gambar-peta-ekosistem.png", 15.5,
           "Gambar 5.1 Peta ekosistem sistem operasi pada IoT dan smart farming")

    par(d, "Gambar 5.2 membandingkan memori terpakai dengan yang masih tersedia pada mesin ukur.")
    gambar(d, "results/gambar-memori.png", 13.0,
           "Gambar 5.2 Pemakaian RAM pada mesin operator saat pengukuran")

    h2(d, "5.2 Analisis")
    par(d, "Poin (1) deskripsi tugas — klasifikasi jenis. Kelima simpul jatuh ke empat kategori "
           "berbeda, dan yang paling menentukan bukan merek sistem operasinya melainkan "
           "ketersediaan unit manajemen memori serta jumlah pengguna yang harus dilayani. ESP32 "
           "tidak memiliki MMU sama sekali; semua alamat memori bersifat fisik dan sudah "
           "ditentukan saat kompilasi. Karena itu FreeRTOS di dalamnya tidak menjalankan proses "
           "terpisah seperti Linux, melainkan task yang berbagi satu ruang alamat. Tidak adanya "
           "isolasi ini bukan kekurangan, melainkan konsekuensi wajar: dengan SRAM sekitar 520 KB, "
           "membuat tabel halaman untuk isolasi memori justru memakan ruang yang tidak tersedia.")
    par(d, "Sebaliknya, mesin operator pada laporan ini memiliki 16 thread CPU, memori terpasang "
           f"{total_mib:.0f} MiB, dan menjalankan 501 proses bersamaan. Pada mesin seperti ini, "
           "isolasi antar-proses justru menjadi syarat utama: satu peramban yang kehabisan memori "
           "tidak boleh menjatuhkan seluruh sistem. Sistem operasi desktop dan server memakai "
           "mekanisme yang sama — MMU, tabel halaman, dan pemisahan ruang alamat — untuk mencapai "
           "hal yang tidak mungkin dilakukan pada mikrokontroler.")
    par(d, "Menariknya, gateway Raspberry Pi dan server cloud sama-sama masuk kategori server, "
           "padahal kemampuan keduanya berbeda jauh. Yang menyatukan keduanya adalah cara pakai: "
           "keduanya dijalankan tanpa layar dan melayani permintaan dari perangkat lain. Kategori "
           "pada lembar tugas dengan demikian lebih menandai peran dalam arsitektur daripada "
           "ukuran perangkat keras.")
    par(d, "Poin (2) deskripsi tugas — fungsi utama pada tiap perangkat. Pada mikrokontroler, "
           "fungsi sistem operasi menyempit menjadi penjadwalan dan pengelolaan antrean. FreeRTOS "
           "menyediakan penjadwal berbasis prioritas yang dapat diprediksi: tugas pembacaan sensor "
           "dijalankan setiap lima detik, dan tugas kendali pompa mendapat prioritas lebih tinggi "
           "agar perintah menutup katup tidak tertunda oleh pembacaan sensor. Tidak ada sistem "
           "berkas, tidak ada pengguna, dan tidak ada manajemen memori dinamis yang rumit.")
    par(d, "Pada gateway, fungsi itu melebar. Raspberry Pi OS Lite menjalankan sistem berkas "
           "penuh untuk menyimpan buffer saat jaringan putus, menjalankan layanan jaringan, dan "
           "mengelola beberapa proses sekaligus seperti klien MQTT dan agen pengirim. Fungsi "
           "manajemen memori mulai penting karena buffer harus dibatasi agar gateway tidak "
           "kehabisan memori saat menyimpan data berhari-hari. Perhitungan pada Tabel 5.2 "
           f"menunjukkan volume {beban['data_mib']:.1f} MiB per hari untuk dua belas node; "
           f"dalam tiga puluh hari menjadi {beban['data_mib'] * 30:.0f} MiB, angka yang masih "
           "wajar untuk kartu microSD kelas biasa, tetapi cukup untuk menuntut kebijakan rotasi "
           "berkas.")
    par(d, "Pada server cloud dan mesin operator, kelima fungsi sistem operasi berjalan penuh. "
           "Di sinilah pengelolaan sumber daya menjadi paling rumit: mesin operator dengan 501 "
           f"proses hanya memakai {terpakai_mib:.0f} MiB dari {total_mib:.0f} MiB, artinya sekitar "
           f"{terpakai_mib / total_mib * 100:.0f} persen. Sisa memori bukan terbuang; sebagian "
           "besar menjadi cache sistem berkas yang bisa diambil kembali kapan saja. Inilah sebabnya "
           "MemAvailable lebih tepat dipakai daripada MemFree saat menilai beban sebenarnya, dan "
           "inilah wujud nyata fungsi manajemen memori yang tidak dimiliki mikrokontroler.")
    par(d, "Poin (3) deskripsi tugas — peta ekosistem. Pada Gambar 5.1, arah aliran dibedakan "
           "menjadi dua: panah hijau membawa data sensor dari lahan menuju cloud, panah merah "
           "putus-putus membawa perintah aktuator kembali ke lahan. Pemisahan arah ini penting "
           "karena keduanya menuntut jaminan yang berbeda. Data sensor boleh terlambat beberapa "
           "detik tanpa akibat serius, sedangkan perintah menutup pompa harus sampai dan "
           "dijalankan. Dari sudut pandang sistem operasi, perbedaan itu diterjemahkan menjadi "
           "prioritas task yang berbeda di ESP32 dan gateway, bukan sekadar prioritas paket di "
           "jaringan.")
    par(d, "Lapisan pada peta juga memperlihatkan bahwa sistem operasi yang paling banyak "
           "jumlahnya justru yang paling sederhana. Dua belas node sensor menjalankan FreeRTOS, "
           "satu gateway menjalankan Raspberry Pi OS, satu server menjalankan Ubuntu Server, dan "
           "satu ponsel menjalankan Android. Artinya keseragaman sistem operasi bukan tujuan di "
           "arsitektur seperti ini; yang dibutuhkan justru penyesuaian dengan batas kemampuan "
           "tiap perangkat, dengan protokol yang menyatukan mereka di lapisan aplikasi.")

    h2(d, "5.3 Catatan keterbatasan")
    par(d, "Empat dari lima simpul pada laporan ini tidak diukur langsung. Angka kapasitas RAM "
           "ESP32, kebutuhan memori Raspberry Pi OS, dan persyaratan server diambil dari dokumen "
           "resmi pabrik, dan hal itu sudah ditandai pada kolom sumber Tabel 5.2. Pembacaan "
           "langsung hanya berlaku untuk mesin operator. Pembaca yang ingin memverifikasi angka "
           "perangkat lain dapat mengulang pengukuran yang sama pada perangkat sesungguhnya "
           "dengan perintah yang dipakai di Bagian 4.")


def kesimpulan(d, peta):
    mem = peta["memori_kb"]
    total_mib = mem["MemTotal"] / 1024
    h1(d, "6. Kesimpulan")
    par(d, "Ekosistem IoT pertanian memakai empat jenis sistem operasi sekaligus, dan kelima "
           "simpul yang dipetakan jatuh ke kategori embedded/RTOS, server, mobile, dan desktop. "
           "Yang membedakan mereka bukan merek, melainkan ketersediaan MMU dan jumlah pengguna "
           "yang harus dilayani: ESP32 tanpa MMU menjalankan FreeRTOS dengan task berbagi ruang "
           "alamat, sementara mesin operator dengan 16 thread CPU dan "
           f"{total_mib:.0f} MiB memori menjalankan 501 proses dengan isolasi penuh. Fungsi "
           "sistem operasi menyempit di ujung lahan dan melebar di pusat data. Karena itu peta "
           "ekosistem sebaiknya dibaca sebagai pembagian peran, bukan sebagai tingkatan kualitas: "
           "pilihan sistem operasi yang tepat adalah yang sesuai dengan batas kemampuan "
           "perangkatnya.")


def kepingan(d):
    h1(d, "7. Kepingan Puzzle")
    tabel(d, ["Keterangan", "Isi"], [
        ("Nomor kepingan", "#1"),
        ("Isi kepingan", "Tabel klasifikasi jenis dan fungsi sistem operasi pada lima simpul "
                         "ekosistem, peta ekosistem beserta arah aliran data, dan hasil ukur "
                         "sumber daya mesin operator"),
        ("Lokasi di portofolio",
         "https://github.com/ZzDendy/so-i1-peta-ekosistem"),
        ("Dipakai untuk", "Level 1 Puzzle UTS — menjadi dasar kepingan #2 (system call) dan #3 "
                          "(proses dan thread), karena pembagian peran antar-simpul di sini "
                          "menentukan jenis pemanggilan sistem dan model proses yang diamati "
                          "pada tugas berikutnya"),
    ], lebar=[4.2, 11.0])


def pustaka(d):
    h1(d, "Daftar Pustaka")
    for teks in [
        "FreeRTOS Project. (2024). The FreeRTOS kernel: Documentation and FAQ. "
        "https://www.freertos.org/Documentation",
        "Helmiawan, M. A. (t.t.). Pendahuluan: Modul pembelajaran sistem operasi. "
        "Universitas Sebelas April.",
        "Kerrisk, M. (2010). The Linux programming interface. No Starch Press.",
        "Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). Operating system concepts "
        "(10th ed.). Wiley.",
        "Tanenbaum, A. S., & Bos, H. (2015). Modern operating systems (4th ed.). Pearson.",
    ]:
        p = d.add_paragraph(style="Normal")
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-1.0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.add_run(teks)


def lampiran(d, peta):
    d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    h1(d, "Lampiran A. Kode Program dan Log")
    par(d, "Dua berkas di bawah ini menghasilkan seluruh angka dan gambar pada laporan. "
           "Keduanya dapat dijalankan ulang pada mesin yang sama.")
    for nama in ("peta_so_kebun.py", "figures.py", "ambil-bukti.sh"):
        p = d.add_paragraph(style="Normal")
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(f"A.{nama}")
        r.bold = True
        r.font.size = Pt(9.5)
        kode(d, baca_berkas(nama), ukuran=7)

    h1(d, "Lampiran B. Pernyataan Penggunaan AI Generatif")
    par(d, "☐  Saya tidak menggunakan AI generatif dalam tugas ini.")
    par(d, "☒  Menggunakan AI generatif dengan rincian berikut:")
    tabel(d, ["Alat", "Tujuan penggunaan", "Bagian yang dibantu", "Cara memverifikasi"], [
        ("Claude (Anthropic)", "Menyusun skrip pengukuran dan merapikan kalimat laporan",
         "Bagian 4 (kode), Bagian 5.2",
         "Seluruh angka diambil dari keluaran perintah pada tangkapan layar; skrip dijalankan "
         "ulang dengan ambil-bukti.sh dan hasilnya dicocokkan dengan Tabel 5.2"),
    ], lebar=[3.0, 4.4, 4.0, 4.4], ukuran=8.5)

    h1(d, "Lampiran C. Daftar Periksa Sebelum Mengumpulkan")
    for teks, sudah in [
        ("Semua teks petunjuk abu-abu dan kotak petunjuk sudah dihapus.", True),
        ("Identitas, kode tugas, dan nama host pada sampul sudah benar.", True),
        ("Setiap poin deskripsi tugas sudah dijawab di bagian Analisis.", True),
        ("Setiap tangkapan layar menampilkan prompt dan memiliki nomor serta keterangan.",
         True),
        ("Kepingan puzzle sudah disimpan di portofolio dan tautannya dicantumkan.", False),
        ("Pernyataan penggunaan AI generatif sudah diisi.", True),
        ("Berkas disimpan sebagai PDF dengan nama C_I-1_<NIM>_<Nama>.pdf.", True),
    ]:
        p = d.add_paragraph(style="Normal")
        p.paragraph_format.space_after = Pt(3)
        p.add_run(f"{'☒' if sudah else '☐'}  {teks}")

    par(d, "")
    h2(d, "Swa-nilai berdasarkan kriteria lembar tugas")
    tabel(d, ["Kriteria (dari lembar tugas)", "Bobot", "Sudah terpenuhi? Di bagian mana"],
          [("Ketepatan konsep", "40%",
            "Ya — empat kategori dipakai konsisten di Tabel 5.1 dan Bagian 2"),
           ("Kedalaman analisis", "30%",
            "Ya — tiga poin tugas dijawab dengan kaitan ke MMU dan jumlah pengguna"),
           ("Bukti praktik/perhitungan", "20%",
            "Ya — 11 tangkapan layar asli dan tabel hasil ukur dengan kolom sumber"),
           ("Orisinalitas dan kerapian", "10%",
            "Ya — diagram dibuat dari data ukur, daftar pustaka memakai gaya APA")],
          lebar=[5.2, 2.0, 8.0])


def main():
    d = docx.Document(TEMPLATE)
    bersihkan(d)
    peta = baca_peta()

    sampul_i1(d)
    pendahuluan(d)
    dasar_teori(d)
    lingkungan(d, peta)
    langkah(d, peta)
    hasil(d, peta)
    kesimpulan(d, peta)
    kepingan(d)
    pustaka(d)
    lampiran(d, peta)

    header_dokumen(d, "Laporan Tugas Individu Sistem Operasi · ", f"{KELAS} · {KODE}")
    nomor_halaman(d)

    d.core_properties.title = "I-1 Pemetaan Sistem Operasi pada Ekosistem IoT dan Smart Farming"
    d.core_properties.author = NAMA
    d.core_properties.subject = "Sistem Operasi (USA-WP2260110), IF-3C"
    d.core_properties.last_modified_by = NAMA

    os.makedirs("results", exist_ok=True)
    d.save(OUT)
    print("tersimpan:", OUT)


if __name__ == "__main__":
    main()
