#!/usr/bin/env bash
# Membuat bukti terminal asli untuk laporan I-1.
# Setiap langkah: ketik perintah ke shell interaktif, tunggu, lalu tangkap
# jendela terminalnya. Prompt, gema perintah, dan keluaran berasal dari bash
# dan dari mesin ini, bukan gambar buatan.
set -u

DIR=${1:?butuh folder kerja}
OUT=${2:?butuh folder keluaran}
FIFO=/tmp/shotest/shot.fifo
mkdir -p "$OUT"
rm -f "$FIFO"; mkfifo "$FIFO"

cd "$DIR" || exit 1

io.elementary.terminal -n -w "$DIR" -x "bash --noprofile --rcfile $HOME/.bashrc -i < $FIFO" \
  > /dev/null 2>&1 &
TERM_PID=$!
sleep 4

exec 3>"$FIFO"

tangkap() {
  local nama=$1
  sleep 0.7
  gdbus call --session --dest org.gnome.Shell.Screenshot \
    --object-path /org/gnome/Shell/Screenshot \
    --method org.gnome.Shell.Screenshot.ScreenshotWindow \
    true false false "$OUT/$nama.png" > /dev/null 2>&1
  echo "  -> $nama.png"
}

ketik() {
  printf '%s\n' "$1" >&3
}

# Bersihkan layar supaya baris peluncuran terminal tidak ikut tertangkap.
ketik 'clear'
sleep 1

# 1. prompt dan folder kerja
tangkap "ss-1-prompt"

# 2. identitas sistem
ketik 'hostname'
tangkap "ss-2-hostname"

ketik 'uname -srm'
tangkap "ss-3-kernel"

ketik 'grep -E "PRETTY_NAME|VERSION_ID" /etc/os-release'
tangkap "ss-4-os-release"

# 3. perangkat keras
ketik 'lscpu | grep -E "^Architecture|^CPU\(s\)|Model name|Thread|Core"'
tangkap "ss-5-cpu"

ketik 'df -hT /'
tangkap "ss-6-disk"

# 4. memori
ketik 'grep -E "^MemTotal|^MemAvailable|^MemFree|^SwapTotal" /proc/meminfo'
tangkap "ss-7-meminfo"

# 5. layanan dan proses
ketik 'ps -p 1 -o pid=,comm='
tangkap "ss-8-init"

ketik 'systemctl list-units --type=service --state=running --no-pager --no-legend | wc -l'
tangkap "ss-9-jumlah-unit"

ketik 'ps -e --no-headers | wc -l'
tangkap "ss-10-jumlah-proses"

# 6. program pemetaan
ketik 'python3 peta_so_kebun.py'
sleep 3
tangkap "ss-11-program"

exec 3>&-
sleep 1
kill "$TERM_PID" 2>/dev/null
rm -f "$FIFO"
echo "selesai: $(ls -1 "$OUT"/*.png | wc -l) tangkapan layar"
