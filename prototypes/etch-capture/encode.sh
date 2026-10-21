#!/usr/bin/env bash
# PROTOTYPE (happy-dwarf-team/.github#15): encode the spike's masters with the #8 settings at a
# few CRFs and report size and SSIM against the master. Usage: encode.sh <ffmpeg-bin> <out-root>
set -euo pipefail
F="$1"; O="$2"; E="$O/encodes"; mkdir -p "$E"
ff() { "$F/ffmpeg.exe" -hide_banner -loglevel error -y "$@"; }

# Masters: ~15.3 s of the edit loop, 30 fps, even sizes, lossless RGB -> yuv444p ref for SSIM.
ff -ss 0.5 -t 15.3 -i "$O/loop-dpr1/gfx-master.mkv" -vf "fps=30" -c:v ffv1 "$E/m-gfx1x.mkv"
ff -ss 0.5 -t 15.3 -i "$O/loop-dpr2/gfx-master.mkv" -vf "crop=3838:2158:0:0,fps=30" -c:v ffv1 "$E/m-gfx2x.mkv"
ff -i "$E/m-gfx2x.mkv" -vf "scale=1920:1080:flags=lanczos" -c:v ffv1 "$E/m-gfx2x-down.mkv"
pw1=$(ls "$O"/loop-dpr1/pw-video/*.webm | head -1)
ff -ss 6.2 -t 15.3 -i "$pw1" -vf "fps=30" -c:v ffv1 "$E/m-pw1x.mkv"

vp9() { # src crf out
  local a=(-i "$1" -an -c:v libvpx-vp9 -b:v 0 -crf "$2" -pix_fmt yuv420p -tune-content screen -deadline good -cpu-used 1 -row-mt 1 -g 240)
  (cd "$E" && ff "${a[@]}" -pass 1 -passlogfile "$3" -f null NUL && ff "${a[@]}" -pass 2 -passlogfile "$3" "$3.webm")
}
x264() { ff -i "$1" -an -c:v libx264 -preset veryslow -crf "$2" -pix_fmt yuv420p -profile:v high -g 240 -movflags +faststart "$E/$3.mp4"; }
ssim() { "$F/ffmpeg.exe" -hide_banner -i "$1" -i "$2" -lavfi "[0:v]format=yuv420p[a];[1:v]format=yuv420p[b];[a][b]ssim" -f null - 2>&1 | grep -o "All:[0-9.]*" | cut -d: -f2; }

echo "file,bytes,ssim_vs_master" > "$E/results.csv"
row() { echo "$(basename "$2"),$(stat -c %s "$2"),$(ssim "$1" "$2")" | tee -a "$E/results.csv"; }

for src in gfx1x gfx2x-down pw1x; do
  for c in 30 34 38 42; do vp9 "$E/m-$src.mkv" $c "$src-vp9-crf$c"; row "$E/m-$src.mkv" "$E/$src-vp9-crf$c.webm"; done
  for c in 20 23 26 29; do x264 "$E/m-$src.mkv" $c "$src-h264-crf$c"; row "$E/m-$src.mkv" "$E/$src-h264-crf$c.mp4"; done
done
for c in 34 40; do vp9 "$E/m-gfx2x.mkv" $c "gfx2x-vp9-crf$c"; row "$E/m-gfx2x.mkv" "$E/gfx2x-vp9-crf$c.webm"; done
for c in 23 28; do x264 "$E/m-gfx2x.mkv" $c "gfx2x-h264-crf$c"; row "$E/m-gfx2x.mkv" "$E/gfx2x-h264-crf$c.mp4"; done
echo done
