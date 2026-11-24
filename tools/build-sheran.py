"""Build the Sheranwala Developers web media from the raw "Sheran Wala Developers/" folder (not committed).

Images -> media/sheran-<i>.webp (1080px wide) and media/sheran-<i>-s.webp (480px wide)
  1-8   single posts (in SINGLES order)
  9-14  Carosuel 1, 15-20 Carosuel 2, 21-26 Carosuel 3 (slides in swipe order)
Reel   -> reels/13.mp4 and media/reel-13.webp / reel-13-s.webp (poster frame)

Run from the portfolio root:
    python tools/build-sheran.py
"""
import os, subprocess
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'Sheran Wala Developers')
MEDIA = os.path.join(ROOT, 'media')
IMG = ('.jpg', '.jpeg', '.png', '.webp')
REEL_NO = 13
# positions (in name order) of the single posts, in the order the page shows them
SINGLES = [1, 4, 2, 3, 5, 7, 6, 0]


def files(folder):
    d = os.path.join(RAW, folder)
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.lower().endswith(IMG))


def save(src, i):
    im = Image.open(src).convert('RGB')
    for w, suffix, q in ((1080, '', 82), (480, '-s', 76)):
        out = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        out.save(os.path.join(MEDIA, f'sheran-{i}{suffix}.webp'), 'WEBP', quality=q, method=6)


singles = files('')
order = [singles[k] for k in SINGLES]
for c in ('Carosuel 1', 'Carosuel 2', 'Carosuel 3'):
    order += files(c)
for i, f in enumerate(order, 1):
    save(f, i)
print(f'{len(order)} images')

vid = next(os.path.join(RAW, f) for f in os.listdir(RAW) if f.lower().endswith('.mp4'))
dst = os.path.join(ROOT, 'reels', f'{REEL_NO}.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-vf', "scale='min(720,iw)':-2", '-c:v', 'libx264', '-crf', '26',
                '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', dst], check=True)
for h, suffix, q in ((720, '', 80), (640, '-s', 76)):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '2', '-i', dst, '-frames:v', '1', '-vf', f'scale=-2:{h}',
                    '-c:v', 'libwebp', '-quality', str(q), os.path.join(MEDIA, f'reel-{REEL_NO}{suffix}.webp')], check=True)
print('reel', os.path.getsize(dst) // 1024, 'KB')
